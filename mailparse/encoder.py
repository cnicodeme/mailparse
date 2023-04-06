# -*- config:utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.message import Message
from email.encoders import encode_noop
from email.header import Header
from email.utils import quote, make_msgid, formataddr, formatdate
from email.generator import Generator, BytesGenerator
from .utils import normalize_keys, EMAIL_HEADERS
from io import StringIO, BytesIO

__all__ = ('EmailEncode',)


# Note This list is different between Decoder and Encoder. That's why it's not in utils.py
_ignore_headers = ('received', 'content-transfer-encoding', 'content-type', 'mime-version', 'timestamp')


class EmailEncode(object):
    def __init__(self, obj):
        text_msg = None
        if obj.get('text') is not None:
            text_msg = MIMEText(self._add_blankline(obj.get('text')), 'plain', 'utf-8')

        html_msg = None
        if obj.get('html') is not None:
            html_msg = MIMEText(self._add_blankline(obj.get('html')), 'html', 'utf-8')

        if text_msg and html_msg:
            parent = MIMEMultipart('alternative')
            parent.attach(text_msg)
            parent.attach(html_msg)
        elif text_msg is not None:
            parent = text_msg
        elif html_msg is not None:
            parent = html_msg
        else:
            if not obj.get('inlines', []) and not obj.get('attachments', []):
                raise Exception('Missing body message (Either text or html).')

            if not obj.get('inlines') and len(obj.get('attachments', [])) == 1:
                item = obj.get('attachments')[0]
                parent = self._get_correct_mime(item.get('type'), self._add_blankline(item.get('content')), encoder=encode_noop)

            # Special case (yay) where the body is encrypted via PGP
            """
            @see https://pastebin.com/9NxMtWh6  for application/signature
            @see https://pastebin.com/Qv3MFFVL  for application/pgp-encrypted
            @see https://pastebin.com/4gF67Hmg  for application/pgp-encrypted (advanced)

            if len(obj.get('attachments', [])) == 1 and obj.get('attachments')[0].get('type') == 'application/pgp-encrypted':
                parent = MIMEMultipart('encrypted', _subparts={'protocol': 'application/pgp-encrypted'})

                parent.attach(text_msg)
                parent.attach(html_msg)
            """

        if obj.get('inlines', []):
            related = MIMEMultipart('related')
            related.attach(parent)
            for inline in obj.get('inlines'):
                item = self._get_correct_mime(inline.get('type'), self._add_blankline(inline.get('content')), encoder=encode_noop)
                related.attach(self._set_inline(item, inline))

            parent = related

        if obj.get('attachments', []):
            mixeds = []
            reports = []
            for attachment in obj.get('attachments'):
                maintype, subtype = attachment.get('type').lower().split('/')

                is_mixed = False
                if maintype == 'text':
                    attach = MIMEText(self._add_blankline(attachment.get('content')), subtype, 'utf-8')
                elif maintype == 'message':
                    msg = Message()
                    msg.set_payload(self._add_blankline(attachment.get('content')) + '\r\n', None)
                    attach = MIMEMessage(msg, subtype)
                else:
                    is_mixed = True
                    attach = MIMEApplication(self._add_blankline(attachment.get('content')), subtype, _encoder=encode_noop)
                    attach['Content-Transfer-Encoding'] = 'base64'

                attach = self._set_attachment(attach, attachment)
                if is_mixed:
                    mixeds.append(attach)
                else:
                    reports.append(attach)

            mixed = None
            if mixeds:
                mixed = MIMEMultipart('mixed')
                mixed.attach(parent)

            report = None
            if reports:
                report = MIMEMultipart('report')
                if not mixed:
                    report.attach(parent)

                for r in reports:
                    report.attach(r)

            if mixed is not None:
                if report:
                    mixed.attach(report)
                for m in mixeds:
                    mixed.attach(m)

                parent = mixed
            elif report is not None:
                parent = report

            if reports:
                parent.set_param('report-type', 'delivery-status')

        parent.set_param('charset', 'utf-8')

        headers = obj.get('headers')
        for key in obj.keys():
            if key in ('headers', 'html', 'text', 'inlines', 'attachments', 'bcc'):
                continue

            headers[normalize_keys(key)] = obj[key]

        for header in headers:
            if header.lower() in _ignore_headers:
                continue

            if not isinstance(headers[header], (dict, list)):
                parent[header] = self._encode_header(headers[header])
                continue

            items = headers[header]
            if isinstance(headers[header], dict):
                items = [headers[header]]

            for current in items:
                if isinstance(current, dict) and header.lower() in EMAIL_HEADERS:
                    if current.get('email') is None:
                        raise Exception('Invalid email provided. Field {0} is missing the email value!'.format(header.lower()))

                    parent[normalize_keys(header)] = formataddr((self._encode_header(current.get('name')), self._encode_header(current.get('email'))))
                else:
                    parent[normalize_keys(header)] = self._encode_header(current)

        if 'date' not in parent:
            parent['Date'] = formatdate()

        self.email = parent

    def _get_correct_mime(self, content_type, data, encoder=None):
        maintype, subtype = content_type.lower().split('/')

        if maintype == 'image':
            return MIMEImage(data, subtype, _encoder=encoder)
        elif maintype == 'audio':
            return MIMEAudio(data, subtype, _encoder=encoder)
        elif maintype == 'text':
            return MIMEText(data, subtype, 'utf-8')
        elif maintype == 'message':
            msg = Message()
            msg.set_payload(data + '\r\n', None)
            return MIMEMessage(msg, subtype)
        elif maintype == 'application':
            item = MIMEApplication(data, subtype, _encoder=encoder)
            item['Content-Transfer-Encoding'] = 'base64'
            return item

    def _set_inline(self, item, inline):
        if inline.get('name'):
            item.set_param('name', quote(inline.get('name')))
            item['Content-Disposition'] = 'inline; filename="{0}"'.format(quote(inline.get('name')))

        item['Content-Transfer-Encoding'] = 'base64'
        item['Content-ID'] = '<{0}>'.format(inline.get('cid'))
        item['X-Attachment-Id'] = inline.get('cid')
        return item

    def _set_attachment(self, item, attachment):
        item.set_type(attachment.get('type'))
        if attachment.get('name'):
            item.set_param('name', quote(attachment.get('name')))
            item['Content-Disposition'] = 'attachment; filename="{0}"'.format(quote(attachment.get('name')))

        if attachment.get('description'):
            item['Content-Description'] = attachment.get('description')

        return item

    def _encode_header(self, value):
        if value is None:
            return None

        try:
            value.encode('ascii')
            return value
        except UnicodeEncodeError:
            return Header(value, 'utf-8').encode()

    def __str__(self):
        fp = StringIO()
        g = Generator(fp, mangle_from_=False, maxheaderlen=60)
        g.flatten(self.email)
        return fp.getvalue()

    def __bytes__(self):
        fp = BytesIO()
        g = BytesGenerator(fp, mangle_from_=False, maxheaderlen=60)
        g.flatten(self.email)
        return fp.getvalue()

    def _add_blankline(self, payload):
        return '{0}\r\n'.format(payload.strip())

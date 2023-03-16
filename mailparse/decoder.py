# -*- config:utf-8 -*-

from email import message_from_bytes, message_from_string
from email.utils import parseaddr, parsedate_to_datetime, formataddr, getaddresses
from email.header import decode_header
from email import policy
from .utils import EMAIL_HEADERS, NOT_HEADERS, SINGLE_HEADERS, normalize_keys

import re, datetime, base64


__all__ = ('EmailDecode',)

# Note This list is different between Decoder and Encoder. That's why it's not in utils.py
_ignore_headers = ('content-transfer-encoding', 'content-type', 'timestamp')


class EmailDecode(dict):
    def __init__(self, email):
        self['headers'] = {}
        self['text'] = None
        self['html'] = None

        # We try to find the charset
        self.default_charset = email.get_content_charset()

        if self.default_charset is None:
            # If we haven't found it, we parse the body to find the correct one
            for c in email.get_charsets():
                if c is not None:
                    self.default_charset = c
                    break

        if self.default_charset is None and 'subject' in email:
            # Finally, our last try is with the subject
            for r in decode_header(email.get('subject')):
                if r[1] is not None:
                    self.default_charset = r[1]
                    break

        if self.default_charset:
            self.default_charset = self.default_charset.upper().replace('HTTP-EQUIVCONTENT-TYPE', '')

        for k in list(set(email.keys())):
            k = k.lower()
            if k in _ignore_headers:
                continue

            try:
                if k in NOT_HEADERS:
                    self._headers(k, email.get_all(k))
                else:
                    self._headers(normalize_keys(k), email.get_all(k), subpart='headers')
            except AttributeError:
                continue

        date = self.get('date')
        if date is not None:
            # Date is (should be) in RFC 2822 format
            if isinstance(date, list):
                date = date[0]

            try:
                parsed = parsedate_to_datetime(date)
                """
                `.timestamp` handles TZ Infos
                if parsed.tzinfo is not None and str(parsed.tzinfo) != 'UTC':
                    # Timezone aware when needed!
                    parsed = parsed.astimezone(pytz.UTC)
                """

                self['timestamp'] = int(parsed.timestamp())
            except (ValueError, TypeError, AssertionError):
                # Saw a "Year out of range" once! With a year of ... 1899 ...
                self['timestamp'] = int(datetime.datetime.utcnow().timestamp())

        self._process_payload(email)

    def _headers(self, key, values, subpart=None):
        base = self
        if subpart:
            base = self[subpart]

        # When subpart, the key has been normalized, so not lowered
        key_lower = key.lower()
        if key in EMAIL_HEADERS:
            values = [formataddr(x) for x in getaddresses(values)]

        for value in values:
            if not isinstance(value, (bytes, str)):
                value = str(value)

            if key_lower in EMAIL_HEADERS:
                value = self._parse_email(value)
                if not value:
                    continue

                if value['name']:
                    value['name'] = self._clear(value['name'])
            else:
                value = self._clear(value)

            if value is None or value == '':
                continue

            if key_lower in SINGLE_HEADERS:
                if key not in base:
                    # We only add the header if it is not already present
                    base[key] = value
            else:
                if key not in base:
                    base[key] = []

                base[key].append(value)

    def _clear(self, value):
        results = decode_header(value)

        if len(results) == 1:
            value = self._decode_str(results[0][0], results[0][1])
        else:
            parts = []
            for r in results:
                parts.append(self._decode_str(r[0], r[1]))
            value = ' '.join(parts)

        return re.sub(r"[\ ]{1,}", ' ', value.strip()).replace('\r', '\n').replace('\n', '').strip('"').strip("'")

    def _decode_str(self, value, charset=None):
        """
        Decodes a given str from a specific charset to UTF-8
        """
        if value is None:
            return None

        if charset:
            charset = charset.upper().replace('HTTP-EQUIVCONTENT-TYPE', '')
        else:
            charset = 'UTF-8'

        # First thing, we translate to charset
        # If it fails, if default != charset, we translate via self.default_charset
        # if it fails, and default != utf-8 and charset != 8, we translate via utf-8 (default)

        # If it's a bytes, we keep it that way
        # Otherwise:
        if isinstance(value, str):
            # We convert the value into bytes
            value = self._encode_charset(value, charset)

        # Now we return a str:
        return self._decode_charset(value, charset)

    def _encode_charset(self, value, charset=None):
        try:
            return value.encode(charset)
        except (LookupError, UnicodeEncodeError):
            pass

        # Given charset failed, we try with the default, if different
        if self.default_charset != charset:
            try:
                return value.encode(self.default_charset)
            except (LookupError, UnicodeEncodeError):
                pass

        if charset != 'UTF-8' and self.default_charset != 'UTF-8':
            try:
                return value.encode('UTF-8')
            except (LookupError, UnicodeEncodeError):
                pass

        # Fall back to an easy value
        return value.encode('utf-8', errors='xmlcharrefreplace')

    def _decode_charset(self, value, charset=None):
        try:
            return value.decode(charset)
        except (LookupError, UnicodeDecodeError):
            pass

        # Given charset failed, we try with the default, if different
        if self.default_charset and self.default_charset != charset:
            try:
                return value.decode(self.default_charset)
            except (LookupError, UnicodeDecodeError):
                pass

        if charset != 'UTF-8' and self.default_charset != 'UTF-8':
            try:
                return value.decode('UTF-8')
            except (LookupError, UnicodeDecodeError):
                pass

        # Fall back to an easy value
        return value.decode('utf-8', errors='replace')  # errors='backslashreplace')

    def _parse_email(self, email):
        (name, email) = parseaddr(email)
        if email == '' or email.find('@') == -1:
            return None

        if name == '':
            name = None

        return {'name': name, 'email': email}

    def _merge_multiple_payload(self, payload, default_charset, decode=True):
        charset = payload.get_content_charset() or default_charset

        if payload.get_content_type().lower() in ('message/rfc822', 'message/delivery-status'):
            content = []
            for pl in payload.get_payload():
                try:
                    content.append(self._decode_str(bytes(pl.get_body())))
                except AttributeError:
                    content.append(self._decode_str(bytes(pl)))

            content = ''.join(content)

        elif payload.is_multipart():
            content = []
            for pl in payload.get_payload():
                content.append(self._merge_multiple_payload(pl, charset))

            content = '\r\n\r\n'.join(content)
        else:
            content = self._decode_str(payload.get_payload(decode=decode), charset)

        return content

    def _process_payload(self, payload, default_charset=None):
        charset = payload.get_content_charset() or default_charset

        if payload.is_multipart() and payload.get_content_maintype().lower() != 'message':
            for pl in payload.get_payload():
                self._process_payload(pl, charset)
        else:
            if payload.get_content_disposition() != 'attachment' and payload.get_content_type().lower() == 'text/plain':
                self['text'] = self._decode_str(payload.get_payload(decode=True).strip(), charset)
            elif payload.get_content_disposition() != 'attachment' and payload.get_content_type().lower() == 'text/html':
                self['html'] = self._decode_str(payload.get_payload(decode=True).strip(), charset)
            else:
                attachment = {
                    'type': payload.get_content_type(),
                    'name': self._decode_str(payload.get_filename(), charset)
                }

                if payload.get('content-description') is not None:
                    attachment['description'] = self._decode_str(str(payload.get('content-description')), charset)

                if str(payload.get('Content-Transfer-Encoding')) == 'base64':
                    attachment['content'] = self._merge_multiple_payload(payload, charset, decode=False)
                elif payload.get_content_maintype().lower() in ('text', 'message'):
                    content = self._merge_multiple_payload(payload, charset)
                    attachment['content'] = self._decode_str(content, charset)
                else:
                    attachment['content'] = base64.b64encode(self._decode_str(payload.get_payload(decode=True), charset).encode('utf-8')).decode('utf-8')

                attachment['content'] = attachment['content'].strip()

                key = 'attachments'
                if payload.get_content_disposition() == 'inline' and payload.get_content_maintype().lower() == 'image' and payload.get('content-id'):
                    """
                    get_content_disposition() : returns the **lowercased** value of the Content-Disposition header if any, with either "attachment", "inline" or None
                    We only consider images to be inline, so any other format is an attachment
                    The image must have a content-id to be considered inline too
                    """
                    # We only consider images to be inline
                    key = 'inlines'
                    attachment['cid'] = str(payload.get('content-id'))[1:-1]

                if key not in self:
                    self[key] = []

                self[key].append(attachment)

    @classmethod
    def load(cls, data, policy=None):
        """
        Allows to set a custom policy. By default the policy is the default from Python's: `policy.compat32`
        """
        options = {}
        if policy:
            options = {'policy': policy}

        if isinstance(data, bytes):
            mail = message_from_bytes(data, **options)
        elif isinstance(data, str):
            mail = message_from_string(data, **options)

        return EmailDecode(mail)

    @classmethod
    def open(cls, path, policy=None):
        # We'll let Python fail in case the path is not correct
        with open(path, 'rb') as fp:
            return cls.load(fp.read(), policy)

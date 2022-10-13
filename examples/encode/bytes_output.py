# -*- config:utf-8 -*-

"""
This script will parse a well-structured dict (generated from EmailDecode for instance) into a well formed EML file.
"""

from mailparse import EmailEncode

# Note: We stripped the unnecessary headers, like received and DKIM, as they are not needed in this scenario
eml = EmailEncode({
    "headers": {
        "Delivered-To": {
            "name": None,
            "email": "some-user@recipient.com"
        },
        "Mime-Version": "1.0"
    },
    "from": {
        "name": "Cyril",
        "email": "cyril@sender.com"
    },
    "return-path": {
        "name": None,
        "email": "some-return-path@sender.com"
    },
    "message-id": "<68950604-d564-40c2-bcb4-e58f5070fdcb@mailsender.net>",
    "subject": "Sample email",
    "to": [
        {
            "name": None,
            "email": "some-user@recipient.com"
        }
    ],
    "date": "Thu, 13 Oct 2022 09:23:24 +0000",
    "timestamp": 1665653004,
    "text": "This is a sample email that contains *inline images* and *attachments* to\nshowcase how MailParse will handle these.\n\nLook at this:\n[image: nice-animation.gif]\n\nNice, isn't it?",
    "html": "<div dir=\"ltr\"><div class=\"gmail_quote\"><div dir=\"ltr\"><div class=\"gmail_quote\"><div dir=\"ltr\">This is a sample email that contains\u00a0<u>inline images</u>\u00a0and\u00a0<b>attachments</b>\u00a0to showcase how MailParse will handle these.<div><br></div><div>Look at this:</div><div><img src=\"cid:ii_l96uj1bo1\" alt=\"nice-animation.gif\" width=\"542\" height=\"542\"><br></div><div><br></div><div>Nice, isn&#39;t it?<br></div><div><br></div></div>\n</div></div>\n</div></div>",
    "inlines": [
        {
            "type": "image/gif",
            "name": "nice-animation.gif",
            "content": "R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
            "cid": "ii_l96uj1bo1"
        }
    ],
    "attachments": [
        {
            "type": "application/pdf",
            "name": "fake.pdf",
            "content": "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJF\nICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQg\nNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdC\ni9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqC\njMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyC\njw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
        }
    ]
})

print(bytes(eml))

"""
Outputs:
b'MIME-Version: 1.0\nContent-Type: multipart/mixed; charset="utf-8";\n boundary="===============3464895521335920506=="\nDKIM-Signature: a=rsa-sha256; v=1; c=relaxed/relaxed;\n d=reflectiv.net; q=dns/txt; s=mx; t=1665653008;\n x=1665739408;\n h=Content-Type: MIME-Version: In-Reply-To: References: To:\n To: Message-Id: Subject: Subject: Date: From: From: Sender;\n bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=;\n b=WRKUEgi1Xl4V3furRD19kktudXg5b9r6ORA9vBU39ba2OXACtrWcav8dHQKB1Eyu5fegSaW/\n GYLVXDfAxljjpXrEtKIBlmizKidyrWzLesz+H89fJeHip0K1GU7M2HfgaN+CLpXpUm6FsW3Z\n CA/Y2Dmp/hdeQS6WdUmjoHDDvlw=\nDKIM-Signature: v=1; a=rsa-sha1; c=relaxed/relaxed;\n s=pm20220416; d=pm.mtasv.net;\n h=From:Date:Subject:Message-Id:To:References:In-Reply-To:MIME-Version:Content-Type;\n bh=9T5/y8MgajuzE8mei59utoNV/m4=;\n b=zgc4MHKYAbg7OCQsmavFPXrQOAk9/HoC0HDz29xIlNG1IEPQduX/erndJ71fz8dkMGk3lyYg1K9J\n w2lLw7cWrYCPETs+6Q4HPKEWPdyxxc3llc1X5iDCkB+MMQVXM5zQXm8+dhBOKI+E1ey7crLRNRFP\n z2D09bquYC/TRuEDKY0=\nDKIM-Signature: v=1; a=rsa-sha256; d=sender.com;\n s=20220909140117pm; c=relaxed/relaxed; i=cyril@sender.com;\n t=1665653004;\n h=date:date:from:from:message-id:reply-to:sender:subject:subject:to:to:cc:\n references:in-reply-to:feedback-id:mime-version:content-type;\n bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=;\n b=IdBcDvOE64rtHIZ0HlqGC3/PuYGv/pV3Vk4flWObFSSM96y+3p8epWb/02xd+skEStV0Oy/p1gl\n NiIrgu9yimzBbXlc+2TtjcfMjNnp/1cOL27mMeRgxi1XvphcWXgq/hMs+6bF3QJl6r9kpD2M9QyEV\n lpcQ61nDmS/G5sWTphs=\nDelivered-To: some-user@recipient.com\nReturn-Path: some-return-path@sender.com\nFrom: Cyril <cyril@sender.com>\nSubject: Sample email\nTo: some-user@recipient.com\nMessage-Id: \n <68950604-d564-40c2-bcb4-e58f5070fdcb@mailsender.net>\nDate: Thu, 13 Oct 2022 09:23:24 +0000\n\n--===============3464895521335920506==\nContent-Type: multipart/related;\n boundary="===============3962430719656374274=="\nMIME-Version: 1.0\n\n--===============3962430719656374274==\nContent-Type: multipart/alternative;\n boundary="===============2221641724099839942=="\nMIME-Version: 1.0\n\n--===============2221641724099839942==\nContent-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nVGhpcyBpcyBhIHNhbXBsZSBlbWFpbCB0aGF0IGNvbnRhaW5zICppbmxpbmUgaW1hZ2VzKiBhbmQg\nKmF0dGFjaG1lbnRzKiB0bwpzaG93Y2FzZSBob3cgTWFpbFBhcnNlciB3aWxsIGhhbmRsZSB0aGVz\nZS4KCkxvb2sgYXQgdGhpczoKW2ltYWdlOiBuaWNlLWFuaW1hdGlvbi5naWZdCgpOaWNlLCBpc24n\ndCBpdD8NCg==\n\n--===============2221641724099839942==\nContent-Type: text/html; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nPGRpdiBkaXI9Imx0ciI+PGRpdiBjbGFzcz0iZ21haWxfcXVvdGUiPjxkaXYgZGlyPSJsdHIiPjxk\naXYgY2xhc3M9ImdtYWlsX3F1b3RlIj48ZGl2IGRpcj0ibHRyIj5UaGlzIGlzIGEgc2FtcGxlIGVt\nYWlsIHRoYXQgY29udGFpbnPCoDx1PmlubGluZSBpbWFnZXM8L3U+wqBhbmTCoDxiPmF0dGFjaG1l\nbnRzPC9iPsKgdG8gc2hvd2Nhc2UgaG93IE1haWxQYXJzZXIgd2lsbCBoYW5kbGUgdGhlc2UuPGRp\ndj48YnI+PC9kaXY+PGRpdj5Mb29rIGF0IHRoaXM6PC9kaXY+PGRpdj48aW1nIHNyYz0iY2lkOmlp\nX2w5NnVqMWJvMSIgYWx0PSJuaWNlLWFuaW1hdGlvbi5naWYiIHdpZHRoPSI1NDIiIGhlaWdodD0i\nNTQyIj48YnI+PC9kaXY+PGRpdj48YnI+PC9kaXY+PGRpdj5OaWNlLCBpc24mIzM5O3QgaXQ/PGJy\nPjwvZGl2PjxkaXY+PGJyPjwvZGl2PjwvZGl2Pgo8L2Rpdj48L2Rpdj4KPC9kaXY+PC9kaXY+DQo=\n\n--===============2221641724099839942==--\n\n--===============3962430719656374274==\nMIME-Version: 1.0\nContent-Type: image/gif; name="nice-animation.gif"\nContent-Disposition: inline; filename="nice-animation.gif"\nContent-Transfer-Encoding: base64\nContent-ID: <ii_l96uj1bo1>\nX-Attachment-Id: ii_l96uj1bo1\n\nR0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==\n\n--===============3962430719656374274==--\n\n--===============3464895521335920506==\nContent-Transfer-Encoding: base64\nMIME-Version: 1.0\nContent-Type: application/pdf; name="fake.pdf"\nContent-Disposition: attachment; filename="fake.pdf"\n\nJVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJF\nICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQg\nNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdC\ni9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqC\njMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyC\njw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G\n\n--===============3464895521335920506==--\n'
"""
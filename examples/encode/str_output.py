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

print(str(eml))

"""
Outputs:

MIME-Version: 1.0
Content-Type: multipart/mixed; charset="utf-8";
 boundary="===============3769984348166854544=="
Delivered-To: some-user@recipient.com
Return-Path: some-return-path@sender.com
Subject: Sample email
Message-Id: 
 <68950604-d564-40c2-bcb4-e58f5070fdcb@mailsender.net>
From: Cyril <cyril@sender.com>
To: some-user@recipient.com
Date: Thu, 13 Oct 2022 09:23:24 +0000

--===============3769984348166854544==
Content-Type: multipart/related;
 boundary="===============0128438130676831463=="
MIME-Version: 1.0

--===============0128438130676831463==
Content-Type: multipart/alternative;
 boundary="===============3679524713184124586=="
MIME-Version: 1.0

--===============3679524713184124586==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64

VGhpcyBpcyBhIHNhbXBsZSBlbWFpbCB0aGF0IGNvbnRhaW5zICppbmxpbmUgaW1hZ2VzKiBhbmQg
KmF0dGFjaG1lbnRzKiB0bwpzaG93Y2FzZSBob3cgTWFpbFBhcnNlciB3aWxsIGhhbmRsZSB0aGVz
ZS4KCkxvb2sgYXQgdGhpczoKW2ltYWdlOiBuaWNlLWFuaW1hdGlvbi5naWZdCgpOaWNlLCBpc24n
dCBpdD8NCg==

--===============3679524713184124586==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64

PGRpdiBkaXI9Imx0ciI+PGRpdiBjbGFzcz0iZ21haWxfcXVvdGUiPjxkaXYgZGlyPSJsdHIiPjxk
aXYgY2xhc3M9ImdtYWlsX3F1b3RlIj48ZGl2IGRpcj0ibHRyIj5UaGlzIGlzIGEgc2FtcGxlIGVt
YWlsIHRoYXQgY29udGFpbnPCoDx1PmlubGluZSBpbWFnZXM8L3U+wqBhbmTCoDxiPmF0dGFjaG1l
bnRzPC9iPsKgdG8gc2hvd2Nhc2UgaG93IE1haWxQYXJzZXIgd2lsbCBoYW5kbGUgdGhlc2UuPGRp
dj48YnI+PC9kaXY+PGRpdj5Mb29rIGF0IHRoaXM6PC9kaXY+PGRpdj48aW1nIHNyYz0iY2lkOmlp
X2w5NnVqMWJvMSIgYWx0PSJuaWNlLWFuaW1hdGlvbi5naWYiIHdpZHRoPSI1NDIiIGhlaWdodD0i
NTQyIj48YnI+PC9kaXY+PGRpdj48YnI+PC9kaXY+PGRpdj5OaWNlLCBpc24mIzM5O3QgaXQ/PGJy
PjwvZGl2PjxkaXY+PGJyPjwvZGl2PjwvZGl2Pgo8L2Rpdj48L2Rpdj4KPC9kaXY+PC9kaXY+DQo=

--===============3679524713184124586==--

--===============0128438130676831463==
MIME-Version: 1.0
Content-Type: image/gif; name="nice-animation.gif"
Content-Disposition: inline; filename="nice-animation.gif"
Content-Transfer-Encoding: base64
Content-ID: <ii_l96uj1bo1>
X-Attachment-Id: ii_l96uj1bo1

R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==

--===============0128438130676831463==--

--===============3769984348166854544==
Content-Transfer-Encoding: base64
MIME-Version: 1.0
Content-Type: application/pdf; name="fake.pdf"
Content-Disposition: attachment; filename="fake.pdf"

JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJF
ICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQg
NSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdC
i9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqC
jMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyC
jw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G

--===============3769984348166854544==--
"""
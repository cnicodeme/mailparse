# MailParse

This library is intended to convert to and from a raw email (EML format) to a Python dictionnary.

This is the current library used at [ImprovMX](https://improvmx.com) and [Fernand](https://getfernand.com).
It was heavily tested in production by handling millions of emails that were parsed to be sent as JSON dictionnary to webhooks.


## Features

 * Support emails with complex structure, such as inline images, attachments, and other odd media.
 * Battle tested in production at ImprovMX


## Decoding an EML email

Take this email sample:

sample.eml:

```eml
Delivered-To: some-user@recipient.com
Received: by 2002:xxxx:2010:0:b0:1e2:d052:cd91 with SMTP id t16csp2528xxxxx;
        Thu, 13 Oct 2022 02:23:36 -0700 (PDT)
Return-Path: <some-return-path@sender.com>
Received: from server-001.forwarder.com (server-001.forwarder.com. [198.61.254.xxx])
        by mx.webmail.com with UTF8SMTPS id p2-20020a056902114200b006c081d13801si16135744ybu.666.2022.10.13.02.23.xxx
        for <some-user@recipient.com>
        (version=TLS1_3 cipher=TLS_AES_128_GCM_SHA256 bits=128/128);
        Thu, 13 Oct 2022 02:23:34 -0700 (PDT)
DKIM-Signature: a=rsa-sha256; v=1; c=relaxed/relaxed; d=reflectiv.net; q=dns/txt; s=mx; t=1665653008; x=1665739408; h=Content-Type: MIME-Version: In-Reply-To: References: To: To: Message-Id: Subject: Subject: Date: From: From: Sender; bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=; b=WRKUEgi1Xl4V3furRD19kktudXg5b9r6ORA9vBU39ba2OXACtrWcav8dHQKB1Eyu5fegSaW/ GYLVXDfAxljjpXrEtKIBlmizKidyrWzLesz+H89fJeHip0K1GU7M2HfgaN+CLpXpUm6FsW3Z CA/Y2Dmp/hdeQS6WdUmjoHDDvlw=
Received: from server-001.firstforward.com (server-001.firstforward.com [104.245.209.xxx]) by 9a93c0110be9 with SMTP id <undefined> (version=TLS1.2, cipher=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256); Thu, 13 Oct 2022 09:23:26 GMT
DKIM-Signature: v=1; a=rsa-sha1; c=relaxed/relaxed; s=pm20220416; d=pm.mtasv.net; h=From:Date:Subject:Message-Id:To:References:In-Reply-To:MIME-Version:Content-Type; bh=9T5/y8MgajuzE8mei59utoNV/m4=; b=zgc4MHKYAbg7OCQsmavFPXrQOAk9/HoC0HDz29xIlNG1IEPQduX/erndJ71fz8dkMGk3lyYg1K9J
   w2lLw7cWrYCPETs+6Q4HPKEWPdyxxc3llc1X5iDCkB+MMQVXM5zQXm8+dhBOKI+E1ey7crLRNRFP
   z2D09bquYC/TRuEDKY0=
Received: by server-001.firstforward.com id h8vcgs27tk4e for <some-user@recipient.com>; Thu, 13 Oct 2022 05:23:25 -0400 (envelope-from <pm_bounces@bounces.sender.com>)
DKIM-Signature: v=1; a=rsa-sha256; d=sender.com; s=20220909140117pm; c=relaxed/relaxed; i=cyril@sender.com; t=1665653004; h=date:date:from:from:message-id:reply-to:sender:subject:subject:to:to:cc: references:in-reply-to:feedback-id:mime-version:content-type; bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=; b=IdBcDvOE64rtHIZ0HlqGC3/PuYGv/pV3Vk4flWObFSSM96y+3p8epWb/02xd+skEStV0Oy/p1gl NiIrgu9yimzBbXlc+2TtjcfMjNnp/1cOL27mMeRgxi1XvphcWXgq/hMs+6bF3QJl6r9kpD2M9QyEV lpcQ61nDmS/G5sWTphs=
From: Cyril <cyril@sender.com>
Date: Thu, 13 Oct 2022 09:23:24 +0000
Subject: Sample email
Message-Id: <68950604-d564-40c2-bcb4-e58f5070fdcb@mailsender.net>
To: some-user@recipient.com
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=mk3-20c60ed498f446c485dcc6ebfbf93421

--mk3-20c60ed498f446c485dcc6ebfbf93421
Content-Type: multipart/related; boundary="=-Z2apUQnAeKYD25qUfsotFw=="

--=-Z2apUQnAeKYD25qUfsotFw==
Content-Type: multipart/alternative; boundary=mk3-b9ac3b13b7b54e60b6b1d61772776994; charset=UTF-8

--mk3-b9ac3b13b7b54e60b6b1d61772776994
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

This is a sample email that contains *inline images* and *attachments* to
showcase how MailParse will handle these.

Look at this:
[image: nice-animation.gif]

Nice, isn't it?

--mk3-b9ac3b13b7b54e60b6b1d61772776994
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

<div dir=3D"ltr"><div class=3D"gmail_quote"><div dir=3D"ltr"><div class=3D"=
gmail_quote"><div dir=3D"ltr">This is a sample email that contains=C2=A0<u>=
inline images</u>=C2=A0and=C2=A0<b>attachments</b>=C2=A0to showcase how Mai=
lParser will handle these.<div><br></div><div>Look at this:</div><div><img =
src=3D"cid:ii_l96uj1bo1" alt=3D"nice-animation.gif" width=3D"542" height=3D=
"542"><br></div><div><br></div><div>Nice, isn&#39;t it?<br></div><div><br><=
/div></div>
</div></div>
</div></div>

--mk3-b9ac3b13b7b54e60b6b1d61772776994--
--=-Z2apUQnAeKYD25qUfsotFw==
Content-Type: image/gif; name=nice-animation.gif
Content-Transfer-Encoding: base64
Content-Id: <ii_l96uj1bo1>
Content-Disposition: inline; filename=nice-animation.gif

R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==

--=-Z2apUQnAeKYD25qUfsotFw==--
--mk3-20c60ed498f446c485dcc6ebfbf93421
Content-Type: application/pdf; name=fake.pdf
Content-Transfer-Encoding: base64
Content-Id: <f_l96uiulr0>
Content-Disposition: attachment; filename=fake.pdf

JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJF
ICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQg
NSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdC
i9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqC
jMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyC
jw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G

--mk3-20c60ed498f446c485dcc6ebfbf93421--
```

Using `mailparse.EmailDecode`:

```python

from mailparse import EmailDecode
import json

decoded = EmailDecode.open('./sample.eml')
print(json.dumps(decoded, indent=4))
```

The output will be:

```json
{
    "headers": {
        "Received": [
            "by 2002:xxxx:2010:0:b0:1e2:d052:cd91 with SMTP id t16csp2528xxxxx; Thu, 13 Oct 2022 02:23:36 -0700 (PDT)",
            "from server-001.forwarder.com (server-001.forwarder.com. [198.61.254.xxx]) by mx.webmail.com with UTF8SMTPS id p2-20020a056902114200b006c081d13801si16135744ybu.666.2022.10.13.02.23.xxx for <some-user@recipient.com> (version=TLS1_3 cipher=TLS_AES_128_GCM_SHA256 bits=128/128); Thu, 13 Oct 2022 02:23:34 -0700 (PDT)",
            "from server-001.firstforward.com (server-001.firstforward.com [104.245.209.xxx]) by 9a93c0110be9 with SMTP id <undefined> (version=TLS1.2, cipher=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256); Thu, 13 Oct 2022 09:23:26 GMT",
            "by server-001.firstforward.com id h8vcgs27tk4e for <some-user@recipient.com>; Thu, 13 Oct 2022 05:23:25 -0400 (envelope-from <pm_bounces@bounces.sender.com>)"
        ],
        "DKIM-Signature": [
            "a=rsa-sha256; v=1; c=relaxed/relaxed; d=reflectiv.net; q=dns/txt; s=mx; t=1665653008; x=1665739408; h=Content-Type: MIME-Version: In-Reply-To: References: To: To: Message-Id: Subject: Subject: Date: From: From: Sender; bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=; b=WRKUEgi1Xl4V3furRD19kktudXg5b9r6ORA9vBU39ba2OXACtrWcav8dHQKB1Eyu5fegSaW/ GYLVXDfAxljjpXrEtKIBlmizKidyrWzLesz+H89fJeHip0K1GU7M2HfgaN+CLpXpUm6FsW3Z CA/Y2Dmp/hdeQS6WdUmjoHDDvlw=",
            "v=1; a=rsa-sha1; c=relaxed/relaxed; s=pm20220416; d=pm.mtasv.net; h=From:Date:Subject:Message-Id:To:References:In-Reply-To:MIME-Version:Content-Type; bh=9T5/y8MgajuzE8mei59utoNV/m4=; b=zgc4MHKYAbg7OCQsmavFPXrQOAk9/HoC0HDz29xIlNG1IEPQduX/erndJ71fz8dkMGk3lyYg1K9J w2lLw7cWrYCPETs+6Q4HPKEWPdyxxc3llc1X5iDCkB+MMQVXM5zQXm8+dhBOKI+E1ey7crLRNRFP z2D09bquYC/TRuEDKY0=",
            "v=1; a=rsa-sha256; d=sender.com; s=20220909140117pm; c=relaxed/relaxed; i=cyril@sender.com; t=1665653004; h=date:date:from:from:message-id:reply-to:sender:subject:subject:to:to:cc: references:in-reply-to:feedback-id:mime-version:content-type; bh=/53IJTVUCdu+CZR3Ar3YkFZdMTe6DkgbtBKyDBVn/2I=; b=IdBcDvOE64rtHIZ0HlqGC3/PuYGv/pV3Vk4flWObFSSM96y+3p8epWb/02xd+skEStV0Oy/p1gl NiIrgu9yimzBbXlc+2TtjcfMjNnp/1cOL27mMeRgxi1XvphcWXgq/hMs+6bF3QJl6r9kpD2M9QyEV lpcQ61nDmS/G5sWTphs="
        ],
        "Delivered-To": {
            "name": null,
            "email": "some-user@recipient.com"
        },
        "Mime-Version": "1.0"
    },
    "from": {
        "name": "Cyril",
        "email": "cyril@sender.com"
    },
    "return-path": {
        "name": null,
        "email": "some-return-path@sender.com"
    },
    "message-id": "<68950604-d564-40c2-bcb4-e58f5070fdcb@mailsender.net>",
    "subject": "Sample email",
    "to": [
        {
            "name": null,
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
}
```

### Alternatives way to load an EML

You can parse an EML file by either calling 

```EmailDecode.open(path_to_file)```

or by calling

```EmailDecode.load(str or bytes)```

Behind the dors, `open` will simply open the file in read and binary, and pass the data to `load`.


## Encoding an email

You can do the reverse operation by creating an instance of `mailparse.EmailEncode` and by passing an object structured similarly to the above generated one, and you'll get a valid EML output.

If we take the previous generated dict:

```python
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
```

The output will be:

```eml
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
```

## Main Headers

We selected a few headers that, per the RFC convention, are unique in an email. For instance, the "From" header cannot be present twice.
These headers will be present under the `headers` key, as either a string or a dict.
Other headers are added as a list, in case they are multiple.

The order of the headers is kept (the first Received will be the first in the list)

Here is the list of headers that will not yield a list of elements:

 * subject
 * from
 * date
 * sender
 * message-id
 * mime-version
 * return-path
 * delivered-to
 * x-forwarding-service
 * feedback-id


## Support

If you find an issue, please open a support requests, or even better, a Pull Requests :)


Thank you!
# Needed to import mailparse from parent directory
import sys
sys.path.insert(0, '../../')

# Standard import
from mailparse import EmailDecode
import json

decoded = EmailDecode.open('./sample.complete.eml')

"""
It's also possible to do

```
with open('./sample.eml', 'rb') as f:
    decoded = EmailDecode.load(f.read())

"""

print(json.dumps(decoded, indent=4))

"""

Outputs:
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
"""
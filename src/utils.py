# -*- config:utf-8 -*-

"""Miscellaneous utilities."""

__all__ = (
    'EMAIL_HEADERS',
    'NOT_HEADERS',
    'SINGLE_HEADERS',
    'normalize_key'
)

NOT_HEADERS = ('subject', 'from', 'to', 'cc', 'bcc', 'return-path', 'date', 'sender', 'message-id')
SINGLE_HEADERS = ('subject', 'from', 'date', 'sender', 'message-id', 'mime-version', 'return-path', 'delivered-to', 'x-forwarding-service', 'feedback-id')
EMAIL_HEADERS = ('from', 'return-path', 'to', 'cc', 'bcc', 'delivered-to', 'sender', 'reply-to')

def normalize_keys(key):
    normalized = []
    for x in key.lower().split('-'):
        if x in ('arc', 'dkim', 'spf'):
            normalized.append(x.upper())
        else:
            normalized.append('{0}{1}'.format(x[0:1].upper(), x[1:]))

    return '-'.join(normalized)

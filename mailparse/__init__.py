# -*- config:utf-8 -*-

from mailparse.__version__ import __version__
from mailparse.decoder import EmailDecode
from mailparse.encoder import EmailEncode

__all__ = (
    '__version__',
    'EmailDecode',
    'EmailEncode'
)

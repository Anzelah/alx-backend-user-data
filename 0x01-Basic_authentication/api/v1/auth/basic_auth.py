#!/usr/bin/env python3
"""Inherits the Auth class"""

from api.v1.auth.auth import Auth
import re
from base64 import b64decode


class BasicAuth(Auth):
    """Processes the basis authentication scheme using base64 encoding
    """
    def __init__(self):
        """Initialize instances of the class
        """
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the encoded Base64 part of the
        Authorization header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic'):
            return None
        encoding = authorization_header[5:].strip()
        return encoding

    def decode_base64_authorization_header(self, base64_
                                           authorization_header: str) -> str:
        """Returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            # Check if encoded-string is a valid base64 strings
            pattern =
            r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$'
            if not re.match(pattern, base64_authorization_header):
                return None
            # Decode encoded string to bytes then decode to string
            base64_bytes = b64decode(base64_authorization_header)
            decoded_str = base64_bytes.decode('utf-8')

            return decoded_str
        except Exception as err:
            return str(err)

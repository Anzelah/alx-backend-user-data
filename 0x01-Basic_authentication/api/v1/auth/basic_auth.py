#!/usr/bin/env python3
"""Inherits the Auth class"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Processes the basis authentication scheme using base64 encoding
    """
    def __init__(self):
        """Initialize instances of the class
        """
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return the Base64 part of the
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

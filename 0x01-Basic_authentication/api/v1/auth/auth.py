#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth():
    """A class to manage the API authentication
    """
    def __init__(self):
        """Initialize instances of the class"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        A public method for authentication
        """
        if excluded_paths is None or [] and path is None:
            return True
        if path not in excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False


    def authorization_header(self, request=None) -> str:
        """Public method for basic authenticatioon
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A public method for identifying the current user
        """
        return None

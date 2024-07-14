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
        if path is None:
            return True
        if excluded_paths is None or []:
            return True
        if path in excluded_paths:
            return False

        # check if in the list of strings(even paths without /)
        for i in excluded_paths:
            if i.startswith(path):
                return False
            if path.startswith(i[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method for basic authentication
        to validate all the requests
        """
        if request is None:
            return None
        header = request.headers
        if 'Authorization' not in header:
            return None
        return header['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """A public method for identifying the current user
        """
        return None

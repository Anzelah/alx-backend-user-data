#!/usr/bin/env python3
"""Session-based authetication"""

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """A class that implements the session-based authentication
    """
    user_id_by_session_id = {}
    # SessionAuth1.user_id_by_session_id()
    def __init__(self):
        """initialize class instances"""
        pass

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        self.session_id = str(uuid4())
        self.user_id_by_session_id = {
                self.session_id: user_id
                }
        return self.session_id

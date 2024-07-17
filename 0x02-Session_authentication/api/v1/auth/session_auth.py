#!/usr/bin/env python3
"""Session-based authetication"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """A class that implements the session-based authentication
    """
    user_id_by_session_id = {}  # maps session id to user id
    # SessionAuth1.user_id_by_session_id()

    def __init__(self):
        """initialize class instances"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a user's id based on the session id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        userId = self.user_id_by_session_id.get(session_id)
        return userId

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value. Its an overload.
        """
        sessionId = self.session_cookie(request)
        userId = self.user_id_for_session_id(sessionId)
        usr = User()
        user = usr.get(userId)
        # print(self.user_id_for_session_id(sessionId))
        return user

    def destroy_session(self, request=None):
        """Logout/destroy the users session
        """
        if request is None:
            return False
        sessionId = self.session_cookie(request)
        if sessionId is None:
            return False
        userId = self.user_id_for_session_id(sessionId)
        if not userId:
            return False
        del self.user_id_by_session_id[sessionId]
        return True

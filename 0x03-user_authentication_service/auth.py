#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> str:
    """Hash passwords and return bytes"""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _generate_uuid(self) -> str:
        """Return a string representation of a new UUID
        """
        return str(uuid.uuid4())

    def register_user(self, email: str, password: str) -> User:
        """Register and save user in database, then return the user object.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists" .format(user.email))
            return user
        except NoResultFound:
            hashed_pw = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pw)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate the users password with bcrypt.
        If it returns true, it meas password is validated
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except Exception:
            return False

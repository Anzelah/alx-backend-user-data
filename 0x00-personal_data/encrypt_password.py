#!/usr/bin/env python3
"""Encrypt passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function expects one string argument(the password);
    and returns a salted, hashed password, which is a byte string.

    Use the bcrypt package to perform the hashing.
    """
    hashed = bcrypt.hashpw(b'password', bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.
    It takes two arguments: a hashed password in bytes, and a password string.
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False

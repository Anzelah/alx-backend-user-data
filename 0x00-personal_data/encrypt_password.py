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

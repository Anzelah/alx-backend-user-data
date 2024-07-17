#!/usr/bin/env python3
"""Handles all Session auth views"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
import os
from typing import Response


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_login() -> Response:
    """Create a session to login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email is '':
        return jsonify({"error": "email missing"}), 400
    if not password or password is '':
        return jsonify({"error": "password missing"}), 400

    # usr = User()
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    valid_password = User.is_valid_password(user, password)
    if not valid_password:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    sessionId = auth.create_session(user.id)
    cookie_name = os.getenv('SESSION_NAME')
    resp = jsonify(User.to_json(user))
    resp.set_cookie(cookie_name, sessionId)

    return resp

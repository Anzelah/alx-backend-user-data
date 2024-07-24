#!/usr/bin/env python3
"""Basic Flask app
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
import requests
from db import DB

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index():
    """Message to be displayed on homepage
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register users
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": user.email,
            "message": "user created"
            })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Log in to the site
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    sessionId = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', sessionId)
    return response


@app.route('/sessions', methods=['DELETE'])
def delete_sessions():
    """Delete the sessions
    """
    sessionId = request.form.get('session_id')

    user = AUTH.get_user_from_session_id(sessionId)
    if not user:
        return 403
    AUTH.destroy_session(user.id)
    redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

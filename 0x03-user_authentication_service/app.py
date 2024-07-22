#!/usr/bin/env python3
"""Basic Flask app
"""

from flask import Flask, jsonify, request, abort
from auth import Auth
import requests
from db import DB

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def hello_world():
    """Message to be displayed on homepage
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register users
    """
    email = request.form['email']
    password = request.form['password']
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
    email = request.form['email']
    password = request.form['password']
    log_in = AUTH.valid_login(email, password)
    if log_in is False:
        abort(401)
    AUTH.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

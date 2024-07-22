#!/usr/bin/env python3
"""Basic Flask app
"""

from flask import Flask, jsonify, request
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
        if user:
            raise ValueError
        return jsonify({
            "email": user.email,
            "message": "user created"
            })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

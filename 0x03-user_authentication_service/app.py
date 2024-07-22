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
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
        if user:
            raise Exception
        new_user = AUTH.register_user(email, password)
        payload = {"email": "{new_user.email}",
                   "message": "user created"
                   }
        return payload.json()
    except Exception:
        payload = ({"message": "email already registered"})
        return jsonify(payload), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

#!/usr/bin/env python3
"""Basic Flask app
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    """Message to be displayed on homepage
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

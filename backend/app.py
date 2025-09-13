# backend/app.py

from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv 
import json

load_dotenv()


app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return " Please got to /test-openrouter to test OpenRouter API."

@app.route("/test-openrouter", methods=["GET"])
def test_openrouter_key():
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "Please set the OPENROUTER_API_KEY environment variable"}), 400

    response = requests.get(
        url="https://openrouter.ai/api/v1/key",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    )

    print(json.dumps(response.json(), indent=2))

    # If status code is not 200, return error details
    if response.status_code != 200:
        return jsonify({
            "error": "Failed to connect to OpenRouter API",
            "status_code": response.status_code,
            "response": response.text
        }), response.status_code

    # Parse JSON response
    data = response.json().get("data", {})

    return jsonify({
        "message": "Successfully connected to OpenRouter API!",
        "label": data.get("label"),
        "used": data.get("usage"),
        "limit_remaining": data.get("limit_remaining"),
        "is_free_tier": data.get("is_free_tier"),
    })

if __name__ == "__main__":
    app.run(debug=True)

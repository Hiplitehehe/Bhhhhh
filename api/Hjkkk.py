from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

# Get sensitive data from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URL = "https://oauth2.googleapis.com/token"

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/refresh', methods=['POST'])
def refresh_access_token():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({"error": "Refresh token is required"}), 400

    try:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(TOKEN_URL, data=data)
        logging.debug(f"Response from Google: {response.status_code} {response.text}")  # Logging

        if response.status_code == 400:
            return jsonify({"error": "Bad Request", "details": response.json()}), 400

        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to refresh access token: {e}")
        return jsonify({"error": "Failed to refresh access token", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

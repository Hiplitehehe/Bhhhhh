from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "790695082520-7pk2liv3qaca2f7uieqr4eig55k2shre.apps.googleusercontent.com"
CLIENT_SECRET = "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"
TOKEN_URL = "https://oauth2.googleapis.com/token"

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
        print("Response from Google:", response.status_code, response.text)  # Debugging

        if response.status_code == 400:
            return jsonify({"error": "Bad Request", "details": response.json()}), 400

        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to refresh access token", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

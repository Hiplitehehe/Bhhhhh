import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')  # Get the authorization code

    data = {
        'code': code,
        'client_id': '790695082520-7pk2liv3qaca2f7uieqr4eig55k2shre.apps.go>
        'client_secret': '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',
        'redirect_uri': 'http://localhost:3000/oauth2callback',
        'grant_type': 'authorization_code'
    }

    # Exchange the authorization code for tokens
    response = requests.post('https://oauth2.googleapis.com/token', data=da>
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')

        # Store the tokens securely (e.g., in a session, database)
        print('Access Token:', access_token)
        print('Refresh Token:', refresh_token)

        return 'OAuth 2.0 flow completed. Tokens received!'
    else:
        return 'Failed to exchange code for tokens', 500

if __name__ == '__main__':
    app.run(port=3000)

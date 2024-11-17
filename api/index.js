const express = require('express');
const axios = require('axios');
const querystring = require('querystring');
const app = express();
const port = 5000;

// Your OAuth 2.0 credentials
const CLIENT_ID = '790695082520-7pk2liv3qaca2f7uieqr4eig55k2shre.apps.googleusercontent.com'; // Replace with your Client ID
const CLIENT_SECRET = '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'; // Replace with your Client Secret
const REDIRECT_URI = 'http://localhost:5000/oauth2callback'; // This must match the one in your Google Console

// Step 1: Redirect user to Google for authorization
app.get('/auth', (req, res) => {
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?${querystring.stringify({
        scope: 'https://www.googleapis.com/auth/drive.file', // Adjust scope as necessary
        access_type: 'offline',
        response_type: 'code',
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
    })}`;
    res.redirect(authUrl);
});

// Step 2: Handle the redirect from Google and exchange code for tokens
app.get('/oauth2callback', async (req, res) => {
    const code = req.query.code; // Extract the authorization code from the query params

    if (!code) {
        return res.status(400).send('Missing authorization code');
    }

    try {
        // Step 3: Exchange the authorization code for access and refresh tokens
        const response = await axios.post('https://oauth2.googleapis.com/token', querystring.stringify({
            code: code,
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            redirect_uri: REDIRECT_URI,
            grant_type: 'authorization_code',
        }));

        // Tokens are returned in the response
        const { access_token, refresh_token, expires_in } = response.data;

        console.log('Access Token:', access_token);
        console.log('Refresh Token:', refresh_token);
        console.log('Expires In:', expires_in);

        // Send the tokens back to the user (or store them securely in your app)
        res.json({
            access_token,
            refresh_token,
            expires_in
        });

    } catch (error) {
        console.error('Error exchanging code for tokens:', error.response ? error.response.data : error.message);
        res.status(500).send('Failed to exchange code for tokens');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

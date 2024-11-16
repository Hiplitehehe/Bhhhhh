require('dotenv').config();  // Load environment variables from .env file

const express = require('express');
const axios = require('axios');
const querystring = require('querystring');
const app = express();
const port = 3090;

// Your OAuth 2.0 credentials from environment variables
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const REDIRECT_URI = process.env.REDIRECT_URI;  // Make sure this matches with Google Cloud Console

// Step 1: Redirect user to Google for authorization
app.get('/auth', (req, res) => {
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?${querystring.stringify({
        scope: 'https://www.googleapis.com/auth/drive.file',
        access_type: 'offline',
        response_type: 'code',
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI, // This should match the redirect URI in Google Cloud Console
    })}`;
    res.redirect(authUrl);
});

// Step 2: Handle the redirect from Google and exchange code for tokens
app.get('/oauth2callback', async (req, res) => {
    const code = req.query.code; // Extract the authorization code from the query params

    try {
        // Exchange the authorization code for an access token and refresh token
        const response = await axios.post('https://oauth2.googleapis.com/token', querystring.stringify({
            code: code,
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            redirect_uri: REDIRECT_URI, // This should match the redirect URI in Google Cloud Console
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
        console.error('Error exchanging code for tokens:', error);
        res.status(500).send('Failed to exchange code for tokens');
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

# Google OAuth Setup for Amazon Bedrock AgentCore

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

## Step 2: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - App name: "Customer Support Assistant"
   - User support email: Your email
   - Developer contact information: Your email
4. Add scopes:
   - `https://www.googleapis.com/auth/calendar`
5. Add test users (your email address)

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Set name: "Customer Support AgentCore"
5. **CRITICAL**: Add Authorized redirect URIs:
   ```
   https://bedrock-agentcore.us-west-2.amazonaws.com/identities/oauth2/callback
   ```
6. Download the JSON credentials file

## Step 4: Update Your Credentials File

Save the downloaded JSON file as `credentials.json` in the project root with this structure:

```json
{
  "web": {
    "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uris": [
      "https://bedrock-agentcore.us-west-2.amazonaws.com/identities/oauth2/callback"
    ]
  }
}
```

## Step 5: Verify Configuration

The redirect URI must exactly match:
- **Correct**: `https://bedrock-agentcore.us-west-2.amazonaws.com/identities/oauth2/callback`
- **Wrong**: `https://bedrock-agentcore.us-west-2.amazonaws.com/identities/oauth2/authorize`

## Troubleshooting

If you get "Error 403: access_denied":
1. Verify the redirect URI is exactly as shown above
2. Ensure your app is in "Testing" mode with your email as a test user
3. Check that Google Calendar API is enabled
4. Make sure the OAuth consent screen is properly configured
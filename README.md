# MSAL Python Popup Authentication

This Flask application demonstrates Microsoft Entra ID (Azure AD) authentication using MSAL Python with a popup-based login flow.

## Setup

1. Create an app registration in Microsoft Entra ID (Azure AD):
   - Go to Azure Portal > Microsoft Entra ID > App registrations
   - Create a new registration
   - Set the redirect URI to `http://localhost:5000/getAToken`
   - Note down the Client ID and Tenant ID
   - Create a client secret and note it down

2. Create a `.env` file in the project root with the following content:
```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
TENANT_ID=your_tenant_id
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Features

- Popup-based authentication flow
- Token caching
- Session management
- Modern UI with Tailwind CSS
- Automatic popup window management

## Security Notes

- The application uses secure session management
- Tokens are cached securely
- Environment variables are used for sensitive configuration
- HTTPS is recommended for production deployment

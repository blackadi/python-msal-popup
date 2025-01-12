import os
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import msal
from dotenv import load_dotenv
import jwt
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Azure AD Configurations
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
SCOPE = ["User.Read"]  # Add more scopes as needed
REDIRECT_PATH = "/getAToken"

# # MSAL configuration
# cache = msal.SerializableTokenCache()

# # Load the cached token
# if os.path.exists("token_cache.bin"):
#     with open("token_cache.bin", "r") as file:
#         cache.deserialize(file.read())

# Create MSAL application
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
    # token_cache=cache
)

# def save_cache(cache):
#     if cache.has_state_changed:
#         with open("token_cache.bin", "w") as file:
#             file.write(cache.serialize())

def get_token_from_cache(scope=None):
    accounts = msal_app.get_accounts()
    if accounts:
        result = msal_app.acquire_token_silent(scope or SCOPE, account=accounts[0])
        return result
    return None

def get_username():
    accounts = msal_app.get_accounts()
    for a in accounts:
        print(a["username"])
    if accounts:
        return accounts[0]["username"]
    return None

@app.route("/")
def index():
    token = get_token_from_cache()
    if not token:
        return render_template("index.html", user=None)
    
    # Get user info from token
    user_info = {
        "name": "User",
        "username": get_username(),
        "token": token.get("access_token", "")
    }

    try:
        # Decoding the JWT token
        access_token = token.get("access_token", "")
        decoded_claims = jwt.decode(access_token, options={"verify_signature": False})  # Do not verify signature
        user_info["name"] = decoded_claims.get("name", "")

    except jwt.DecodeError:
        decoded_claims = "Invalid token format."
        
    print(user_info)
    return render_template("index.html", user=user_info, access_token=access_token, decoded_claims=decoded_claims)

@app.route("/login")
def login():
    # Generate the auth URL for the popup
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for("get_token", _external=True),
        response_type="code",
        prompt="select_account"
    )
    return jsonify({"auth_url": auth_url})

@app.route(REDIRECT_PATH)
def get_token():
    code = request.args.get('code')
    if code:
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=url_for("get_token", _external=True)
        )
        if "error" in result:
            return render_template("auth_error.html", result=result)
        
        #save_cache(cache)
        return render_template("auth_complete.html")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    accounts = msal_app.get_accounts()
    if accounts:
        msal_app.remove_account(accounts[0])
        #save_cache(cache)
    session.clear()
    return redirect(url_for("index"))

@app.route("/check_auth")
def check_auth():
    token = get_token_from_cache()
    return jsonify({"authenticated": token is not None})

@app.route("/iframe")
def iframe():
    return render_template("iframe.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

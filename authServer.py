#!/usr/bin/env python3
import os
import json
import threading
import secrets
import requests
import base64
import hashlib
import webbrowser
from flask import Flask, request
from dotenv import load_dotenv

# ==============================
# 1. Load environment variables
# ==============================
load_dotenv()
client_id = os.getenv("MAL_CLIENT_ID")
client_secret = os.getenv("MAL_CLIENT_SECRET")

if not client_id or not client_secret:
    raise SystemExit("❌ Please set MAL_CLIENT_ID and MAL_CLIENT_SECRET in your .env file.")

# ==============================
# 2. PKCE Helper
# ==============================
def generate_code_verifier():
    return secrets.token_urlsafe(64)

def generate_code_challenge(verifier: str):
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print("PKCE verifier:", code_verifier)
print("PKCE challenge:", code_challenge)

# ==============================
# 3. Flask mini server
# ==============================
app = Flask(__name__)
auth_code = None

@app.route("/")
def callback():
    global auth_code
    auth_code = request.args.get("code")
    return (
        "<h1>✅ Authorization successful</h1>"
        "<p>You may now close this tab.</p>"
    )

def start_server():
    app.run(port=8080)

# ==============================
# 4. Authorization URL
# ==============================
redirect_uri = "http://localhost:8080/"

auth_url = (
    "https://myanimelist.net/v1/oauth2/authorize"
    "?response_type=code"
    f"&client_id={client_id}"
    f"&code_challenge={code_challenge}"
    f"&code_challenge_method=S256"
    f"&redirect_uri={redirect_uri}"
)

# ==============================
# 5. Exchange code for token
# ==============================
def generate_new_token(authorisation_code: str, verifier: str):
    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": authorisation_code,
        "code_verifier": verifier,
        "redirect_uri": redirect_uri,
    }

    print("\nSending token request with:")
    print(json.dumps(data, indent=4))

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("\n❌ TOKEN EXCHANGE FAILED")
        print("Status:", response.status_code)
        print("Response:", response.text)
        raise SystemExit()

    token = response.json()
    with open("token.json", "w") as f:
        json.dump(token, f, indent=4)

    print("✅ Token saved to token.json")
    return token

# ==============================
# 6. Fetch user info
# ==============================
def print_user_info(access_token: str):
    url = "https://api.myanimelist.net/v2/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("\n❌ FAILED FETCHING USER INFO")
        print(response.text)
        return

    user = response.json()
    print(f"\n👋 Hello, {user['name']}! Auth successful.")

# ==============================
# 7. Run end-to-end
# ==============================
if __name__ == "__main__":
    print("🚀 Starting local auth server on port 8080...")
    threading.Thread(target=start_server, daemon=True).start()

    print("\n🌐 Opening MyAnimeList login page...")
    print(f"URL:\n{auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for authorization code...")
    while not auth_code:
        pass  # wait for Flask callback

    print(f"\n✅ Authorization code received: {auth_code}")

    token = generate_new_token(auth_code, code_verifier)
    print_user_info(token["access_token"])

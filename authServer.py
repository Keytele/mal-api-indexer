#!/usr/bin/env python3
import os
import json
import threading
import secrets
import requests
import webbrowser
from flask import Flask, request
from dotenv import load_dotenv

# ==============================
#  1. Load environment variables
# ==============================
load_dotenv()
client_id = os.getenv("MAL_CLIENT_ID")
client_secret = os.getenv("MAL_CLIENT_SECRET")

if not client_id or not client_secret:
    raise SystemExit("❌ Please set MAL_CLIENT_ID and MAL_CLIENT_SECRET in your .env file.")

# ==============================
#  2. PKCE helper
# ==============================
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

# ==============================
#  3. Flask mini server
# ==============================
app = Flask(__name__)
auth_code = None

@app.route("/")
def callback():
    global auth_code
    auth_code = request.args.get("code")
    return (
        "<h1>✅ Authorization Successful!</h1>"
        "<p>You can close this window and return to the terminal.</p>"
    )

def start_server():
    app.run(port=8080)

# ==============================
#  4. Build authorization URL
# ==============================
redirect_uri = "http://localhost:8080/"
auth_url = (
    f"https://myanimelist.net/v1/oauth2/authorize"
    f"?response_type=code"
    f"&client_id={client_id}"
    f"&code_challenge={code_challenge}"
    f"&redirect_uri={redirect_uri}"
)

# ==============================
#  5. Exchange code for token
# ==============================
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorisation_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    response = requests.post(url, data)
    response.raise_for_status()

    token = response.json()
    with open("token.json", "w") as f:
        json.dump(token, f, indent=4)

    print("✅ Token generated and saved to token.json")
    return token

# ==============================
#  6. Fetch user info
# ==============================
def print_user_information(access_token: str):
    url = "https://api.myanimelist.net/v2/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    user = response.json()
    print(f"\n👋 Hello, {user['name']}! Your MAL authentication is successful.")

# ==============================
#  7. Run full flow
# ==============================
if __name__ == "__main__":
    print("🚀 Starting local auth server on port 8080...")
    threading.Thread(target=start_server, daemon=True).start()

    print("\n🌐 Opening MyAnimeList authorization page...")
    print(f"If your browser doesn't open, visit this URL manually:\n{auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for authorization code...")
    while not auth_code:
        pass  # wait until Flask receives the code

    print(f"\n✅ Authorization code received: {auth_code}")

    token = generate_new_token(auth_code, code_verifier)
    print_user_information(token["access_token"])

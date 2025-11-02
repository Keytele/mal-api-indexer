#!/usr/bin/env python3

import os
import sys
import argparse
import json
import secrets
from dotenv import load_dotenv
import requests  # pip install requests

load_dotenv()

client_id = os.getenv('MAL_CLIENT_ID')
client_secret = os.getenv('MAL_CLIENT_SECRET')

def get_new_code_verifier() -> str: #This function is to generate a Code Verifier and Code Challenge with PKCE
    token = secrets.token_urlsafe(100)
    return token[:128]

code_verifier = code_challenge = get_new_code_verifier()

print(len(code_verifier))
print(code_verifier)

def print_new_authorisation_url(code_challenge: str):
    global client_id
    
    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={client_id}&code_challenge={code_challenge}'

    print(f'Authorise your application by access the link provided: {url}\n')
    
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global client_id, client_secret
    
    url = 'https://myanimelist.net/v1/oath2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(url, data)
    response.raise_for_status() # Check whether the request contains errors and will raise a status
    
    token = response.json()
    response.close()
    
    print('Token generated successfully!')
    
    with open('token.json', 'w') as file:
        json.dump(token, file, indent = 4)
        print('Token is saved in "token.json"')
        
    return token

def print_user_information(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers = {
        'Authorization': f'Bearer {access_token}'
    })
    
    response.raise_for_status()
    user = response.json()
    response.close()
    
    print(f"\n>>> Greetings {user['name']}! <<<")
    
if __name__ == '__main__':
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge)
    
    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    token = generate_new_token(authorisation_code, code_verifier)
    
    print_user_information(token['access_token'])
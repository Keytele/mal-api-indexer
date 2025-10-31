#!/usr/bin/env python3

import os
import sys
import argparse
from dotenv import load_dotenv
import requests  # pip install requests

load_dotenv()

def get_anime():
    BASE_URL = "https://api.myanimelist.net/v2/anime"
    try:
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
        
    
    """
    TODOs (do them in order):
    1) Read MAL_CLIENT_ID from environment (os.environ.get).
    2) If missing, print a short message telling the user how to set it and exit(1).
    3) Build headers = {"X-MAL-CLIENT-ID": <client_id>}.
    4) Use requests.get(BASE_URL + path, params=params, headers=headers, timeout=10).
    5) If response status code not 2xx, print status + body and exit(1).
    6) Return response.json().
    """

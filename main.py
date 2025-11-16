# Import libraries

import json
import os
import argparse
import requests
from dotenv import load_dotenv

load_dotenv() # Load environment variables

CLIENT_ID = os.getenv("MAL_CLIENT_ID")
if not CLIENT_ID:
    raise RuntimeError("No Client ID found in environment variables, program will terminate!")

BASE_URL = "https://api.myanimelist.net/v2/anime/season/{year}/{season}?{limit}"


# Calling the MAL API

def load_token():
    global data

    try:
        with open('token.json', 'r') as file:
            data = json.load(file)
    except:
        print("token.json missing. Run AuthServer.py.")
        exit()

    token = data.get("access_token")
    expires_in = data.get("expires_in", 0)

    # If expired, refresh the token
    if expires_in <= 0:
        token = refresh_access_token()

    return token
        
def search_anime(year, season, limit): # Function to search anime by year, season, and limit along with handling request errors
    url = BASE_URL.format(year = year, season = season.lower(), limit = limit)
    
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID,
        "Authorization": f"Bearer {load_token()}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Request failed:", response.status_code, response.text)
        exit()
        
    return response.json()


def refresh_access_token():
    url = "https://myanimelist.net/v1/oauth2/token"
    
    refresh_token = data.get("refresh_token")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print("Failed to refresh token:", response.text)
        exit()

    new_data = response.json()

    # Save updated token.json
    with open("token.json", "w") as f:
        json.dump(new_data, f, indent=4)

    print("✔ Access token refreshed")
    return new_data["access_token"]



# Setting up argument parser using Argparse and initialising the CLI

parser = argparse.ArgumentParser(description= "MAL Search Program")
parser.add_argument('-y', '--year', type=int, required=True, help="Select the year of anime")
parser.add_argument('-s', '--season', type=str, required=True, choices=['spring', 'summer', 'autumn', 'winter'], help="Select the season eg. Spring, Summer")
parser.add_argument('-l', '--limit', type=int,  required=True, default=10,help="Select the limit of anime to be displayed")

args = parser.parse_args()

# Running the search

result = search_anime(args.year, args.season, args.limit)

# Display results
print("\n=== Anime Search Results ===\n")

for anime in result.get("data", []):
    node = anime.get("node", {})
    print(f"Title: {node.get('title')}")
    print(f"ID: {node.get('id')}")
    print(f"Link: https://myanimelist.net/anime/{node.get('id')}")
    print("-" * 40)

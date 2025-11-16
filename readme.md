# MAL Seasonal Anime Search CLI (IN-PROGRESS)

A Python command-line application that authenticates with the MyAnimeList (MAL) API using OAuth2 + PKCE and allows you to search anime by year, season, and limit using the /anime/season endpoint.

This project contains two main files:
- authServer.py → Handles MAL OAuth2 PKCE authentication (generates access & refresh tokens)
- main.py → CLI application for searching seasonal anime


## Installation

Install required dependencies

```bash
 pip install -r requirements.txt
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```
MAL_CLIENT_ID=your_client_id_here
MAL_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:8080/callback
```
Replace the values above

To setup a MAL API App and obtain your client details: [LINK]



## Token Generation

Before using the CLI, you must authenticate with MAL using OAuth2 PKCE.

1. Run the authentication server

```
python authServer.py
```

2. Approve the request

You will be redirected to MAL to approve the application.

3. After allowing the application access, it will redirect you to your local 8080 server
It will automatically:
- Receive the authorisation code
- Exchange it for an access token
- Generate a refresh token
- Save it into token.json

## Token.json

The file will contain:

```
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": xxx,
  "token_type": "Bearer"
}
```

- The CLI will read this file to authenticate requests
- If ```access_token``` expires, you will need to get a new token
- If ```token.json``` is not present, the program will not run



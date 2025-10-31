#!/usr/bin/env python3

import os
import sys
import argparse
import requests  # pip install requests

BASE_URL = "https://api.myanimelist.net/v2"

def api_get(path: str, params: dict):
    
    response = requests.get(BASE_URL)
    print(response.json)
    
    """
    TODOs (do them in order):
    1) Read MAL_CLIENT_ID from environment (os.environ.get).
    2) If missing, print a short message telling the user how to set it and exit(1).
    3) Build headers = {"X-MAL-CLIENT-ID": <client_id>}.
    4) Use requests.get(BASE_URL + path, params=params, headers=headers, timeout=10).
    5) If response status code not 2xx, print status + body and exit(1).
    6) Return response.json().
    """
    # write your code here
    pass


def cmd_search(args: argparse.Namespace):
    """
    TODOs:
    1) Build params with keys: "q", "limit", "fields".
    2) Call api_get("/anime", params).
    3) The payload shape is typically: {"data": [{"node": {...}}, ...]}
       Extract each item’s "node" then "title" and "id".
    4) Print a short list like: "• Title (id: 123, mean: 8.1)".
       Only show mean if present in the node.
    """
    # write your code here
    pass


def cmd_season(args: argparse.Namespace):
    """
    TODOs:
    1) Build the path f"/anime/season/{args.year}/{args.season}".
    2) Build params with "limit", "offset", "fields".
    3) Call api_get(path, params).
    4) Print items same style as search (title/id/mean).
    5) (Later) if args.all_pages is True, loop while there's a 'next' page
       (hint: response may include 'paging': {'next': '...offset=...'}).
       For now, just print the first page.
    """
    # write your code here
    pass


def build_parser() -> argparse.ArgumentParser:
    """
    TODOs:
    1) Create an ArgumentParser with a short description.
    2) Add subparsers and two subcommands: 'search' and 'season'.
    3) For 'search':
       - required positional 'query'
       - optional '--limit' (int, default 5)
       - optional '--fields' (default "id,title,mean,rank")
       - set_defaults(func=cmd_search)
    4) For 'season':
       - positional 'year' (int)
       - positional 'season' (choices: winter, spring, summer, fall)
       - optional '--limit' (int, default 10)
       - optional '--offset' (int, default 0)
       - optional '--fields' (default "id,title,mean,rank,start_season")
       - optional '--all-pages' (store_true)
       - set_defaults(func=cmd_season)
    5) Return the parser.
    """
    # write your code here
    pass


def main():
    """
    TODOs:
    1) parser = build_parser()
    2) args = parser.parse_args()
    3) Call args.func(args)
    """
    # write your code here
    pass


if __name__ == "__main__":
    main()


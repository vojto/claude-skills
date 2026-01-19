#!/usr/bin/env python3
"""
WHOOP OAuth Setup Script

This script performs a one-time OAuth flow to obtain access and refresh tokens
for the WHOOP API. The tokens are saved to .whoop_credentials.json for future use.

Usage:
    python setup.py

Prerequisites:
    pip install whoopy python-dotenv
"""

import json
import os
import sys
from pathlib import Path

# Change to script directory so .env and credentials are found
os.chdir(Path(__file__).parent)

try:
    from dotenv import load_dotenv
    from whoopy import WhoopClient
except ImportError:
    print("Missing dependencies. Installing...")
    os.system(f"{sys.executable} -m pip install whoopy python-dotenv")
    from dotenv import load_dotenv
    from whoopy import WhoopClient

def main():
    # Load credentials from .env
    load_dotenv()

    client_id = os.getenv("WHOOP_CLIENT_ID")
    client_secret = os.getenv("WHOOP_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: WHOOP_CLIENT_ID and WHOOP_CLIENT_SECRET must be set in .env")
        sys.exit(1)

    print("=" * 60)
    print("WHOOP OAuth Setup")
    print("=" * 60)
    print()
    print("This will open your browser to authenticate with WHOOP.")
    print("After granting access, you'll be redirected to localhost.")
    print()
    print("Press Enter to continue...")
    input()

    try:
        # Run the OAuth flow - this opens a browser
        client = WhoopClient.auth_flow(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:1234"
        )

        # Save tokens to credentials file (including client credentials)
        credentials_file = Path(__file__).parent / ".whoop_credentials.json"
        client.save_token(str(credentials_file))

        # Add client_id and client_secret to the saved credentials
        with open(credentials_file) as f:
            creds = json.load(f)
        creds["client_id"] = client_id
        creds["client_secret"] = client_secret
        with open(credentials_file, "w") as f:
            json.dump(creds, f, indent=2)

        print()
        print("=" * 60)
        print("Success!")
        print("=" * 60)
        print(f"Credentials saved to: {credentials_file}")
        print()

        # Test the connection by fetching user profile
        print("Testing connection...")
        user = client.user.get_profile()
        print(f"Connected as: {user.first_name} {user.last_name}")
        print(f"Email: {user.email}")
        print()
        print("Setup complete! You can now use the WHOOP skill.")

    except Exception as e:
        print(f"Error during OAuth flow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

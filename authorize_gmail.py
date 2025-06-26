from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    # Load credentials from file
    if os.path.exists('token.json'):
        print("token.json already exists.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
        print("token.json generated successfully.")

if __name__ == '__main__':
    main()

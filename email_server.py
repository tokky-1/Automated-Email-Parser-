# API integration
#Purpose: Handles connection to email (gmail API)
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

#gets and saves user credentials
def authenticate():
    creds = None
    #checks for saved tokens
    if os.path.exists("token.json"): 
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # checks for none or if it has expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # refreshes
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True) # opens the browser login

        with open("token.json", "w") as token:
            token.write(creds.to_json()) # saves the credentials

    return creds

def fetch_emails():
    creds = authenticate()
    #creates api client
    service = build("gmail", "v1", credentials=creds)

    # get the ids of the first 150 emails
    results = service.users().messages().list(
        userId="me",
        maxResults=150
    ).execute()
    messages = results.get("messages", [])
    if not messages:
        print("No emails found.")
        return []

    #prints out the emails in details
    emails = []
    for msg in messages:
        detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        emails.append(detail)

    return emails
#for test purposes only
# if __name__ == "__main__":
#     emails = fetch_emails()
#     print(f"Fetched {len(emails)} emails")
#     print(emails[0])  # prints the first raw email so you can see the structure
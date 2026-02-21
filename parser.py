#Data structuring
#Purpose: Extracts useful info from raw email data
import base64

def parse_email(raw_email):
    #holds the main content of the email
    payload = raw_email["payload"]

    #holds sender,reciever,date
    headers = payload["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    sender  = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
    date    = next((h["value"] for h in headers if h["name"] == "Date"), "Unknown")

    #converts the text version gotten from google to plain text
    body:str = ""
    parts = payload.get("parts", [])
    for part in parts:
        if part["mimeType"] == "text/plain":
            data = part["body"]["data"]
            body = base64.urlsafe_b64decode(data).decode("utf-8")
            break
    return {
        "subject": subject,
        "sender":  sender,
        "date":    date,
        "body":    body,
        "labels":  raw_email.get("labelIds", []),
    }
#for test purposes only
# if __name__ == "__main__":
#     from email_server import fetch_emails
    
#     raw_emails = fetch_emails()
#     parsed = parse_email(raw_emails[0])
#     print(parsed)
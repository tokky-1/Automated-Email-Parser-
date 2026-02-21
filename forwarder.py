# Forwarding logic
# Purpose: Forwards emails based on user-defined rules

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_server import authenticate
from googleapiclient.discovery import build


def get_service():
    creds = authenticate()
    return build("gmail", "v1", credentials=creds)

def matches_rule(email: dict, rule: dict) -> bool:
    sender  = email.get("sender", "").lower()
    subject = email.get("subject", "").lower()
    body    = email.get("body", "").lower()
    category = email.get("category", "")

    match_type = rule["type"]
    value      = rule["value"].lower()

    if match_type == "category":
        return category == value.upper()
    elif match_type == "sender":
        return value in sender
    elif match_type == "subject":
        return value in subject
    elif match_type == "body":
        return value in body

    return False

def forward_email(service, email: dict, forward_to: str) -> bool:
    try:
        msg = MIMEMultipart()
        msg["To"]      = forward_to
        msg["Subject"] = f"Fwd: {email.get('subject', '')}"

        body = (
            f"---------- Forwarded message ----------\n"
            f"From: {email.get('sender', '')}\n"
            f"Date: {email.get('date', '')}\n"
            f"Subject: {email.get('subject', '')}\n\n"
            f"{email.get('body', '')}"
        )
        msg.attach(MIMEText(body, "plain"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()
        return True

    except Exception as e:
        print(f"Failed to forward: {e}")
        return False
    
def apply_rules(emails: list, rules: list) -> list:
    service = get_service()
    log = []

    for email in emails:
        for rule in rules:
            if matches_rule(email, rule):
                success = forward_email(service, email, rule["forward_to"])
                log.append({
                    "subject":    email.get("subject"),
                    "sender":     email.get("sender"),
                    "rule_type":  rule["type"],
                    "rule_value": rule["value"],
                    "forward_to": rule["forward_to"],
                    "success":    success,
                })

    return log
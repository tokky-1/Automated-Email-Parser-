# Category logic
#Purpose: Decides which category/folder each email belongs to

#the available categories
CATEGORIES = {
    "WORK/PROFESSIONAL":    [],
    "PROMOTIONS/MARKETING": [],
    "SOCIALS":              [],
    "UPDATES":              [],
    "SPAM":                 [],
    "UNCATEGORIZED":        [],
}

# Emails sent from any of these domains will be classified as WORK/PROFESSIONAL
WORK_DOMAINS = [
    "babcock.edu.ng",
    "gov.ng",
    "edu.ng",
    # add more domains here as needed
]
WORK_KEYWORDS = [
    "invoice", "meeting", "agenda", "proposal", "contract",
    "project", "deadline", "report", "schedule", "follow up",
    "follow-up", "action required", "review", "approval",
    "onboarding", "interview", "offer letter", "internship", "siwes",
]

#Gmail's own labels to categorizes emails
def categorize_email(parsed_email):    
    ## matches Gmail's label names to category names
    label_map = {
            "CATEGORY_PROMOTIONS": "PROMOTIONS/MARKETING",
            "CATEGORY_SOCIAL":     "SOCIALS",
            "CATEGORY_UPDATES":    "UPDATES",
            "CATEGORY_FORUMS":     "SOCIALS",
            "SPAM":                "SPAM",
        }
    
    # loops through the labels Gmail
    for label in parsed_email["labels"]:
            if label in label_map:
                return label_map[label]

    # categorieses email into work, by first checking the domain, then checking the content       
    sender = parsed_email.get("sender", "").lower()
    for domain in WORK_DOMAINS:
        if domain in sender:
            return "WORK/PROFESSIONAL"

    subject = parsed_email.get("subject", "").lower()
    for keyword in WORK_KEYWORDS:
        if keyword in subject:
            return "WORK/PROFESSIONAL"
    return "UNCATEGORIZED"
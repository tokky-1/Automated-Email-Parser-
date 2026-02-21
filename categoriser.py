# Category logic
#Purpose: Decides which category/folder each email belongs to

#the available categories
CATEGORIES = {
    "WORK/PROFESSIONAL":    [],
    "PROMOTIONS/MARKETING": [],
    "SOCIALS":              [],
    "SPAM":                 [],
    "UNCATEGORIZED":        [],
}

#Gmail's own labels to categorizes emails
def categorize_email(parsed_email):    
    ## matches Gmail's label names to category names
    label_map = {
            "CATEGORY_PROMOTIONS": "PROMOTIONS/MARKETING",
            "CATEGORY_SOCIAL":     "SOCIALS",
            "CATEGORY_UPDATES":    "SOCIALS",
            "CATEGORY_FORUMS":     "SOCIALS",
            "SPAM":                "SPAM",
        }
    
    # loops through the labels Gmail
    for label in parsed_email["labels"]:
            if label in label_map:
                return label_map[label]

    return "UNCATEGORIZED"
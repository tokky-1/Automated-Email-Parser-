# Pandas analysis
# Purpose: Analyze email data and generate insights

import pandas as pd

#Analyzes categorized email data and returns insights as structured data.
def analyze_emails(categorized_emails):
    """
    Args:
        categorized_emails: list of dicts with keys: 'category', 'sender', 'date'

    Returns:
        dict with keys:
            - 'emails_per_category': pd.Series
            - 'top_senders': pd.Series
            - 'emails_per_day': pd.Series
            - 'dataframe': full pd.DataFrame
    """
    if not categorized_emails:
        return None

    df = pd.DataFrame(categorized_emails)

    # Normalize date column
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df["date_only"] = df["date"].dt.date

    emails_per_category = df["category"].value_counts()
    top_senders = df["sender"].value_counts().head(10)
    emails_per_day = df["date_only"].value_counts().sort_index()

    return {
        "emails_per_category": emails_per_category,
        "top_senders": top_senders,
        "emails_per_day": emails_per_day,
        "dataframe": df,
    }
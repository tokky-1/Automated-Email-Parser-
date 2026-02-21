# Pandas analysis
# Purpose: Analyze email data and generate insights

import pandas as pd

def analyze_emails(categorized_emails):
    df = pd.DataFrame(categorized_emails)
    print(df.head())

    print("\n--- Emails per Category ---")
    print(df["category"].value_counts())

    print("\n--- Top 10 Senders ---")
    print(df["sender"].value_counts().head(10))

    print("\n--- Emails per Day ---")
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    print(df["date"].dt.date.value_counts().sort_index())
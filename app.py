# Streamlit frontend
# Purpose: The main entry point that runs everything

import streamlit as st
from email_server import fetch_emails, authenticate
from parser import parse_email
from categoriser import categorize_email, CATEGORIES
from forwarder import apply_rules
from analytics import analyze_emails
import pandas as pd
import os

st.set_page_config(
    page_title="Email Parser & Organizer",
    page_icon="📬",
    layout="wide"
)

# ── Credentials guard ─────────────────────────────────────────────────
if not os.path.exists("credentials.json"):
    st.error(
        "⚠️ **Missing `credentials.json`** — Download it from the "
        "[Google Cloud Console](https://console.cloud.google.com/) and place it "
        "in the project root folder, then refresh this page."
    )
    st.stop()

# ── Auth gate ─────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.title("📬 Email Parser & Organizer")
    st.write("Sign in with your Google account to get started.")
    if st.button("🔐 Sign in with Google", type="primary"):
        try:
            authenticate()
            st.session_state["logged_in"] = True
            st.rerun()
        except FileNotFoundError:
            st.error("⚠️ `credentials.json` not found. Please add it to the project root and refresh.")
            st.stop()
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📬 Email Parser")
    st.divider()
    max_emails = st.slider("Emails to fetch", 10, 300, 150, step=10)
    fetch = st.button("Fetch Emails", width="stretch", type="primary")
    st.divider()
    if st.button("🚪 Sign Out", width="stretch"):
        st.session_state.clear()
        if os.path.exists("token.json"):
            os.remove("token.json")
        st.rerun()

# ── Main area ─────────────────────────────────────────────────────────
st.title("📬 Email Parser & Organizer")
st.caption("Fetch, categorize and explore your Gmail inbox.")
st.divider()

if fetch:
    with st.spinner("Fetching emails..."):
        raw_emails = fetch_emails(max_results=max_emails)
        categorized_emails = []
        for raw in raw_emails:
            parsed = parse_email(raw)
            parsed["category"] = categorize_email(parsed)
            categorized_emails.append(parsed)

        df = pd.DataFrame(categorized_emails)
        st.session_state["df"] = df
        st.session_state["categorized_emails"] = categorized_emails
        st.success(f"✅ Fetched {len(df)} emails!")

if "df" in st.session_state:
    df = st.session_state["df"]

    # ── Stats row ─────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Total Emails", len(df))
    col2.metric("Unique Senders", df["sender"].nunique())
    col3.metric("Categories", df["category"].nunique())

    st.divider()

    # ── Filter + table ────────────────────────────────────────────
    categories = ["All"] + list(CATEGORIES.keys())
    selected = st.selectbox("Filter by category", categories)

    filtered_df = df if selected == "All" else df[df["category"] == selected]

    st.subheader(f"Showing {len(filtered_df)} emails")
    st.dataframe(
        filtered_df[["date", "sender", "subject", "category"]],
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # ── Analytics ─────────────────────────────────────────────────
    st.subheader("📊 Email Analytics")
    results = analyze_emails(st.session_state["categorized_emails"])

    if results:
        tab1, tab2, tab3 = st.tabs(["By Category", "Top Senders", "Emails per Day"])

        with tab1:
            st.bar_chart(results["emails_per_category"])

        with tab2:
            st.bar_chart(results["top_senders"])

        with tab3:
            st.line_chart(results["emails_per_day"])
    else:
        st.info("No analytics data available.")

    st.divider()

    # ── Rule builder ──────────────────────────────────────────────
    st.subheader("⚡ Auto-Forwarding Rules")

    col1, col2, col3 = st.columns(3)
    with col1:
        rule_type = st.selectbox("Match by", ["category", "sender", "subject", "body"])
    with col2:
        rule_value = st.text_input("Match value", placeholder="e.g. SPAM or @babcock.edu.ng")
    with col3:
        forward_to = st.text_input("Forward to", placeholder="friend@gmail.com")

    personal_message = st.text_area(
    "Personal message (optional)",
    placeholder="Add a note to include at the top of the forwarded email...",
    height=100)

    if st.button("▶ Apply Rule", type="primary"):
        if not rule_value or not forward_to:
            st.error("Please fill in both match value and forward to fields.")
        elif "@" not in forward_to or "." not in forward_to:
            st.error("Please enter a valid email address.")
        else:
            rule = [{
                "type":       rule_type,
                "value":      rule_value,
                "forward_to": forward_to,
                "personal_message": personal_message,
            }]
            with st.spinner("Applying rule..."):
                log = apply_rules(st.session_state["df"].to_dict(orient="records"), rule)
            if not log:
                st.info("No emails matched this rule.")
            else:
                st.success(f"✅ Forwarded {len(log)} emails!")
                log_df = pd.DataFrame(log)
                log_df["success"] = log_df["success"].map({True: "✅", False: "❌"})
                st.dataframe(log_df, hide_index=True, width="stretch")
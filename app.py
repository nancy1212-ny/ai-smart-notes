import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

from model import analyze_sentiment, extract_keywords, generate_smart_notes

# ----------------------------
# TITLE
# ----------------------------
st.title("AI Smart Notes from Patient Surveys")

# ----------------------------
# LOAD DATA
# ----------------------------
data = pd.read_csv("data.csv")

# ----------------------------
# INPUT SECTION
# ----------------------------
st.subheader("📝 Enter Patient Feedback")

new_feedback = st.text_input("Type feedback here")

if st.button("Add Feedback"):
    if new_feedback:
        data = pd.concat(
            [data, pd.DataFrame({"feedback": [new_feedback]})],
            ignore_index=True
        )
        data.to_csv("data.csv", index=False)
        st.success("Feedback added!")

# ----------------------------
# INSTANT ANALYSIS (🔥 NEW)
# ----------------------------
if st.button("Analyze Single Feedback"):
    if new_feedback:
        result = analyze_sentiment([new_feedback])[0]
        st.info(f"Sentiment: {result[0]} ({round(result[1],2)})")

# ----------------------------
# SHOW DATA
# ----------------------------
st.subheader("📊 Raw Patient Feedback Data")
st.dataframe(data)

feedbacks = data["feedback"].tolist()

# ----------------------------
# MAIN ANALYSIS
# ----------------------------
if st.button("Generate Smart Notes"):

    sentiments = analyze_sentiment(feedbacks)
    keywords = extract_keywords(feedbacks)
    notes = generate_smart_notes(feedbacks, sentiments)

    # ----------------------------
    # COUNTS
    # ----------------------------
    pos_count = sum(1 for s in sentiments if s[0] == "POSITIVE")
    neg_count = sum(1 for s in sentiments if s[0] == "NEGATIVE")

    total = len(feedbacks)
    neg_percent = round((neg_count / total) * 100, 1)

    # ----------------------------
    # ISSUE GROUPING (🔥 IMPORTANT)
    # ----------------------------
    issue_list = []

    for note in notes:
        if "Waiting Time Issue" in note:
            issue_list.append("Waiting Time")
        elif "Cleanliness Issue" in note:
            issue_list.append("Cleanliness")
        else:
            issue_list.append("General")

    issue_counts = Counter(issue_list)
    top_issue = issue_counts.most_common(1)[0][0]

    # ----------------------------
    # IMPACT SUMMARY (🔥🔥🔥)
    # ----------------------------
    st.subheader("📌 Impact Summary")

    st.write(f"Total Feedback: {total}")
    st.write(f"Negative Feedback: {neg_percent}%")
    st.write(f"Top Issue: {top_issue}")

    # ----------------------------
    # PIE CHART
    # ----------------------------
    st.subheader("📊 Sentiment Distribution")

    fig1, ax1 = plt.subplots()
    ax1.pie([pos_count, neg_count], labels=["Positive", "Negative"], autopct="%1.1f%%")
    st.pyplot(fig1)

    # ----------------------------
    # BAR CHART (🔥 NEW)
    # ----------------------------
    st.subheader("📊 Issue Distribution")

    fig2, ax2 = plt.subplots()
    ax2.bar(issue_counts.keys(), issue_counts.values())
    ax2.set_xlabel("Issue Type")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

    # ----------------------------
    # GROUPED ISSUES (🔥🔥🔥)
    # ----------------------------
    st.subheader("🚨 Issue Breakdown")

    for issue, count in issue_counts.items():
        if issue != "General":
            st.error(f"{issue} Issues ({count} complaints)")

    st.success(f"Positive Feedback ({pos_count})")

    # ----------------------------
    # KEYWORDS
    # ----------------------------
    st.subheader("🔹 Keywords")
    st.write(", ".join(keywords))

    # ----------------------------
    # SMART NOTES
    # ----------------------------
    st.subheader("🧠 Smart Notes")

    for note in notes:
        st.success(note)
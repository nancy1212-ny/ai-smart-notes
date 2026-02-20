from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

# ----------------------------
# SENTIMENT
# ----------------------------
def analyze_sentiment(texts):
    results = sentiment_pipeline(texts)
    return [(res["label"], res["score"]) for res in results]

# ----------------------------
# KEYWORDS
# ----------------------------
def extract_keywords(texts):
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()

    # return top 10 keywords
    return words[:10]

# ----------------------------
# SMART NOTES
# ----------------------------
def generate_smart_notes(texts, sentiments):
    notes = []

    for text, (label, score) in zip(texts, sentiments):

        if "wait" in text.lower():
            issue = "Waiting Time Issue"
        elif "clean" in text.lower():
            issue = "Cleanliness Issue"
        else:
            issue = "General Feedback"

        note = f"Feedback: {text} | Sentiment: {label} | Issue: {issue}"
        notes.append(note)

    return notes
# assistant.py
import csv
from datetime import datetime
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CSV_PATH = Path(__file__).parent / "data" / "faqs.csv"

df = pd.read_csv(CSV_PATH).dropna(subset=["question", "answer"]).reset_index(drop=True)

# Match on question + category so category words (fees, library, hostel...) also help
corpus = (df["question"] + " " + df["category"].fillna("")).tolist()

vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
matrix = vectorizer.fit_transform(corpus)


def get_answer(query, threshold=0.2):
    """Return (answer, category, score) for the closest FAQ."""
    query = query.strip()
    if not query:
        return "Please type a question.", None, 0.0

    scores = cosine_similarity(vectorizer.transform([query]), matrix)[0]
    best = scores.argmax()

    if scores[best] < threshold:
        return (
            "Sorry, I don't have an answer for that. Please contact the college office.",
            None,
            float(scores[best]),
        )

    row = df.iloc[best]
    return row["answer"], row["category"], float(scores[best])


def get_categories():
    return sorted(df["category"].dropna().unique().tolist())
FEEDBACK_PATH = Path(__file__).parent / "data" / "feedback.csv"


def save_feedback(question, answer, category, rating):
    """Append one feedback row to data/feedback.csv."""
    new_file = not FEEDBACK_PATH.exists()
    with open(FEEDBACK_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "question", "answer", "category", "rating"])
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                question,
                answer,
                category or "",
                rating,
            ]
        )


def get_feedback_stats():
    """Return (total, helpful) counts from the feedback file."""
    if not FEEDBACK_PATH.exists():
        return 0, 0
    fb = pd.read_csv(FEEDBACK_PATH)
    return len(fb), int((fb["rating"] == "helpful").sum())
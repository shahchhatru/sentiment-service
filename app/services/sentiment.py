from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

# Setup model and tokenizer
TASK = "sentiment"
MODEL_NAME = f"cardiffnlp/twitter-roberta-base-emotion"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Load labels
mapping_url = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/emotion/mapping.txt"
with urllib.request.urlopen(mapping_url) as f:
    lines = f.read().decode("utf-8").split("\n")
labels = [row.split("\t")[1] for row in lines if row]

def preprocess(text: str) -> str:
    return " ".join(['@user' if t.startswith('@') else 'http' if t.startswith('http') else t for t in text.split()])

def analyze_sentiment(text: str):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)[::-1]
    results = [
        {"label": labels[i], "score": round(float(scores[i]), 4)}
        for i in ranking
    ]
    return results

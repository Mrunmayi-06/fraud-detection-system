import joblib
import requests
import pandas as pd

# Load ML model
vectorizer, model = joblib.load("level1_filter.pkl")

# Load dataset from CSV
df = pd.read_csv("obscured_dataset.csv")

emails = df["text"].tolist()[:10]  # take first 10 for testing

def rule_risk_score(email):
    score = 0
    keywords = ["verify", "credential", "password", "reset", "portal", "login"]
    for k in keywords:
        if k in email.lower():
            score += 10
    if "http" in email.lower():
        score += 30
    return score


OLLAMA_URL = "http://localhost:11434/api/generate"

for email in emails:
    X = vectorizer.transform([email])
    pred = model.predict(X)[0]

    if pred == 1:
        print("\n⚠️ Suspicious (ML):", email)

        prompt = f"""
You are a bank fraud analysis AI.

The following email may contain a hidden or obscured message.

Email:
\"\"\"{email}\"\"\"

Tasks:
1. Analyze if the text hides an encoded or fragmented meaning.
2. Attempt to infer any hidden intent.
3. Decide if the hidden or visible meaning suggests fraud.
4. Detect any attempt to obtain credentials or redirect user action.

Output strictly in this format:

Decoded_Message: <your inferred hidden meaning or NONE>
Fraud_Status: <Fraudulent or Safe>
Hidden_Channel: <Yes or No>
Risk_Score: <0-100>
Explanation: <short reasoning>
"""

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        r = requests.post(OLLAMA_URL, json=payload)
        result = r.json()["response"]
        print(result)

    else:
        print("\n✅ Safe (ML):", email)

def is_fraud(text):
    text = text.lower()

    suspicious_words = ["password", "otp", "pin", "login", "verify", "credentials"]
    urgent_words = ["urgent", "immediately", "suspended", "blocked"]
    link_words = ["http://", "https://", "bit.ly", "tinyurl"]

    score = 0

    for w in suspicious_words:
        if w in text:
            score += 2

    for w in urgent_words:
        if w in text:
            score += 2

    for w in link_words:
        if w in text:
            score += 3

    if score >= 4:
        return "Fraudulent", score
    else:
        return "Safe", score

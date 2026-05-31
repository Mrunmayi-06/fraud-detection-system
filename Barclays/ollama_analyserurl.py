import joblib
import requests
import pandas as pd

# Load ML model
vectorizer, model = joblib.load("level1_filter.pkl")

# Load dataset (NORMAL emails, not obscured)
df = pd.read_csv("level1_dataset.csv")

emails = df["text"].tolist()[:10]  # test first 10

OLLAMA_URL = "http://localhost:11434/api/generate"

def rule_risk_score(text):
    text = text.lower()
    score = 0

    credential_words = ["password", "otp", "pin", "login", "verify", "credentials", "reset"]
    urgent_words = ["urgent", "immediately", "suspended", "blocked"]
    link_words = ["http://", "https://", "bit.ly", "tinyurl"]

    for w in credential_words:
        if w in text:
            score += 20

    for w in urgent_words:
        if w in text:
            score += 15

    for w in link_words:
        if w in text:
            score += 30

    return score


for email in emails:
    X = vectorizer.transform([email])
    pred = model.predict(X)[0]

    rule_score = rule_risk_score(email)

    if pred == 1 or rule_score >= 30:
        print("\n⚠️ Suspicious:", email)

        prompt = f"""
You are a bank fraud detection AI.

Analyze the following email and decide if it is attempting:
1. Credential theft (password, OTP, login, PIN)
2. Fraud through website or link redirection

Email:
\"\"\"{email}\"\"\"

Output ONLY in this format:

Fraud_Status: <Fraudulent or Safe>
Risk_Score: <0-100>
Reason: <short explanation>
"""

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()["response"]
        print(result)

    else:
        print("\n✅ Safe:", email)

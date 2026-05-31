import joblib
import pandas as pd

vectorizer, model = joblib.load("level1_filter.pkl")

new_emails = [
    "Please update your banking credentials today.",
    "Lunch meeting at 2 PM in conference room.",
    "Verify your login through the attached page.",
    "Quarterly report draft attached."
]

X = vectorizer.transform(new_emails)
preds = model.predict(X)

for email, p in zip(new_emails, preds):
    if p == 1:
        print("⚠️ Suspicious:", email)
    else:
        print("✅ Safe:", email)


import pandas as pd

data = [
"""Meeting notes were prepared carefully for review.
Everyone agreed the agenda looked balanced today.
Lunch discussions helped clarify many points.
All departments shared their updates.
Please archive the document securely.""",

"""Project timelines usually depend on vendor responses.
Our finance team reviews unusual delays closely.
Reports should always be sent through official channels.
Updates are expected before the end of day.
Nothing seems wrong at first glance.""",

"""Customer service handled the case politely.
Agents followed protocol step by step.
Revisions were suggested by compliance.
Data privacy rules must be followed strictly.
Each action is logged internally.""",

"""Training sessions improve employee awareness.
Risk management focuses on abnormal behavior.
Audits are scheduled every quarter.
Security notices appear during system upgrades.
Everyone follows official instructions.""",

"""Monthly reports summarize performance clearly.
Internal reviews prevent operational mistakes.
System alerts are part of daily routine.
Transactions are monitored automatically.
Emails look routine but require inspection."""
]

labels = [1, 1, 0, 1, 0]  
# 1 = contains hidden risky intent
# 0 = safe

df = pd.DataFrame({"text": data, "label": labels})
df.to_csv("hidden_level2_dataset.csv", index=False)

print("Hidden dataset created")

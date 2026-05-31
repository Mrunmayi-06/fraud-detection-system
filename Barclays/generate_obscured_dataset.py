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

"""Training sessions improve employee awareness.
Risk management focuses on abnormal behavior.
Audits are scheduled every quarter.
Security notices appear during system upgrades.
Everyone follows official instructions.""",

"""Customer service handled the case politely.
Agents followed protocol step by step.
Revisions were suggested by compliance.
Data privacy rules must be followed strictly.
Each action is logged internally.""",

"""Monthly reports summarize performance clearly.
Internal reviews prevent operational mistakes.
System alerts are part of daily routine.
Transactions are monitored automatically.
Emails look routine but require inspection.""",

"""Finance teams coordinate resource planning daily.
Managers ensure communication remains transparent.
Operations continue smoothly despite pressure.
Deadlines are adjusted without public notice.
Everyone trusts the system fully.""",

"""The schedule was updated to reflect changes.
All members reviewed the document thoroughly.
Performance indicators appear within limits.
No one questioned the unusual alert.
Supervisors approved the final report.""",

"""Team discussions focused on workflow improvement.
Data logs were archived as usual.
Nothing appeared abnormal in the summary.
External links were included for reference.
Users were advised to follow instructions.""",

"""Reports were prepared using official templates.
Updates arrived later than expected.
Staff assumed the delay was technical.
No verification was requested externally.
Everything looked acceptable on paper.""",

"""Daily briefings covered compliance topics.
Security policies were mentioned briefly.
Employees followed the shared guidance.
A link was circulated for convenience.
No warnings were issued at the time."""
]

labels = [
    1,  # hidden suspicious
    1,  # hidden suspicious
    0,  # safe
    0,  # safe
    1,  # hidden suspicious
    1,
    1,
    1,
    0,
    1
]

df = pd.DataFrame({
    "text": data,
    "label": labels
})

df.to_csv("obscured_dataset.csv", index=False)
print("obscured_dataset.csv created")

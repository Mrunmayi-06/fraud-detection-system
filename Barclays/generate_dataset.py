import pandas as pd

data = [
    "Please review the attached invoice before the meeting tomorrow.",
    "Your account needs immediate verification to avoid service disruption.",
    "Kindly update your contact details in the internal system.",
    "The package could not be delivered due to incorrect address.",
    "We noticed unusual activity and recommend resetting your password.",
    "Schedule a discussion about quarterly performance metrics.",
    "To continue using services, validate credentials through the portal.",
    "The document was shared for collaboration and comments.",
    "Confirm your identity to maintain uninterrupted access.",
    "Team lunch is planned after the project review session.",

    # Obscured style emails (meaningful but suspicious)
    "Many users forget how passwords expire when access delays happen.",
    "Verification steps exist because attackers imitate trusted systems.",
    "Our internal notice reminds staff that login pages can be spoofed.",
    "Security policies mention that links may redirect silently.",
    "Employees should treat unexpected credentials requests carefully.",
    "A meeting agenda was sent with a hidden redirect link inside.",
    "System alerts are sometimes disguised as friendly reminders.",
    "Instructions were divided into small segments for clarity.",
    "Login confirmation should never be shared externally.",
    "External vendors sometimes send masked URLs in emails."
]

labels = [
    0,1,0,0,1,0,1,0,1,0,
    1,1,1,1,1,1,1,1,1,1
]

df = pd.DataFrame({"text": data, "label": labels})
df.to_csv("level1_dataset.csv", index=False)

print("Dataset created: level1_dataset.csv")

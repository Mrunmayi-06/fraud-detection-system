import json
import pandas as pd
from credential_scanner import CredentialScanner

scanner = CredentialScanner()

# Load dataset
df = pd.read_csv("level1_dataset.csv")

print("\n🔐 Credential Exposure Scanner (from dataset)\n")

for index, row in df.iterrows():
    text = row["text"]

    print("====================================")
    print("Email:", text)

    result = scanner.scan(text)

    print("Scan Result:")
    print(json.dumps(result, indent=4))

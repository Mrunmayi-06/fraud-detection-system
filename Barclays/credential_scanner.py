import re
import base64
import urllib.parse
from typing import List, Dict


class CredentialScanner:

    def __init__(self):
        self.total_score = 0
        self.findings = []

    # ---------------------------
    # Utility: Mask Credential
    # ---------------------------
    def mask_value(self, value: str) -> str:
        if len(value) <= 8:
            return "*" * len(value)
        return value[:4] + "*" * (len(value) - 8) + value[-4:]

    # ---------------------------
    # Utility: Add Finding
    # ---------------------------
    def add_finding(self, cred_type, value, location, score, was_obfuscated=False):
        self.total_score += score
        self.findings.append({
            "type": cred_type,
            "masked_value": self.mask_value(value),
            "location": location,
            "was_obfuscated": was_obfuscated,
            "score_contribution": score
        })

    # ---------------------------
    # Base64 Detection
    # ---------------------------
    def is_base64(self, s: str) -> bool:
        if len(s) < 20:
            return False
        if len(s) % 4 != 0:
            return False
        return re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s) is not None

    def try_base64_decode(self, s: str):
        try:
            decoded = base64.b64decode(s).decode("utf-8", errors="ignore")
            return decoded
        except Exception:
            return None

    # ---------------------------
    # Main Scan Function
    # ---------------------------
    def scan(self, text: str) -> Dict:

        lines = text.split("\n")

        # Patterns
        patterns = {
            "API_KEY_SK": r"\b(sk-[A-Za-z0-9]{16,})\b",
            "API_KEY_AWS": r"\b(AKIA[0-9A-Z]{16})\b",
            "API_KEY_GITHUB": r"\b(ghp_[A-Za-z0-9]{36})\b",
            "API_KEY_GOOGLE": r"\b(AIza[0-9A-Za-z-_]{35})\b",
            "BEARER_TOKEN": r"\bBearer\s+([A-Za-z0-9\-._~+/]+=*)\b",
            "JWT": r"\beyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b",
            "PRIVATE_KEY": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
            "PLAINTEXT_PASSWORD": r"(password|pwd|pass|db_password)\s*[:=]\s*['\"]?([^'\"\s]{6,})['\"]?"
        }

        # 1️⃣ Direct Pattern Matching
        for i, line in enumerate(lines):
            for key, pattern in patterns.items():
                matches = re.findall(pattern, line)
                for match in matches:
                    location = f"line {i+1}"

                    if key == "PRIVATE_KEY":
                        self.add_finding("PRIVATE_KEY", match, location, 50)

                    elif key == "PLAINTEXT_PASSWORD":
                        password_value = match[1]
                        self.add_finding("PLAINTEXT_PASSWORD", password_value, location, 35)

                    elif key == "JWT":
                        self.add_finding("JWT_TOKEN", match, location, 30)

                    elif key == "BEARER_TOKEN":
                        token = match
                        self.add_finding("BEARER_TOKEN", token, location, 30)

                    else:
                        self.add_finding("API_KEY", match, location, 40)

        # 2️⃣ Base64 Encoded Secret Detection
        words = re.findall(r"\b[A-Za-z0-9+/]{20,}={0,2}\b", text)
        for word in words:
            if self.is_base64(word):
                decoded = self.try_base64_decode(word)
                if decoded:
                    # Re-scan decoded content for credentials
                    if re.search(r"(password|AKIA|sk-|ghp_|secret|Bearer)", decoded):
                        self.add_finding("ENCODED_SECRET", word, "decoded_content", 35, True)

        # 3️⃣ URL Decode Detection
        decoded_url = urllib.parse.unquote(text)
        if decoded_url != text:
            if re.search(r"(password|AKIA|sk-|ghp_|secret|Bearer)", decoded_url):
                self.add_finding("URL_ENCODED_CREDENTIAL", decoded_url, "url_decoded", 35, True)

        # Cap score
        final_score = min(self.total_score, 100)

        # Risk tier
        if final_score <= 25:
            tier = "LOW"
        elif final_score <= 50:
            tier = "MEDIUM"
        elif final_score <= 75:
            tier = "HIGH"
        else:
            tier = "CRITICAL"

        return {
            "credential_exposure_detected": len(self.findings) > 0,
            "risk_score": final_score,
            "risk_tier": tier,
            "findings": self.findings
        }
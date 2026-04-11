"""Detection service."""
def detect_attack(payload: str):
    payload = payload.lower()

    if "or 1=1" in payload or "'--" in payload:
        return "SQL Injection"

    if "<script>" in payload:
        return "XSS"

    if "admin" in payload and "password" in payload:
        return "Brute Force Attempt"

    return "Normal"
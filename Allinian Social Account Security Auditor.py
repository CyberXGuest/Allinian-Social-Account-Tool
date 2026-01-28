import re
import time
from datetime import datetime

# -----------------------------
# ANSI COLORS
# -----------------------------
PINK = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# -----------------------------
# BANNER
# -----------------------------
def banner():
    print(PINK + """
╔══════════════════════════════════════════════╗
║     Allinian Social Account Security Tool     ║
║     Created by Allin Isla Minde               ║
║     Facebook: Hackrate.Inc                    ║
║     Defensive Security Auditor                ║
╚══════════════════════════════════════════════╝
""" + RESET)

# -----------------------------
# PASSWORD STRENGTH CHECK
# -----------------------------
def password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*()_+=-]", password):
        score += 1

    return score

# -----------------------------
# MFA CHECK (SIMULATED)
# -----------------------------
def mfa_check(method):
    if method.lower() == "app":
        return GREEN + "Strong MFA (Authenticator App)" + RESET, 0
    elif method.lower() == "sms":
        return YELLOW + "Weak MFA (SMS vulnerable to SIM-swap)" + RESET, 1
    else:
        return RED + "No MFA Enabled" + RESET, 3

# -----------------------------
# LOGIN ANOMALY DETECTION
# -----------------------------
def analyze_logins(login_attempts):
    risky = 0
    ips = set()

    for attempt in login_attempts:
        ips.add(attempt["ip"])
        if attempt["success"] is False:
            risky += 1

    if len(ips) > 3:
        risky += 2

    return risky

# -----------------------------
# SECURITY AUDIT
# -----------------------------
def run_audit(username, password, mfa_method, login_attempts):
    print(f"\nAuditing account: {username}")
    risk_score = 0

    pw_score = password_strength(password)
    if pw_score < 4:
        print(RED + "❌ Weak password detected" + RESET)
        risk_score += 3
    else:
        print(GREEN + "✔ Strong password" + RESET)

    mfa_result, mfa_risk = mfa_check(mfa_method)
    print("MFA Status:", mfa_result)
    risk_score += mfa_risk

    login_risk = analyze_logins(login_attempts)
    if login_risk > 2:
        print(YELLOW + "⚠ Suspicious login behavior detected" + RESET)
    else:
        print(GREEN + "✔ Login behavior normal" + RESET)

    risk_score += login_risk

    return risk_score

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    banner()

    # Mock data (safe & local)
    user_logins = [
        {"ip": "192.168.1.10", "success": False},
        {"ip": "192.168.1.11", "success": False},
        {"ip": "192.168.1.12", "success": True},
        {"ip": "192.168.1.13", "success": False}
    ]

    total_risk = run_audit(
        username="alice",
        password="Password123!",
        mfa_method="sms",
        login_attempts=user_logins
    )

    print("\nRisk Score:", total_risk)

    if total_risk >= 6:
        print(RED + "HIGH RISK – Immediate action required" + RESET)
    elif total_risk >= 3:
        print(YELLOW + "MEDIUM RISK – Security improvements recommended" + RESET)
    else:
        print(GREEN + "LOW RISK – Account security is strong" + RESET)

    print("\nAudit completed:", datetime.now())

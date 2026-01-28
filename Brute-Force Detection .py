import time
from collections import defaultdict

# -----------------------------
# Mock user database (hashed in real systems)
# -----------------------------
USERS = {
    "alice": "password123",
    "bob": "securepass",
    "charlie": "letmein"
}

# -----------------------------
# Security configuration
# -----------------------------
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 60  # seconds
MFA_THRESHOLD = 3

failed_attempts = defaultdict(int)
lockout_until = {}
suspicious_ips = defaultdict(int)

# -----------------------------
# Login function (DEFENSIVE)
# -----------------------------
def login(username, password, ip_address):
    current_time = time.time()

    # Check lockout
    if username in lockout_until and current_time < lockout_until[username]:
        return f"[LOCKED] Account '{username}' locked until {time.ctime(lockout_until[username])}"

    # Invalid user
    if username not in USERS:
        suspicious_ips[ip_address] += 1
        return "[ERROR] Invalid username"

    # Wrong password
    if USERS[username] != password:
        failed_attempts[username] += 1
        suspicious_ips[ip_address] += 1

        # MFA trigger simulation
        if failed_attempts[username] >= MFA_THRESHOLD:
            print(f"[MFA] MFA challenge required for user '{username}'")

        # Lockout trigger
        if failed_attempts[username] >= MAX_ATTEMPTS:
            lockout_until[username] = current_time + LOCKOUT_TIME
            return f"[LOCKED] Too many attempts. Account locked."

        return "[DENIED] Incorrect password"

    # Successful login
    failed_attempts[username] = 0
    return "[SUCCESS] Login successful"


# -----------------------------
# Brute-force attempt simulator
# -----------------------------
def brute_force_simulator(username, ip_address):
    common_passwords = [
        "123456", "password", "admin", "letmein",
        "qwerty", "password123", "welcome"
    ]

    for pwd in common_passwords:
        result = login(username, pwd, ip_address)
        print(f"Attempting '{pwd}' → {result}")
        time.sleep(0.5)


# -----------------------------
# Run simulation
# -----------------------------
if __name__ == "__main__":
    print("=== Brute-Force Defense Simulator ===\n")

    brute_force_simulator("alice", "192.168.1.50")

    print("\n=== Suspicious IP Report ===")
    for ip, count in suspicious_ips.items():
        print(f"{ip} → {count} suspicious actions")

import time
from collections import defaultdict

# -----------------------------
# ANSI COLORS
# -----------------------------
PINK = "\033[95m"
RESET = "\033[0m"

# -----------------------------
# BANNER
# -----------------------------
def banner():
    print(PINK + r"""
    █████╗ ██╗     ██╗     ██╗███╗   ██╗██╗ █████╗ ███╗   ██╗
   ██╔══██╗██║     ██║     ██║████╗  ██║██║██╔══██╗████╗  ██║
   ███████║██║     ██║     ██║██╔██╗ ██║██║███████║██╔██╗ ██║
   ██╔══██║██║     ██║     ██║██║╚██╗██║██║██╔══██║██║╚██╗██║
   ██║  ██║███████╗███████╗██║██║ ╚████║██║██║  ██║██║ ╚████║
   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

        Allinian Social Account Tool
   Created by Allin Isla Minde
   Facebook: Hackrate.Inc
   (Defensive Security Simulator)
    """ + RESET)

# -----------------------------
# MOCK USER DATABASE
# -----------------------------
USERS = {
    "alice": "password123",
    "bob": "securepass",
    "charlie": "letmein"
}

# -----------------------------
# SECURITY CONFIG
# -----------------------------
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 60  # seconds
MFA_THRESHOLD = 3

failed_attempts = defaultdict(int)
lockout_until = {}
suspicious_ips = defaultdict(int)

# -----------------------------
# DEFENSIVE LOGIN FUNCTION
# -----------------------------
def login(username, password, ip_address):
    now = time.time()

    if username in lockout_until and now < lockout_until[username]:
        return f"[LOCKED] Account locked until {time.ctime(lockout_until[username])}"

    if username not in USERS:
        suspicious_ips[ip_address] += 1
        return "[ERROR] Invalid username"

    if USERS[username] != password:
        failed_attempts[username] += 1
        suspicious_ips[ip_address] += 1

        if failed_attempts[username] >= MFA_THRESHOLD:
            print(f"[MFA] MFA required for user '{username}'")

        if failed_attempts[username] >= MAX_ATTEMPTS:
            lockout_until[username] = now + LOCKOUT_TIME
            return "[LOCKED] Too many failed attempts"

        return "[DENIED] Incorrect password"

    failed_attempts[username] = 0
    return "[SUCCESS] Login successful"

# -----------------------------
# BRUTE-FORCE BEHAVIOR SIMULATOR
# (FOR DEFENSE TESTING ONLY)
# -----------------------------
def brute_force_simulator(username, ip):
    test_passwords = [
        "123456", "password", "admin",
        "welcome", "password123", "qwerty"
    ]

    for pwd in test_passwords:
        result = login(username, pwd, ip)
        print(f"Trying '{pwd}' → {result}")
        time.sleep(0.5)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    banner()

    print("Running defensive brute-force detection simulation...\n")
    brute_force_simulator("alice", "192.168.1.100")

    print("\nSuspicious IP activity:")
    for ip, count in suspicious_ips.items():
        print(f"{ip} → {count} alerts")

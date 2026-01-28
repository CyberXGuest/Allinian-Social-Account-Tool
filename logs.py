from datetime import datetime

LOG_FILE = "allinian_security.log"

def log_event(level, module, message):
    """
    level  : INFO | WARNING | ALERT | ERROR
    module : Tool name (BruteForce, Login, Audit, etc.)
    message: Event description
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] [{module}] {message}\n"

    with open(LOG_FILE, "a") as log:
        log.write(entry)

def log_info(module, message):
    log_event("INFO", module, message)

def log_warning(module, message):
    log_event("WARNING", module, message)

def log_alert(module, message):
    log_event("ALERT", module, message)

def log_error(module, message):
    log_event("ERROR", module, message)
from logger import log_info, log_warning, log_alert
log_info("Login", "User alice logged in successfully")
log_warning("BruteForce", "Multiple failed attempts detected")
log_alert("Audit", "High-risk account identified")

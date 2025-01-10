import re
import time
from collections import defaultdict

LOGIN_ATTEMPTS = defaultdict(list)
BLACKLISTED_IPS = set()
SCAM_KEYWORDS = ["prize", "lottery", "urgent", "account suspended", "click here"]
THRESHOLD = 5
TIME_WINDOW = 60
ALERT_LOG = []

class MailIDS:
    def __init__(self, threshold, time_window):
        self.threshold = threshold
        self.time_window = time_window

    def analyze_logs(self, log_file):
        with open(log_file, "r") as f:
            for line in f:
                self.analyze_line(line)

    def analyze_line(self, line):
        login_match = re.search(r"(\d+\.\d+\.\d+\.\d+).*email=(\S+).*status=(\S+)", line)
        if login_match:
            ip, email, status = login_match.groups()
            self.process_login_entry(ip, email, status)
        scam_match = re.search(r"email=(\S+).*message=(.*)", line)
        if scam_match:
            email, message = scam_match.groups()
            self.check_for_scam(email, message)

    def process_login_entry(self, ip, email, status):
        if status == "FAILED":
            LOGIN_ATTEMPTS[email].append(time.time())
            self.check_suspicious_activity(email)
        if ip in BLACKLISTED_IPS:
            self.alert(email, f"Blacklisted IP detected: {ip}")

    def check_suspicious_activity(self, email):
        attempts = LOGIN_ATTEMPTS[email]
        now = time.time()
        LOGIN_ATTEMPTS[email] = [t for t in attempts if now - t <= self.time_window]
        if len(LOGIN_ATTEMPTS[email]) >= self.threshold:
            self.alert(email, "Multiple failed login attempts")
        if len(set([t // self.time_window for t in attempts])) > 1:
            self.alert(email, "Suspicious activity: multiple login attempts from different time windows")

    def check_for_scam(self, email, message):
        lower_message = message.lower()
        for keyword in SCAM_KEYWORDS:
            if keyword in lower_message:
                self.alert(email, f"Potential scam detected: {keyword}")
                break

    def detect_anomalous_activity(self, email, ip):
        if len(LOGIN_ATTEMPTS[email]) >= self.threshold:
            unique_ips = len(set(LOGIN_ATTEMPTS[email]))
            if unique_ips > 1:
                self.alert(email, f"Suspicious activity: multiple IPs used for {email}")

    def alert(self, email, reason):
        alert_message = f"ALERT: {reason} for {email}"
        ALERT_LOG.append(alert_message)
        print(alert_message)

    def add_blacklisted_ip(self, ip):
        BLACKLISTED_IPS.add(ip)
        print(f"IP {ip} has been blacklisted")

    def verify_before_alert(self, email, reason):
        if reason.startswith("Potential scam") and not any([kw in reason for kw in SCAM_KEYWORDS]):
            print(f"ALERT (Double Check Passed): {reason} for {email}")
        else:
            self.alert(email, reason)

    def generate_dashboard(self):
        print("\n--- Dashboard ---")
        print("Total Alerts:", len(ALERT_LOG))
        print("Recent Alerts:")
        for alert in ALERT_LOG[-10:]:
            print(alert)

    def segment_user_behavior(self):
        user_patterns = {email: len(LOGIN_ATTEMPTS[email]) for email in LOGIN_ATTEMPTS}
        print("\n--- User Behavior Analysis ---")
        for email, attempts in user_patterns.items():
            print(f"{email}: {attempts} login attempts")

ids = MailIDS(THRESHOLD, TIME_WINDOW)

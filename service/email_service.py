import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import os
from pathlib import Path
import json

class EmailService:
    """
    Simple email sender using localhost SMTP (no authentication).
    Works out-of-the-box on Ubuntu and macOS if a local SMTP server is running.
    Supports port 25 (default) and 1025 (MailHog, smtp4dev, etc).
    """
    def __init__(self, smtp_server: str = "localhost", smtp_port: int = 25):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, subject: str, body: str, recipients: List[str], sender: str = None):
        sender = sender or "TAF <jbriceno.qa@gmail.com>"
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.sendmail(sender, recipients, msg.as_string())
            print(f"Email sent to {recipients} via {self.smtp_server}:{self.smtp_port}")
        except Exception as e:
            print(f"Failed to send email via {self.smtp_server}:{self.smtp_port}: {e}")

    def send_report_email(self):
        """
        Send the Playwright test report as an email (if the report exists).
        """
        REPORT_PATH = Path(__file__).parent.parent / "reports" / "playwright_report.json"
        EMAIL_TO = "jbriceno.qa@gmail.com"
        if REPORT_PATH.exists():
            with REPORT_PATH.open("r", encoding="utf-8") as f:
                report = json.load(f)
            subject = "Playwright Test Report"
            body = json.dumps(report, indent=2)
            try:
                self.send_email(subject, body, [EMAIL_TO], sender="TAF <jbriceno.qa@gmail.com>")
                print(f"\nTest report sent to {EMAIL_TO} via EmailService.")
            except Exception as e:
                print(f"\nFailed to send test report email: {e}")
        else:
            print(f"\nNo test report found at {REPORT_PATH}, email not sent.")

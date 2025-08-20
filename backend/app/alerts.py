import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def send_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    to_email: str,
    subject: str,
    body: str
) -> bool:
    """Send email alert via SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        logger.info(f"Email alert sent successfully to {to_email}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")
        return False

async def send_alert(
    message: str,
    smtp_config: dict,
    to_email: str
) -> bool:
    """Send alert via email"""
    try:
        return send_email(
            smtp_config["host"],
            smtp_config["port"],
            smtp_config["username"],
            smtp_config["password"],
            to_email,
            f"CI/CD Alert: {message[:50]}...",
            message
        )
    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")
        return False

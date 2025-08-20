import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def send_slack(webhook_url: str, text: str) -> bool:
    """Send Slack alert via webhook"""
    try:
        message = {
            "text": text,
            "username": "CI/CD Dashboard",
            "icon_emoji": ":robot_face:"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=message, timeout=10.0)
            response.raise_for_status()
            
        logger.info(f"Slack alert sent successfully: {text[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")
        return False

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
    channel: str,
    message: str,
    webhook_url: Optional[str] = None,
    smtp_config: Optional[dict] = None,
    to_email: Optional[str] = None
) -> bool:
    """Send alert via specified channel"""
    try:
        if channel == "slack" and webhook_url:
            return await send_slack(webhook_url, message)
        elif channel == "email" and smtp_config and to_email:
            return send_email(
                smtp_config["host"],
                smtp_config["port"],
                smtp_config["username"],
                smtp_config["password"],
                to_email,
                f"CI/CD Alert: {message[:50]}...",
                message
            )
        else:
            logger.error(f"Invalid channel {channel} or missing configuration")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send alert via {channel}: {e}")
        return False

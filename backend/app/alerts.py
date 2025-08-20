import smtplib
import os
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

async def send_build_failure_alert(
    build_data: dict,
    settings: dict,
    session
) -> bool:
    """Send alert for a failed build"""
    try:
        # Check if alerts are enabled
        if not os.getenv("ALERTS_ENABLED", "true").lower() == "true":
            logger.info("Alerts disabled, skipping alert send")
            return False
        
        # Check if we already sent an alert for this build
        from .models import Alert
        from sqlalchemy import select
        
        existing_alert = await session.execute(
            select(Alert).where(
                Alert.build_id == build_data["id"],
                Alert.channel == "email"
            )
        )
        
        if existing_alert.scalar_one_or_none():
            logger.info(f"Alert already sent for build {build_data['id']}, skipping")
            return False
        
        # Prepare alert message
        provider_name = build_data.get("provider_name", "Unknown Provider")
        external_id = build_data.get("external_id", "Unknown")
        branch = build_data.get("branch", "Unknown")
        duration = build_data.get("duration_seconds", 0)
        url = build_data.get("url", "")
        
        # Email subject and body
        subject = f"[CI/CD] Build FAILED: {provider_name} #{external_id}"
        body = f"""Build FAILED

Provider: {provider_name}
Build ID: #{external_id}
Branch: {branch}
Duration: {duration} seconds
URL: {url}

This is an automated alert from the CI/CD Health Dashboard.
"""
        
        # Get SMTP configuration from environment
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USERNAME")
        smtp_pass = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_host, smtp_user, smtp_pass]):
            logger.error("SMTP configuration incomplete, cannot send email alert")
            return False
        
        # Send email
        success = send_email(
            smtp_host,
            smtp_port,
            smtp_user,
            smtp_pass,
            settings["alert_email"],
            subject,
            body
        )
        
        if success:
            # Store alert record to prevent duplicate alerts
            alert = Alert(
                build_id=build_data["id"],
                channel="email",
                success=True,
                message=f"Build failure alert sent to {settings['alert_email']}"
            )
            session.add(alert)
            await session.commit()
            
            logger.info(f"Build failure alert sent successfully for build {build_data['id']}")
            return True
        else:
            # Store failed alert record
            alert = Alert(
                build_id=build_data["id"],
                channel="email",
                success=False,
                message="Failed to send build failure alert"
            )
            session.add(alert)
            await session.commit()
            
            return False
            
    except Exception as e:
        logger.error(f"Failed to send build failure alert: {e}")
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

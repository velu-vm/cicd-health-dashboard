import os
import aiohttp
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime
from .models import Alert, AlertHistory, Build
from .schemas import AlertType, AlertSeverity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class AlertService:
    """Service for sending alerts via various channels"""
    
    def __init__(self):
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "#alerts")
        
        # SMTP configuration
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "alerts@cicd-dashboard.com")
        self.smtp_from_name = os.getenv("SMTP_FROM_NAME", "CI/CD Dashboard")
        
        self.alerts_enabled = os.getenv("ALERTS_ENABLED", "true").lower() == "true"
    
    async def send_alert(
        self,
        session: AsyncSession,
        alert_type: AlertType,
        message: str,
        severity: AlertSeverity = AlertSeverity.INFO,
        build: Optional[Build] = None,
        alert_id: Optional[int] = None
    ) -> bool:
        """Send an alert via the specified channel"""
        if not self.alerts_enabled:
            print(f"Alerts disabled, skipping: {message}")
            return False
        
        try:
            # Create alert history record
            alert_history = AlertHistory(
                alert_id=alert_id or 1,  # Default alert ID
                build_id=build.id if build else None,
                message=message,
                severity=severity.value,
                status="pending"
            )
            session.add(alert_history)
            await session.commit()
            
            # Send alert based on type
            success = False
            error_message = None
            
            if alert_type == AlertType.SLACK:
                success = await self._send_slack_alert(message, severity, build)
            elif alert_type == AlertType.EMAIL:
                success = await self._send_email_alert(message, severity, build)
            elif alert_type == AlertType.WEBHOOK:
                success = await self._send_webhook_alert(message, severity, build)
            
            # Update alert history
            alert_history.status = "sent" if success else "failed"
            if not success:
                alert_history.error_message = error_message or "Unknown error"
            
            await session.commit()
            return success
            
        except Exception as e:
            print(f"Error sending alert: {e}")
            if 'alert_history' in locals():
                alert_history.status = "failed"
                alert_history.error_message = str(e)
                await session.commit()
            return False
    
    async def send_build_failure_alert(
        self,
        session: AsyncSession,
        build: Build,
        alert_type: AlertType = AlertType.EMAIL
    ) -> bool:
        """Send a build failure alert"""
        message = f"Build #{build.external_id} failed on branch {build.branch}"
        if build.triggered_by:
            message += f" (triggered by {build.triggered_by})"
        
        return await self.send_alert(
            session=session,
            alert_type=alert_type,
            message=message,
            severity=AlertSeverity.ERROR,
            build=build
        )
    
    async def _send_slack_alert(
        self,
        message: str,
        severity: AlertSeverity,
        build: Optional[Build] = None
    ) -> bool:
        """Send alert to Slack"""
        if not self.slack_webhook_url:
            print("Slack webhook URL not configured")
            return False
        
        try:
            # Prepare Slack message
            color_map = {
                AlertSeverity.INFO: "#36a64f",
                AlertSeverity.WARNING: "#ffa500",
                AlertSeverity.ERROR: "#ff0000",
                AlertSeverity.CRITICAL: "#8b0000"
            }
            
            attachments = [{
                "color": color_map.get(severity, "#36a64f"),
                "title": f"CI/CD Alert - {severity.value.upper()}",
                "text": message,
                "fields": [],
                "footer": "CI/CD Dashboard",
                "ts": int(datetime.now().timestamp())
            }]
            
            if build:
                attachments[0]["fields"].extend([
                    {"title": "Build ID", "value": build.external_id, "short": True},
                    {"title": "Branch", "value": build.branch or "N/A", "short": True},
                    {"title": "Status", "value": build.status, "short": True}
                ])
                if build.url:
                    attachments[0]["title_link"] = build.url
            
            payload = {
                "channel": self.slack_channel,
                "text": f"CI/CD Alert: {message}",
                "attachments": attachments
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.slack_webhook_url, json=payload) as response:
                    if response.status == 200:
                        print(f"Slack alert sent successfully: {message}")
                        return True
                    else:
                        print(f"Slack alert failed with status {response.status}")
                        return False
                        
        except Exception as e:
            print(f"Error sending Slack alert: {e}")
            return False
    
    async def _send_email_alert(
        self,
        message: str,
        severity: AlertSeverity,
        build: Optional[Build] = None
    ) -> bool:
        """Send alert via email"""
        if not all([self.smtp_host, self.smtp_username, self.smtp_password]):
            print("SMTP configuration incomplete")
            return False
        
        try:
            # Prepare email
            subject = f"CI/CD Alert - {severity.value.upper()}"
            
            # Build email body
            body = f"""
            CI/CD Dashboard Alert
            
            Severity: {severity.value.upper()}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Message: {message}
            """
            
            if build:
                body += f"""
                
                Build Details:
                - ID: {build.external_id}
                - Branch: {build.branch or 'N/A'}
                - Status: {build.status}
                - Triggered by: {build.triggered_by or 'N/A'}
                """
                if build.url:
                    body += f"- URL: {build.url}"
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
            msg['To'] = self.smtp_username  # Send to configured email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=True
            )
            
            print(f"Email alert sent successfully: {message}")
            return True
            
        except Exception as e:
            print(f"Error sending email alert: {e}")
            return False
    
    async def _send_webhook_alert(
        self,
        message: str,
        severity: AlertSeverity,
        build: Optional[Build] = None
    ) -> bool:
        """Send alert via webhook (placeholder for future implementation)"""
        print(f"Webhook alerts not yet implemented: {message}")
        return False
    
    async def test_alert(
        self,
        session: AsyncSession,
        alert_type: AlertType,
        message: str,
        severity: AlertSeverity = AlertSeverity.INFO
    ) -> Dict[str, Any]:
        """Test alert delivery"""
        try:
            success = await self.send_alert(
                session=session,
                alert_type=alert_type,
                message=message,
                severity=severity
            )
            
            return {
                "success": success,
                "message": f"Test alert {'sent successfully' if success else 'failed'}",
                "alert_type": alert_type.value,
                "severity": severity.value
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Test alert failed: {str(e)}",
                "error": str(e)
            }

# Global alert service instance
alert_service = AlertService()

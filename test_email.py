#!/usr/bin/env python3
"""
Simple email test script to debug SMTP issues
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection step by step"""
    
    # Get SMTP settings
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL")
    smtp_from_name = os.getenv("SMTP_FROM_NAME")
    
    print("🔧 SMTP Configuration:")
    print(f"  Host: {smtp_host}")
    print(f"  Port: {smtp_port}")
    print(f"  Username: {smtp_username}")
    print(f"  Password: {smtp_password[:4]}***{smtp_password[-4:] if len(smtp_password) > 8 else '***'}")
    print(f"  From Email: {smtp_from_email}")
    print(f"  From Name: {smtp_from_name}")
    print()
    
    try:
        # Test 1: Create message
        print("📧 Creating email message...")
        msg = MIMEMultipart()
        msg["From"] = f"{smtp_from_name} <{smtp_from_email}>"
        msg["To"] = "renugavelmurugan09@gmail.com"
        msg["Subject"] = "Test Email from CI/CD Dashboard"
        
        body = "This is a test email from the CI/CD Dashboard to verify SMTP configuration."
        msg.attach(MIMEText(body, "plain"))
        print("✅ Message created successfully")
        
        # Test 2: Connect to SMTP server
        print(f"🔌 Connecting to {smtp_host}:{smtp_port}...")
        if smtp_port == 465:
            print("  Using SSL connection...")
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            print("  Using TLS connection...")
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        
        print("✅ Connected to SMTP server")
        
        # Test 3: Login
        print("🔐 Logging in...")
        server.login(smtp_username, smtp_password)
        print("✅ Login successful")
        
        # Test 4: Send email
        print("📤 Sending email...")
        text = msg.as_string()
        server.sendmail(smtp_from_email, "renugavelmurugan09@gmail.com", text)
        print("✅ Email sent successfully!")
        
        # Test 5: Close connection
        server.quit()
        print("✅ Connection closed")
        
        print("\n🎉 All tests passed! Email should be delivered to renugavelmurugan09@gmail.com")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide specific guidance for common errors
        if "Authentication" in str(e):
            print("\n💡 Authentication Error - Check:")
            print("  1. Gmail username is correct")
            print("  2. App password is correct (not your regular password)")
            print("  3. 2-Factor Authentication is enabled")
            print("  4. App password was generated for 'Mail'")
        
        elif "SSL" in str(e) or "TLS" in str(e):
            print("\n💡 SSL/TLS Error - Check:")
            print("  1. Port 465 for SSL, Port 587 for TLS")
            print("  2. Firewall allows outbound SMTP")
        
        elif "Connection" in str(e):
            print("\n💡 Connection Error - Check:")
            print("  1. Internet connection")
            print("  2. Gmail SMTP server is accessible")
            print("  3. No corporate firewall blocking SMTP")

if __name__ == "__main__":
    test_smtp_connection()

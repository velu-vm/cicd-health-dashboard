#!/usr/bin/env python3
"""
Database initialization script for CI/CD Health Dashboard
Creates tables and inserts default settings
"""

import asyncio
import os
from sqlalchemy import select
from app.db import init_db, AsyncSessionLocal
from app.models import Settings, Provider

async def create_default_settings():
    """Create default settings if they don't exist"""
    async with AsyncSessionLocal() as session:
        # Check if settings exist
        result = await session.execute(select(Settings).where(Settings.id == 1))
        settings = result.scalar_one_or_none()
        
        if not settings:
            # Create default settings
            default_settings = Settings(
                id=1,
                alert_email="alerts@example.com",
                smtp_host="smtp.gmail.com",
                smtp_port=587,
                smtp_username="alerts@example.com",
                smtp_password="your-app-password",
                api_write_key="dev-write-key-change-in-production"
            )
            session.add(default_settings)
            await session.commit()
            print("✅ Default settings created")
        else:
            print("✅ Settings already exist")

async def create_default_providers():
    """Create default providers if they don't exist"""
    async with AsyncSessionLocal() as session:
        # Check if GitHub Actions provider exists
        result = await session.execute(
            select(Provider).where(Provider.name == "github-actions-default")
        )
        github_provider = result.scalar_one_or_none()
        
        if not github_provider:
            github_provider = Provider(
                name="github-actions-default",
                kind="github_actions",
                config_json={"description": "Default GitHub Actions provider"}
            )
            session.add(github_provider)
        
        # Check if Jenkins provider exists
        result = await session.execute(
            select(Provider).where(Provider.name == "jenkins-default")
        )
        jenkins_provider = result.scalar_one_or_none()
        
        if not jenkins_provider:
            jenkins_provider = Provider(
                name="jenkins-default",
                kind="jenkins",
                config_json={"description": "Default Jenkins provider"}
            )
            session.add(jenkins_provider)
        
        await session.commit()
        print("✅ Default providers created")

async def main():
    """Main initialization function"""
    print("🚀 Initializing CI/CD Health Dashboard Database...")
    
    try:
        # Initialize database tables
        await init_db()
        print("✅ Database tables created")
        
        # Create default settings
        await create_default_settings()
        
        # Create default providers
        await create_default_providers()
        
        print("🎉 Database initialization completed successfully!")
        print("\nDefault API Write Key: dev-write-key-change-in-production")
        print("Use this key in the X-API-KEY header for write operations")
        print("\nEmail Configuration:")
        print("- SMTP Host: smtp.gmail.com")
        print("- SMTP Port: 587")
        print("- Username: alerts@example.com")
        print("- Password: your-app-password (update this)")
        print("- Alert Email: alerts@example.com")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

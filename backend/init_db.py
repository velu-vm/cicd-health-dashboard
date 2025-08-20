#!/usr/bin/env python3
"""
Database initialization script for CI/CD Health Dashboard
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.db import init_db, close_db
from app.models import Base, Provider, Alert, Settings
from app.db import async_engine

async def main():
    """Initialize the database with tables and basic data"""
    print("🚀 Initializing CI/CD Health Dashboard Database...")
    
    try:
        # Create all tables
        print("📋 Creating database tables...")
        await init_db()
        
        # Create default alert configuration
        print("🔔 Setting up default alert configuration...")
        async with async_engine.begin() as conn:
            # Check if default alert exists
            from sqlalchemy import select
            result = await conn.execute(select(Alert).where(Alert.name == "default-email"))
            if not result.scalar_one_or_none():
                # Create default email alert
                default_alert = Alert(
                    name="default-email",
                    type="email",
                    config_json={
                        "enabled": True,
                        "recipients": ["admin@example.com"]
                    },
                    is_active=True
                )
                await conn.execute(
                    "INSERT INTO alerts (name, type, config_json, is_active, created_at) VALUES (?, ?, ?, ?, ?)",
                    (default_alert.name, default_alert.type, str(default_alert.config_json), default_alert.is_active, default_alert.created_at)
                )
                print("✅ Default email alert created")
            else:
                print("ℹ️  Default alert already exists")
        
        # Create default settings
        print("⚙️  Setting up default settings...")
        async with async_engine.begin() as conn:
            # Check if default settings exist
            result = await conn.execute(select(Settings).where(Settings.key == "dashboard_title"))
            if not result.scalar_one_or_none():
                # Create default settings
                default_settings = [
                    ("dashboard_title", "CI/CD Health Dashboard", "Dashboard title"),
                    ("refresh_interval", "30", "Auto-refresh interval in seconds"),
                    ("alerts_enabled", "true", "Enable/disable alert system"),
                    ("max_builds_display", "50", "Maximum builds to display in table")
                ]
                
                for key, value, description in default_settings:
                    await conn.execute(
                        "INSERT INTO settings (key, value, description, created_at) VALUES (?, ?, ?, ?)",
                        (key, value, description, "2024-01-01T00:00:00")
                    )
                print("✅ Default settings created")
            else:
                print("ℹ️  Default settings already exist")
        
        print("🎉 Database initialization completed successfully!")
        print("\n📊 Next steps:")
        print("1. Start the backend: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("2. Seed with sample data: curl -X POST http://localhost:8000/api/seed")
        print("3. Open the frontend: frontend/index.html")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())

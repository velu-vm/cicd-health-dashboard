# Scripts Directory

## 🎯 **Main Script (Use This One)**

### `setup.sh` - Complete Setup Script
**Purpose**: The ONLY script you need - handles everything automatically
**Usage**: `./setup.sh`
**What it does**:
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Generates configuration files
- ✅ Starts the server
- ✅ Tests all functionality
- ✅ Provides setup instructions

## 🔧 **Utility Scripts**

### `deploy.sh` - Production Deployment
**Purpose**: Deploy the dashboard using Docker
**Usage**: `./deploy.sh`
**When to use**: For production deployments

### `scripts/verify.sh` - API Testing
**Purpose**: Test all API endpoints
**Usage**: `./scripts/verify.sh`
**When to use**: After setup to verify everything works

## 📚 **Documentation Files**

- **`EMAIL_SETUP.md`** - How to configure email notifications
- **`NGROK_SETUP.md`** - How to expose dashboard for GitHub webhooks
- **`SETUP_GUIDE.md`** - Detailed manual setup instructions

## 🚀 **Quick Start**

```bash
# 1. Clone the repository
git clone https://github.com/velu-vm/cicd-health-dashboard.git
cd cicd-health-dashboard

# 2. Run the setup script (handles everything)
./setup.sh

# 3. Follow the instructions provided
```

## 💡 **Pro Tips**

- **Always start with `./setup.sh`** - it handles everything
- **Use `./deploy.sh`** only for production deployments
- **Use `./scripts/verify.sh`** to test after setup
- **Check documentation files** for specific configuration needs

## 🎉 **Result**

One script to rule them all! No more confusion about which script to use.

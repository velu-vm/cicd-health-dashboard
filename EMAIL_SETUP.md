# Email Alert Setup for CI/CD Dashboard

This guide explains how to configure email notifications for your CI/CD Health Dashboard.

## 🎯 What You'll Get

- **Success Notifications**: Email when pipelines complete successfully
- **Failure Alerts**: Immediate email notifications when pipelines fail
- **Real-time Updates**: Alerts sent as soon as GitHub Actions completes
- **Complete Coverage**: You'll get notified for EVERY pipeline result (success/failure)

## 📧 Email Configuration

### **Option 1: Gmail (Recommended for Testing)**

1. **Enable 2-Factor Authentication**:
   - Go to [Google Account Settings](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate App Password**:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Other (Custom name)"
   - Name it "CI/CD Dashboard"
   - Copy the generated 16-character password

3. **Update Your .env File**:
   ```bash
   ALERTS_ENABLED=true
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   SMTP_FROM_EMAIL=noreply@cicd-dashboard.com
   SMTP_FROM_NAME=CI/CD Dashboard
   ALERT_DEFAULT_RECIPIENT=renugavelmurugan09@gmail.com
   ```

### **Option 2: Other SMTP Providers**

#### **Outlook/Hotmail**:
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

#### **Yahoo Mail**:
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

#### **Custom SMTP Server**:
```bash
SMTP_HOST=your-smtp-server.com
SMTP_PORT=587
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

## 🔧 Testing Email Configuration

### **1. Test with the Dashboard**:
1. Open your dashboard at `http://localhost:8000`
2. Click the "Test Alert" button in the Alert Configuration section
3. Check your email for the test message

### **2. Test via API**:
```bash
curl -X POST "http://localhost:8000/api/alert/test" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test email alert", "severity": "info"}'
```

### **3. Test with Real Pipeline**:
1. Make a commit and push to your repository
2. Watch the GitHub Actions pipeline run
3. Check your email for success/failure notifications

## 📋 GitHub Repository Secrets

Add these secrets to your GitHub repository:

1. **Go to**: Repository → Settings → Secrets and variables → Actions
2. **Add these secrets**:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DASHBOARD_WEBHOOK_URL` | `https://your-ngrok-url` | Public dashboard URL |
| `DASHBOARD_WRITE_KEY` | Your dashboard WRITE_KEY | Authentication token |

## 🚀 How It Works

### **Pipeline Flow**:
1. **Push Code** → GitHub Actions starts
2. **Pipeline Running** → Dashboard shows "running" status
3. **Pipeline Completes** → Dashboard updates status
4. **Email Sent** → Success/failure notification delivered

### **Email Triggers**:
- ✅ **Success**: Pipeline completes successfully (sends success notification)
- ❌ **Failure**: Pipeline fails (tests fail, build errors, etc.) (sends failure alert)
- ⏱️ **Running**: Pipeline starts (optional notification)
- 📧 **Complete Coverage**: You receive alerts for ALL pipeline results

## 🔍 Troubleshooting

### **Email Not Sending**:
1. Check `.env` file has correct SMTP settings
2. Verify `ALERTS_ENABLED=true`
3. Check server logs for SMTP errors
4. Test SMTP connection manually

### **Gmail Issues**:
1. Ensure 2FA is enabled
2. Use App Password, not regular password
3. Check if "Less secure app access" is disabled (should be)

### **Webhook Issues**:
1. Verify GitHub secrets are set correctly
2. Check dashboard logs for webhook errors
3. Ensure ngrok URL is accessible

## 📱 Email Format

**Success Email Subject**: `CI/CD Dashboard Alert - INFO`

**Success Email Body**:
```
CI/CD Health Dashboard Alert

Severity: INFO
Time: 2025-08-25 15:30:00

Message:
✅ Build #123456789 succeeded on GitHub Actions
Branch: main
Triggered by: username
Duration: 1800s
URL: https://github.com/repo/actions/runs/123456789

---
This is an automated alert from the CI/CD Health Dashboard.
```

**Failure Email Subject**: `CI/CD Dashboard Alert - ERROR`

**Failure Email Body**:
```
CI/CD Health Dashboard Alert

Severity: ERROR
Time: 2025-08-25 15:30:00

Message:
🚨 Build #123456789 failed on GitHub Actions
Branch: main
Triggered by: username
Duration: 1800s
URL: https://github.com/repo/actions/runs/123456789

---
This is an automated alert from the CI/CD Health Dashboard.
```

## 🎉 Next Steps

1. **Configure your .env file** with email settings
2. **Set up GitHub repository secrets**
3. **Test with a commit/push**
4. **Check your email for notifications**

Your CI/CD pipeline will now work normally and send email alerts for real success/failure results!

# 📧 Email Notification Setup Guide

## 🎯 **Email Configuration Complete!**

Your CI/CD Dashboard is now configured to send email notifications to:
**`renugavelmurugan09@gmail.com`**

## ⚠️ **IMPORTANT: Gmail App Password Required**

To make email notifications work, you need to:

### 1. **Enable 2-Factor Authentication on Gmail**
- Go to [Google Account Settings](https://myaccount.google.com/security)
- Enable "2-Step Verification" if not already enabled

### 2. **Generate App Password**
- Go to [Google Account Security](https://myaccount.google.com/apppasswords)
- Select "Mail" and "Other (Custom name)"
- Name it "CI/CD Dashboard"
- Copy the generated 16-character password (it will look like: `abcd efgh ijkl mnop`)

### 3. **Update Your .env File**
Replace `Arvish@09` with the actual app password:

```bash
# Current setting (needs to be updated)
SMTP_PASSWORD=Arvish@09

# Should become (example)
SMTP_PASSWORD=abcd efgh ijkl mnop
```

## 🔧 **Manual Update Command**
```bash
sed 's/SMTP_PASSWORD=Arvish@09/SMTP_PASSWORD=YOUR_ACTUAL_APP_PASSWORD/' .env > .env.new && mv .env.new .env
```

## 📋 **Current Email Configuration**
```env
ALERTS_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=renugavelmurugan09@gmail.com
SMTP_PASSWORD=Arvish@09  # ⚠️ UPDATE THIS with App Password!
SMTP_FROM_EMAIL=renugavelmurugan09@gmail.com
SMTP_FROM_NAME=CI/CD Dashboard - renugavelmurugan09@gmail.com
```

## 🧪 **Test Email Notifications**

Once you've updated the app password, test the email functionality:

```bash
# Test alert endpoint
curl -X POST http://localhost:8000/api/alert/test \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer d447e5b2466828ddda9eed4da0597577" \
  -d '{"message": "Test email notification from CI/CD Dashboard"}'
```

## 📬 **What You'll Receive**

- **Build Failure Alerts**: When any CI/CD pipeline fails
- **Test Notifications**: When you manually test the alert system
- **Pipeline Status Updates**: Important pipeline events

## 🚨 **Troubleshooting**

### **Email Not Sending?**
1. Check if `ALERTS_ENABLED=true`
2. Verify Gmail app password is correct (NOT your regular password)
3. Ensure 2FA is enabled on Gmail
4. Check backend logs for SMTP errors

### **Gmail Security Issues?**
- Gmail blocks regular passwords for SMTP - use App Passwords instead
- Check Gmail spam folder for test emails
- Verify sender email matches your Gmail account

## 🔄 **Restart Required**

After updating the `.env` file, restart your backend server:

```bash
# Stop current server
pkill -f "python run_server.py"

# Start with new config
python run_server.py &
```

## ✅ **Next Steps**

1. **Generate Gmail App Password** (see step 2 above)
2. **Update SMTP_PASSWORD** in `.env` file with the app password
3. **Restart backend server**
4. **Test email notifications**
5. **Trigger a failed build** to see failure alerts

---

**🎉 Your dashboard will now send real-time email notifications for all CI/CD pipeline failures!**

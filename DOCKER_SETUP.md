# 🐳 Docker Setup Guide for CI/CD Pipeline

## 🎯 **Overview**

Your CI/CD pipeline now includes Docker image building and pushing to Docker Hub. This guide will help you set up the required secrets and configuration.

## 🔐 **Required GitHub Secrets**

You need to add these secrets to your GitHub repository:

### 1. **DOCKERUSERNAME**
- **What**: Your Docker Hub username
- **Where**: Go to [GitHub Repository Settings](https://github.com/velu-vm/cicd-health-dashboard/settings/secrets/actions) → Secrets and variables → Actions
- **Example**: `velmurugan` (if your Docker Hub username is velmurugan)

### 2. **DOCKERPASSWORD**
- **What**: Your Docker Hub access token (NOT your login password)
- **How to get it**:
  1. Go to [Docker Hub](https://hub.docker.com/settings/security)
  2. Click "New Access Token"
  3. Name it "CI/CD Dashboard"
  4. Copy the generated token

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
2. Verify Gmail app password is correct
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

## 🚀 **CI/CD Pipeline Flow**

### **Test Job** ✅
- Runs simple tests (no app dependencies)
- Ensures code quality

### **Build Job** 🐳
- Builds Docker image from Dockerfile
- Pushes to Docker Hub with tags:
  - `latest` - Most recent build
  - `{commit-sha}` - Specific commit build

### **Deploy Job** 🚀
- Deploys the built Docker image
- Sends notifications to dashboard

## 📋 **Docker Image Details**

### **Image Name**:
```
{your-docker-username}/cicd-dashboard:latest
{your-docker-username}/cicd-dashboard:{commit-sha}
```

### **What's Included**:
- **Backend**: FastAPI application with all dependencies
- **Frontend**: Static HTML/CSS/JS files
- **Nginx**: Reverse proxy and static file server
- **Database**: SQLite (can be mounted as volume)

## 🔧 **Setup Steps**

### **Step 1: Create Docker Hub Account**
1. Go to [Docker Hub](https://hub.docker.com)
2. Sign up or sign in
3. Note your username

### **Step 2: Generate Access Token**
1. Go to [Docker Hub Security Settings](https://hub.docker.com/settings/security)
2. Click "New Access Token"
3. Name: "CI/CD Dashboard"
4. Copy the token (you won't see it again!)

### **Step 3: Add GitHub Secrets**
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add:
   - **Name**: `DOCKERUSERNAME`
   - **Value**: Your Docker Hub username
5. Add another:
   - **Name**: `DOCKERPASSWORD`
   - **Value**: Your Docker Hub access token

### **Step 4: Test the Pipeline**
1. Push any change to `main` branch
2. Watch GitHub Actions tab
3. Verify Docker image is built and pushed

## 📊 **Expected Results**

### **Successful Build**:
```
✅ Test Job: 13 tests passed
✅ Build Job: Docker image built and pushed
✅ Deploy Job: Deployment completed
```

### **Docker Hub**:
- New image: `{username}/cicd-dashboard:latest`
- Tagged image: `{username}/cicd-dashboard:{sha}`

## 🧪 **Testing Locally**

### **Pull and Run**:
```bash
# Pull the built image
docker pull {your-username}/cicd-dashboard:latest

# Run locally
docker run -d \
  --name cicd-dashboard \
  -p 8080:80 \
  -p 8000:8000 \
  {your-username}/cicd-dashboard:latest
```

### **Access Points**:
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🚨 **Troubleshooting**

### **Build Fails**:
1. Check Docker Hub credentials
2. Verify secrets are set correctly
3. Check Dockerfile syntax

### **Push Fails**:
1. Verify Docker Hub access token
2. Check repository permissions
3. Ensure Docker Hub account is active

### **Deploy Fails**:
1. Check if Docker image was built
2. Verify deployment script
3. Check target environment

## 🔄 **Next Steps**

1. **Set up Docker Hub secrets** (see Step 3 above)
2. **Push to main branch** to trigger pipeline
3. **Monitor GitHub Actions** for build progress
4. **Verify Docker Hub** for new images
5. **Test deployment** with built images

## 📚 **Resources**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Build Action](https://github.com/docker/build-push-action)

---

**🎉 Once configured, every push to main will automatically build and push a new Docker image!**

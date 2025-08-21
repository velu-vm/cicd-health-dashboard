# 🐳 Docker Setup Guide for CI/CD Pipeline

## 🎯 **Overview**

Your CI/CD pipeline now includes Docker image building and pushing to Docker Hub. This guide will help you set up the required secrets and configuration.

## 🔐 **Required GitHub Secrets**

You need to add these secrets to your GitHub repository:

### 1. **DOCKER_USERNAME**
- **What**: Your Docker Hub username
- **Where**: Go to [GitHub Repository Settings](https://github.com/velu-vm/cicd-health-dashboard/settings/secrets/actions) → Secrets and variables → Actions
- **Example**: `velmurugan` (if your Docker Hub username is velmurugan)

### 2. **DOCKER_PASSWORD**
- **What**: Your Docker Hub access token (NOT your login password)
- **How to get it**:
  1. Go to [Docker Hub](https://hub.docker.com/settings/security)
  2. Click "New Access Token"
  3. Name it "CI/CD Dashboard"
  4. Copy the generated token

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
   - **Name**: `DOCKER_USERNAME`
   - **Value**: Your Docker Hub username
5. Add another:
   - **Name**: `DOCKER_PASSWORD`
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

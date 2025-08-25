# Ngrok Setup for CI/CD Dashboard

This document explains how to set up ngrok to expose your local CI/CD dashboard for GitHub webhooks.

## What is ngrok?

Ngrok creates secure tunnels to expose your local development server to the internet, allowing GitHub Actions to send webhooks to your local dashboard.

## Installation

### macOS
```bash
brew install ngrok
```

### Other Platforms
Download from [https://ngrok.com/download](https://ngrok.com/download)

## Setup Steps

1. **Start your dashboard**:
   ```bash
   python run_server.py
   ```

2. **In another terminal, expose with ngrok**:
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abcd-1234.ngrok-free.app`)

4. **Add to GitHub repository secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add `DASHBOARD_WEBHOOK_URL`: `https://your-ngrok-url/api/webhook/github-actions`
   - Add `DASHBOARD_WRITE_KEY`: Your dashboard's WRITE_KEY

## Example ngrok Command

```bash
ngrok http 8000 --log=stdout
```

## Security Notes

- Ngrok URLs change each time you restart ngrok (unless you have a paid account)
- Update your GitHub secrets when the URL changes
- The free tier has limitations on connections per minute

## Troubleshooting

- Make sure your dashboard is running on port 8000
- Check ngrok logs for connection issues
- Verify the webhook URL in GitHub secrets matches exactly

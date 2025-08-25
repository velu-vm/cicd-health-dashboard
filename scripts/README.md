# Scripts Directory

This directory contains essential scripts for the CI/CD Health Dashboard.

## Available Scripts

### `verify.sh`
**Purpose**: Comprehensive API verification and testing script
**Usage**: `./scripts/verify.sh`
**What it does**:
- Tests all backend API endpoints
- Verifies webhook authentication
- Checks database connectivity
- Validates response formats
- Provides detailed test results with color-coded output

**Requirements**:
- Backend server running on port 8000
- `jq` installed for JSON formatting (optional but recommended)
- Valid API key in `API_WRITE_KEY` environment variable

## Script Usage Examples

### Verify API Health
```bash
# Set your API key
export API_WRITE_KEY="your-write-key-here"

# Run verification
./scripts/verify.sh
```

### Install jq (for better JSON formatting)
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

## Notes

- The `verify.sh` script is essential for testing the dashboard after deployment
- It provides comprehensive validation of all API endpoints
- Use this script to troubleshoot any API issues
- The script will exit with error code 1 if any tests fail

# Authentication Setup Guide

Complete guide to setting up authentication for Nano Banana Pro.

---

## Prerequisites

- Google account (for Google AI Studio)
- Databricks workspace access (for MLflow tracking)

---

## Quick Setup (5 Minutes)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Get your API keys (see sections below)
# 3. Edit .env with your credentials
nano .env

# 4. Load environment
source .env

# 5. Verify setup
nano-banana check-auth
```

---

## Step 1: Google AI API Key

**Required for:** Diagram generation and visual analysis

### Getting Your API Key

1. **Go to Google AI Studio**
   - URL: https://aistudio.google.com/app/apikey
   - Click the link to open in your browser

2. **Sign In**
   - Use your Google account (Gmail, Google Workspace, etc.)
   - Accept terms of service if prompted

3. **Create API Key**
   - Click **"Get API Key"** or **"Create API Key"**
   - You'll see options to:
     - **Create API key in new project** (if you don't have a project)
     - **Create API key in existing project** (if you have projects)

4. **Select/Create Project**
   - If new: Enter a project name (e.g., "nano-banana")
   - If existing: Select from dropdown

5. **Copy Your API Key**
   - The key will start with `AIza...`
   - Click the copy button or select and copy manually
   - **Important:** Save this key securely - you won't see it again

6. **Add to .env**
   ```bash
   GEMINI_API_KEY=AIzaSyD...your-actual-key-here...abc123
   ```

### Billing & Quotas

- **Free tier**: Generous free quota for testing
- **Pricing**: Only pay for what you use beyond free quota
- **Rate limits**: Check https://ai.google.dev/pricing for current limits

### Visual Guide

```
Google AI Studio Homepage
┌─────────────────────────────────────────────────┐
│  🔧 Settings              Your Profile ▼        │
├─────────────────────────────────────────────────┤
│                                                  │
│  Get API Key  ← Click here                      │
│  ┌────────────────────────────────────────┐    │
│  │ Create API key in new project          │    │
│  │ Create API key in existing project     │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  After creating:                                │
│  ┌────────────────────────────────────────┐    │
│  │ Your API Key:                          │    │
│  │ AIzaSyD...abc123...xyz789              │    │
│  │                           [Copy] 📋     │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## Step 2: Databricks Credentials

**Required for:** MLflow experiment tracking and artifact storage

### Getting Your Credentials

1. **Go to Your Databricks Workspace**
   - URL format: `https://your-workspace.cloud.databricks.com`
   - Or: `https://your-workspace.azuredatabricks.net` (Azure)
   - Or: `https://your-workspace.gcp.databricks.com` (GCP)

2. **Navigate to Settings**
   - Click your **profile icon** (top right corner)
   - Select **"Settings"** from dropdown

3. **Open Developer Settings**
   - In the left sidebar, find **"Developer"**
   - Click **"Access tokens"**

4. **Generate New Token**
   - Click **"Manage"** or **"Generate new token"**
   - Settings:
     - **Comment**: "Nano Banana Pro" (or any description)
     - **Lifetime**: 90 days (or as needed)
   - Click **"Generate"**

5. **Copy Your Token**
   - The token will start with `dapi...`
   - **Critical:** Copy immediately - you won't see it again
   - Click copy button or select and copy

6. **Note Your Workspace Details**
   - **Workspace URL**: The full URL (e.g., `https://my-workspace.cloud.databricks.com`)
   - **Email/Username**: Your Databricks login email

7. **Add to .env**
   ```bash
   DATABRICKS_HOST=https://my-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=dapi1234567890abcdef...
   DATABRICKS_USER=your.email@company.com
   ```

### Visual Guide

```
Databricks Settings Page
┌─────────────────────────────────────────────────┐
│  Settings                      Your Profile ▼   │
├──────────────┬──────────────────────────────────┤
│ Account      │                                   │
│ Workspace    │  Access Tokens                    │
│ ─────────    │  ─────────────                    │
│ > Developer  │  ┌─────────────────────────────┐ │
│   Access     │  │ Generate new token          │ │
│   tokens     │  └─────────────────────────────┘ │
│              │                                   │
│              │  Active tokens:                   │
│              │  ┌─────────────────────────────┐ │
│              │  │ Comment: Nano Banana Pro    │ │
│              │  │ Created: 2026-01-30         │ │
│              │  │ dapi123...abc [Revoke]      │ │
│              │  └─────────────────────────────┘ │
└──────────────┴──────────────────────────────────┘
```

### Alternative: OAuth Setup

If your organization requires OAuth instead of tokens:

```bash
# Install Databricks CLI
pip install databricks-cli

# Authenticate with OAuth
databricks auth login --host https://your-workspace.cloud.databricks.com

# Credentials stored in ~/.databrickscfg
# Nano Banana will automatically use these
```

---

## Step 3: Configure Environment

### Edit .env File

```bash
# Copy template
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code
```

### Complete Configuration

Your `.env` file should look like:

```bash
# ============================================================================
# Google AI API Key
# ============================================================================
GEMINI_API_KEY=AIzaSyD...your-actual-key-here...abc123

# ============================================================================
# Databricks Configuration
# ============================================================================
DATABRICKS_HOST=https://my-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef...your-actual-token...
DATABRICKS_USER=your.email@company.com

# ============================================================================
# Optional: GCP Project (usually not needed)
# ============================================================================
# GCP_PROJECT_ID=your-project-id
```

### Load Environment

**Every time you start a new terminal session:**

```bash
source .env
```

**Make it automatic** (optional):

```bash
# Add to your shell profile (~/.bashrc or ~/.zshrc)
echo 'source ~/path/to/nano_banana/.env' >> ~/.bashrc

# Or use direnv (recommended)
brew install direnv
echo 'source .env' > .envrc
direnv allow
```

---

## Step 4: Verify Setup

```bash
nano-banana check-auth
```

**Expected output:**

```
✓ Google AI API key configured
✓ Databricks credentials configured
✓ MLflow connection successful

Everything looks good! You're ready to generate diagrams.
```

**If there are errors:**

```
✗ Google AI API key not found
  Set GEMINI_API_KEY or GOOGLE_CLOUD_API_KEY environment variable

✗ Databricks credentials not configured
  Set DATABRICKS_HOST, DATABRICKS_TOKEN, and DATABRICKS_USER

✗ MLflow connection failed: Authentication error
  Check your Databricks token is valid and not expired
```

---

## Troubleshooting

### Google AI API Key Issues

#### "API key not found"

**Problem:** Environment variable not set

**Solution:**
```bash
# Check if variable is set
echo $GEMINI_API_KEY

# If empty, reload .env
source .env

# Verify
echo $GEMINI_API_KEY  # Should show your key
```

#### "Invalid API key"

**Problem:** Key is incorrect or expired

**Solution:**
1. Go back to https://aistudio.google.com/app/apikey
2. Verify your key or generate a new one
3. Update `.env` with new key
4. Reload: `source .env`

#### "Quota exceeded"

**Problem:** Hit free tier limits

**Solution:**
1. Check usage at https://aistudio.google.com
2. Enable billing if needed
3. Wait for quota reset (usually daily)

### Databricks Issues

#### "Connection failed"

**Problem:** Incorrect host URL

**Solution:**
```bash
# Verify URL format (no trailing slash)
DATABRICKS_HOST=https://my-workspace.cloud.databricks.com  ✓
DATABRICKS_HOST=https://my-workspace.cloud.databricks.com/ ✗

# Test connection
curl -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  "$DATABRICKS_HOST/api/2.0/clusters/list"
```

#### "Authentication error"

**Problem:** Invalid or expired token

**Solution:**
1. Go to Databricks → Settings → Developer → Access tokens
2. Check if token is expired
3. Generate new token if needed
4. Update `.env` and reload

#### "MLflow experiment not found"

**Problem:** Experiment path doesn't exist

**Solution:**
```bash
# Let nano-banana create it automatically
nano-banana verify-setup

# Or create manually in Databricks UI
# Navigate to: Machine Learning → Experiments
# Click "Create Experiment"
```

### Permission Issues

#### "Insufficient permissions"

**Problem:** Token doesn't have required permissions

**Solution:**
1. Contact your Databricks admin
2. Request permissions for:
   - Create MLflow experiments
   - Log MLflow runs
   - Upload artifacts
3. Or use a different workspace where you have admin rights

---

## Security Best Practices

### Protect Your API Keys

```bash
# NEVER commit .env to git
echo ".env" >> .gitignore

# Verify it's ignored
git status  # .env should not appear

# Check if accidentally committed
git log --all --full-history -- .env
```

### Rotate Keys Regularly

```bash
# Every 90 days:
# 1. Generate new Google AI key
# 2. Generate new Databricks token
# 3. Update .env
# 4. Test with nano-banana check-auth
# 5. Revoke old keys
```

### Use Different Keys Per Environment

```bash
# Development
.env.dev
GEMINI_API_KEY=AIza...dev-key...

# Production
.env.prod
GEMINI_API_KEY=AIza...prod-key...

# Load appropriate environment
source .env.dev
```

---

## Alternative Authentication Methods

### 1. Environment Variables Only

Skip `.env` file and set variables directly:

```bash
export GEMINI_API_KEY="AIza..."
export DATABRICKS_HOST="https://..."
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_USER="your.email@company.com"

nano-banana check-auth
```

### 2. Databricks CLI Config

Use existing Databricks CLI configuration:

```bash
# Setup via CLI
databricks configure --token

# Nano Banana will automatically detect ~/.databrickscfg
```

### 3. Azure CLI (for Azure Databricks)

```bash
# Login with Azure CLI
az login

# Nano Banana will use Azure credentials automatically
```

### 4. GCP Application Default Credentials

For Vertex AI (not usually needed):

```bash
gcloud auth application-default login
```

---

## Verification Checklist

Before generating your first diagram:

- [ ] Google AI API key obtained from https://aistudio.google.com/app/apikey
- [ ] Databricks token generated from workspace settings
- [ ] `.env` file created and populated
- [ ] Environment loaded with `source .env`
- [ ] `nano-banana check-auth` shows all green checkmarks
- [ ] `.env` added to `.gitignore`

---

## Quick Reference

### Key Sources

| Service | Get Keys From | Variable Name |
|---------|---------------|---------------|
| Google AI | https://aistudio.google.com/app/apikey | `GEMINI_API_KEY` |
| Databricks | Workspace Settings → Developer → Access tokens | `DATABRICKS_TOKEN` |

### Environment Variables

```bash
# Required
GEMINI_API_KEY=AIza...           # Google AI Studio
DATABRICKS_HOST=https://...      # Databricks workspace URL
DATABRICKS_TOKEN=dapi...         # Databricks token
DATABRICKS_USER=user@email.com   # Your email

# Optional
GCP_PROJECT_ID=project-id        # Only if using Vertex AI directly
```

### Verify Commands

```bash
source .env                      # Load environment
nano-banana check-auth           # Verify all credentials
echo $GEMINI_API_KEY            # Check Google AI key
echo $DATABRICKS_TOKEN          # Check Databricks token
```

---

## Need Help?

### Common Issues

1. **"Command not found: nano-banana"**
   - Solution: Activate venv: `source .venv/bin/activate`

2. **"ModuleNotFoundError"**
   - Solution: Install deps: `uv pip install -e .`

3. **"API rate limit exceeded"**
   - Solution: Wait a few minutes or check your quota

4. **"Experiment path not found"**
   - Solution: Run `nano-banana verify-setup` to auto-create

### Resources

- Google AI Studio: https://aistudio.google.com
- Databricks Docs: https://docs.databricks.com
- API Pricing: https://ai.google.dev/pricing
- Issue Tracker: See repository issues

---

**You're now ready to generate diagrams!** 🎉

Next step: [Generate your first diagram](../../README.md#generate-your-first-diagram)

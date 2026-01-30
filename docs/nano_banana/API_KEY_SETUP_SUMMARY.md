# API Key Setup - What's New

## Summary of Changes

Added comprehensive instructions for obtaining and configuring API keys for Nano Banana Pro.

---

## What Was Added

### 1. **Enhanced README.md**

Added a complete "Get Your API Keys" section with:
- **Google AI API Key**: Step-by-step guide to get key from Google AI Studio
- **Databricks Credentials**: How to generate access tokens
- **Configuration**: How to set up `.env` file
- **Verification**: How to check everything is working

**Location:** Right after "Installation" section in README.md

### 2. **Updated .env.example**

Completely rewrote with:
- Clear section headers (Required vs Optional)
- Detailed comments explaining each variable
- Step-by-step instructions for getting keys
- Links to relevant pages
- Verification instructions at the bottom

**Key improvements:**
```bash
# Before
GEMINI_API_KEY=your-gemini-api-key-here

# After
# ============================================================================
# REQUIRED: Google AI API Key (for Gemini image generation and analysis)
# ============================================================================
# Get your API key from: https://aistudio.google.com/app/apikey
# 1. Sign in with your Google account
# 2. Click "Get API Key" or "Create API Key"
# 3. Select or create a project
# 4. Copy the key (starts with AIza...)
#
GEMINI_API_KEY=AIza...your-key-here...
```

### 3. **Updated CLAUDE.md**

Enhanced authentication section with:
- Quick setup commands
- "Getting Your API Keys" subsections
- Direct links to Google AI Studio and Databricks
- Clear step-by-step instructions

### 4. **New: Complete Authentication Guide**

Created `docs/nano_banana/AUTHENTICATION.md` - a comprehensive guide covering:

**Contents:**
- ✅ Prerequisites
- ✅ Quick setup (5 minutes)
- ✅ Step-by-step Google AI key setup with visual guides
- ✅ Step-by-step Databricks setup with visual guides
- ✅ Environment configuration
- ✅ Verification steps
- ✅ Troubleshooting section
- ✅ Security best practices
- ✅ Alternative authentication methods
- ✅ Verification checklist
- ✅ Quick reference table

**Highlights:**
- Visual ASCII diagrams showing UI navigation
- Common error messages and solutions
- Security best practices (key rotation, .gitignore, etc.)
- Alternative auth methods (OAuth, Azure CLI, GCP ADC)
- Quick reference table

---

## Quick Links for Users

### Getting Started

1. **Quick setup:** See README.md → "Get Your API Keys"
2. **Detailed guide:** See [AUTHENTICATION.md](AUTHENTICATION.md)
3. **Environment template:** Copy [.env.example](../../.env.example)

### Key URLs

| Service | URL |
|---------|-----|
| **Google AI Studio** | https://aistudio.google.com/app/apikey |
| **Databricks** | `https://your-workspace.cloud.databricks.com` → Settings → Developer → Access tokens |

---

## User Journey

### For First-Time Users

```
1. Read: README.md → "Get Your API Keys"
   ├─→ Follow inline instructions
   └─→ Get keys in ~5 minutes

2. Configure: Copy .env.example to .env
   ├─→ .env.example has detailed comments
   └─→ Paste in your keys

3. Verify: nano-banana check-auth
   └─→ Should show all green checkmarks

4. Generate: nano-banana generate ...
```

### For Users Needing Help

```
1. Something not working?
   └─→ Read: docs/nano_banana/AUTHENTICATION.md

2. Still stuck?
   └─→ Check: Troubleshooting section
       ├─→ Common error messages
       ├─→ Step-by-step fixes
       └─→ Verification commands

3. Security questions?
   └─→ Read: Security Best Practices section
```

---

## Example: Complete Setup Flow

```bash
# 1. Clone repo and install
git clone <repo>
cd nano_banana
uv venv && source .venv/bin/activate
uv pip install -e .

# 2. Get Google AI key
# Go to: https://aistudio.google.com/app/apikey
# Click "Get API Key"
# Copy key (starts with AIza...)

# 3. Get Databricks credentials
# Go to: https://your-workspace.cloud.databricks.com
# Settings → Developer → Access tokens
# Generate token, copy (starts with dapi...)

# 4. Configure
cp .env.example .env
nano .env  # Paste keys

# 5. Load and verify
source .env
nano-banana check-auth
# Output:
# ✓ Google AI API key configured
# ✓ Databricks credentials configured

# 6. Generate first diagram!
nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template baseline
```

---

## Documentation Structure

```
docs/nano_banana/
├── AUTHENTICATION.md              # ← NEW: Complete auth guide
│   ├── Prerequisites
│   ├── Step 1: Google AI API Key
│   ├── Step 2: Databricks Credentials
│   ├── Step 3: Configure Environment
│   ├── Step 4: Verify Setup
│   ├── Troubleshooting
│   ├── Security Best Practices
│   └── Quick Reference
│
├── LOGO_SETUP.md                  # Logo configuration
├── PROMPT_REFINEMENT.md           # Visual refinement guide
└── VISUAL_REFINEMENT_QUICKSTART.md # Refinement quick start

README.md                          # ← UPDATED: Added "Get Your API Keys"
CLAUDE.md                          # ← UPDATED: Enhanced auth section
.env.example                       # ← UPDATED: Detailed comments
```

---

## Key Features

### 1. Progressive Disclosure

- **Quick path:** README has inline 5-minute setup
- **Detailed path:** AUTHENTICATION.md has comprehensive guide
- **Reference path:** .env.example has inline comments

### 2. Visual Guides

ASCII diagrams show UI navigation:
```
Google AI Studio Homepage
┌─────────────────────────────────────────────────┐
│  Get API Key  ← Click here                      │
│  ┌────────────────────────────────────────┐    │
│  │ Your API Key:                          │    │
│  │ AIzaSyD...abc123...xyz789              │    │
│  │                           [Copy] 📋     │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 3. Troubleshooting

Common issues with solutions:
- "API key not found" → Check environment
- "Invalid API key" → Regenerate key
- "Quota exceeded" → Check billing
- "Connection failed" → Verify URL format
- "Authentication error" → Check token expiry

### 4. Security Best Practices

- How to protect keys
- Key rotation schedule
- .gitignore setup
- Different keys per environment

### 5. Quick Reference

Table format for easy lookup:
| Service | Get Keys From | Variable Name |
|---------|---------------|---------------|
| Google AI | https://aistudio.google.com/app/apikey | `GEMINI_API_KEY` |
| Databricks | Settings → Developer → Access tokens | `DATABRICKS_TOKEN` |

---

## Files Modified

1. ✅ `README.md` - Added "Get Your API Keys" section
2. ✅ `.env.example` - Complete rewrite with detailed comments
3. ✅ `CLAUDE.md` - Enhanced authentication section
4. ✅ `docs/nano_banana/AUTHENTICATION.md` - NEW: Complete guide

---

## Benefits

### For New Users
- Can get started in 5 minutes
- Clear step-by-step instructions
- Visual guides reduce confusion
- Verification step confirms success

### For Experienced Users
- Quick reference available
- Alternative auth methods documented
- Security best practices included
- Troubleshooting for edge cases

### For Teams
- Consistent setup process
- Security guidelines to follow
- Documentation to share
- Common pitfalls covered

---

## Testing Checklist

To verify the instructions work:

- [ ] Can a new user follow README → "Get Your API Keys" and succeed?
- [ ] Does .env.example have clear enough comments?
- [ ] Do the verification steps (`nano-banana check-auth`) work?
- [ ] Are troubleshooting steps accurate?
- [ ] Are all URLs correct and working?
- [ ] Are security best practices clear?

---

## Next Steps for Users

After authentication setup:

1. ✅ **Generate first diagram**
   ```bash
   nano-banana generate --diagram-spec prompts/diagram_specs/example_basic.yaml --template baseline
   ```

2. ✅ **Try visual refinement** (NEW feature)
   ```bash
   nano-banana refine-prompt --run-id <run-id> --feedback "logos too small"
   ```

3. ✅ **Read guides**
   - [LOGO_SETUP.md](LOGO_SETUP.md) - Logo configuration
   - [PROMPT_REFINEMENT.md](PROMPT_REFINEMENT.md) - Visual refinement

---

**Authentication is now fully documented and easy to set up!** 🔑

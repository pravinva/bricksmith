# 🚀 Start Here: DSPy Batch Refinement with MCP Integration

## What You Have

You asked: "Why can't DSPy work with my MCP server?"

**Answer:** It can! But you need to understand you have **two different MCP servers**:

1. **Databricks Docs MCP** (Docker) - For documentation searches ✅ Already running
2. **DSPy Proxy MCP** (New) - For batch API proxying ➕ Need to start this

**Read first:** [`TWO_MCP_SERVERS_EXPLAINED.md`](TWO_MCP_SERVERS_EXPLAINED.md) for a clear explanation.

---

## 🎯 Your Goal

Process 200 AGL RFP responses through DSPy while routing all API calls through your local MCP server for visibility and control.

---

## ⚡ Quick Start (3 Steps)

### Step 1: Start DSPy Proxy MCP Server

```bash
cd /Users/david.okeeffe/databricks-sandbox/nano_banana

# Easy way (recommended)
./start-dspy-proxy.sh

# Or manually
python local_mcp_server.py
```

You should see:
```
🚀 Starting DSPy MCP Server
Server will run on: http://0.0.0.0:8001
```

**Keep this terminal open!**

### Step 2: Expose to Databricks (New Terminal)

```bash
# Install ngrok if needed
brew install ngrok

# Expose port 8001
ngrok http 8001

# Copy the HTTPS URL
# Example: https://abc123.ngrok.io
```

**Keep this terminal open too!**

### Step 3: Run Batch Refinement in Databricks

1. Open `agl_rfp_dspy_with_mcp.py` in Databricks
2. Update the MCP server URL:
   ```python
   MCP_SERVER_URL = "https://abc123.ngrok.io"  # Your ngrok URL
   ```
3. Set batch mode:
   ```python
   BATCH_MODE = "DEMO"  # Test with 5 responses first
   ```
4. Run all cells

**Watch your MCP server terminal** - you'll see all DSPy requests flowing through! 🎉

---

## 📊 What You'll See

### In Your MCP Server Terminal:

```
================================================================================
📥 REQUEST abc12345
   Endpoint: databricks-claude-sonnet-4-5
   Messages: 1
   Prompt length: 1542 characters
   Max tokens: 2000
   Temperature: 0.1
🔄 Forwarding to Databricks Model Serving API...
✅ SUCCESS abc12345
   Response length: 823 characters
   Response time: 2.34s
📤 RESPONSE abc12345
================================================================================
```

### In Databricks Notebook:

```
[1/5] (20.0%) | Elapsed: 0.5m | ETA: 2.0m | RFP: Q001
  ✓ Complete (2.3s)
```

### After DEMO Mode (5 responses):

Check statistics:
```bash
curl http://localhost:8001/stats

# Returns:
{
  "total_requests": 15,        # 3 stages × 5 responses
  "total_tokens": 8145,
  "average_response_time_seconds": 2.1
}
```

---

## 📁 Files Guide

### Core Files (Use These)

| File | What It Does |
|------|-------------|
| `agl_rfp_dspy_with_mcp.py` | 📓 Databricks notebook with DSPy + MCP integration |
| `local_mcp_server.py` | 🔄 DSPy proxy server (run locally) |
| `start-dspy-proxy.sh` | 🚀 Easy startup script |

### Documentation (Read These)

| File | What It Explains |
|------|-----------------|
| `START_HERE.md` | 👉 This file - where to begin |
| `TWO_MCP_SERVERS_EXPLAINED.md` | 📚 Explains your two MCP servers |
| `DSPY_MCP_INTEGRATION_GUIDE.md` | 🔧 Technical deep dive |
| `MCP_DOCKER_SETUP_GUIDE.md` | 🐳 Docker setup options |

### Optional Files

| File | What It's For |
|------|--------------|
| `Dockerfile.dspy-proxy` | 🐳 Docker image for proxy (optional) |
| `docker-compose-mcp.yml` | 🐳 Docker Compose setup (optional) |

---

## 🎓 Understanding the Flow

```
Databricks Notebook (agl_rfp_dspy_with_mcp.py)
    ↓
DSPy Refinement Agent
    ↓ (3 stages per response)
MCPServerLM (custom LM class)
    ↓
Your Local MCP Server (localhost:8001)
    ↓ (via ngrok)
Databricks Model Serving API
    ↓
Claude Sonnet 4.5
    ↓
Response flows back through MCP
    ↓
DSPy receives refined text
```

**For 200 responses:**
- 3 stages × 200 responses = **600 API calls** through your MCP server
- Estimated time: **100-200 minutes**
- Cost: **~$2.70** (same as direct API)

---

## ✅ Checklist

Before running batch refinement:

- [ ] Databricks Docs MCP is running in Docker (check: `docker ps | grep databricks-mcp-server`)
- [ ] Started DSPy Proxy MCP (`./start-dspy-proxy.sh`)
- [ ] Started ngrok (`ngrok http 8001`)
- [ ] Copied ngrok HTTPS URL
- [ ] Updated `MCP_SERVER_URL` in Databricks notebook
- [ ] Set `BATCH_MODE = "DEMO"` for testing
- [ ] Both terminals (proxy + ngrok) are open and running

---

## 🐛 Troubleshooting

### "Connection refused" in Databricks

**Check:**
```bash
# Is proxy running?
curl http://localhost:8001/health

# Is ngrok running?
curl https://your-ngrok-url.ngrok.io/health
```

**Fix:** Make sure both terminals are still open and running.

### Port 8001 already in use

**Fix:**
```bash
# The start script will automatically use 8002 if 8001 is busy
./start-dspy-proxy.sh
```

### Want to see what's happening

**Monitor:**
```bash
# In the terminal where proxy is running, you'll see live logs

# Or check statistics
curl http://localhost:8001/stats
```

---

## 🎯 After Testing (DEMO Mode)

Once DEMO mode works (5 responses):

1. ✅ **Verify results** in Databricks output
2. ✅ **Check MCP server logs** - did all 15 requests succeed?
3. ✅ **Review refined responses** for quality
4. ✅ **Switch to FULL mode:**
   ```python
   BATCH_MODE = "FULL"  # Process all 200 responses
   ```
5. ✅ **Run batch refinement** (~2-3 hours)
6. ✅ **Check final results** in Delta table

---

## 🎉 What You Get

After setup:

✅ **All DSPy calls** route through your MCP server
✅ **Full visibility** - see every prompt and response
✅ **Custom logging** - all requests stored locally
✅ **Statistics** - track tokens, timing, success rate
✅ **Same DSPy features** - ChainOfThought, Signatures, 3-stage pipeline
✅ **Production-ready** - 200 RFP responses refined with AGL + Databricks context

---

## 📞 Quick Commands Reference

```bash
# Start proxy
./start-dspy-proxy.sh

# Start ngrok
ngrok http 8001

# Check health
curl http://localhost:8001/health

# View statistics
curl http://localhost:8001/stats

# Check proxy logs (if running in Docker)
docker logs -f dspy-proxy

# Stop proxy (if running in Docker)
docker stop dspy-proxy
```

---

## 🚦 Status Check

Run these to verify everything is working:

```bash
# 1. Check Databricks Docs MCP (existing)
docker ps | grep databricks-mcp-server
# Should show running container

# 2. Check DSPy Proxy MCP (new)
curl http://localhost:8001/health
# Should return: {"status":"healthy",...}

# 3. Check ngrok
curl https://your-ngrok-url.ngrok.io/health
# Should return: {"status":"healthy",...}

# All three working? You're ready to go! 🎉
```

---

## 🎓 Remember

- **Databricks Docs MCP** (Docker) = For Claude Code documentation searches
- **DSPy Proxy MCP** (Local) = For DSPy batch API proxying
- They're **independent** and both can run simultaneously
- Your **existing MCP config** stays unchanged

---

## Next Step

**Read:** [`TWO_MCP_SERVERS_EXPLAINED.md`](TWO_MCP_SERVERS_EXPLAINED.md)

Then follow the Quick Start above! 🚀

---

**Created:** 2026-01-18
**Purpose:** Clear starting point for DSPy batch refinement with MCP integration
**Time to setup:** ~5 minutes
**Time for 200 responses:** ~2-3 hours

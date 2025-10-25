# 🚀 Hugging Face Spaces Deployment Guide

## 📋 Prerequisites

1. ✅ Hugging Face account (free) - [Sign up here](https://huggingface.co/join)
2. ✅ Groq API key (free) - [Get it here](https://console.groq.com/keys)
3. ✅ Your GitHub repository: https://github.com/MehediGit98/rag-policy-chatbot

## 🎯 Deployment Steps

### Step 1: Create New Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configure:
   - **Owner**: Your username
   - **Space name**: `policy-assistant` (or your preferred name)
   - **License**: MIT
   - **Select the SDK**: **Gradio**
   - **SDK version**: 4.0.0 (or latest)
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public (or Private if you prefer)
4. Click **"Create Space"**

### Step 2: Clone Your Space Repository

```bash
# Clone the newly created space
git clone https://huggingface.co/spaces/YOUR_USERNAME/policy-assistant
cd policy-assistant
```

### Step 3: Copy Project Files

You have two options:

#### Option A: Manual File Copy (Recommended)

```bash
# From your project directory
cd /path/to/rag-policy-chatbot

# Copy the new app.py (Gradio version)
cp app.py ../policy-assistant/

# Copy requirements.txt (HF version)
cp requirements.txt ../policy-assistant/

# Copy README.md (HF version)
cp README.md ../policy-assistant/

# Copy source code
cp -r src ../policy-assistant/

# Copy policy documents
cp -r data ../policy-assistant/

# Optional: Copy pre-built vector store (faster startup)
# If you have it built locally
cp -r chroma_db ../policy-assistant/
```

#### Option B: Clone and Replace

```bash
# Clone your GitHub repo
git clone https://github.com/MehediGit98/rag-policy-chatbot
cd rag-policy-chatbot

# Copy files to HF Space
cp app.py /path/to/policy-assistant/
cp requirements.txt /path/to/policy-assistant/
cp README.md /path/to/policy-assistant/
cp -r src /path/to/policy-assistant/
cp -r data /path/to/policy-assistant/
```

### Step 4: Update Your GitHub Repository First

Before deploying to HF, update your GitHub repo with the new files:

```bash
# In your GitHub repo directory
cd /path/to/rag-policy-chatbot

# Create a new branch for HF deployment
git checkout -b huggingface-deployment

# Add the new files (they're in the artifacts above)
# You'll need to create these files from the artifacts:
# - app.py (Gradio version)
# - requirements.txt (HF version)
# - README.md (HF version)
# - HF_DEPLOYMENT_GUIDE.md (this file)

git add app.py requirements.txt README.md HF_DEPLOYMENT_GUIDE.md
git commit -m "Add Hugging Face Spaces deployment files"
git push origin huggingface-deployment

# Optionally merge to main
git checkout main
git merge huggingface-deployment
git push origin main
```

### Step 5: Commit and Push to HF Space

```bash
# Go to your HF Space directory
cd /path/to/policy-assistant

# Add all files
git add .

# Commit
git commit -m "Initial deployment of RAG Policy Assistant"

# Push to Hugging Face
git push
```

### Step 6: Add Secrets

1. Go to your Space on HF: `https://huggingface.co/spaces/YOUR_USERNAME/policy-assistant`
2. Click **"Settings"** tab
3. Scroll to **"Repository secrets"**
4. Click **"New secret"**
5. Add:
   - **Name**: `GROQ_API_KEY`
   - **Value**: `gsk_your_actual_api_key_here`
6. Click **"Add secret"**

### Step 7: Monitor Build

1. Go to the **"Logs"** tab in your Space
2. Watch the build process (takes 3-5 minutes)
3. Look for:
   ```
   ✅ Installing dependencies...
   ✅ Initializing RAG system...
   ✅ Running on http://0.0.0.0:7860
   ```

### Step 8: Test Your Deployment

1. Once build completes, go to the **"App"** tab
2. You'll see the Gradio interface
3. Try example questions:
   - "How many PTO days do employees get?"
   - "What is the remote work policy?"
   - "How do I submit expense reports?"

## 🎨 Expected Interface

Your deployed app will have:

- 🤖 Beautiful chat interface with message history
- 📚 Source citations for every answer
- ⚡ Fast responses (< 3 seconds)
- 💡 Example questions to get started
- ℹ️ System information panel

## 📁 Required File Structure

Your HF Space repository should look like:

```
policy-assistant/
├── app.py                          # Gradio interface (new)
├── requirements.txt                # HF dependencies (new)
├── README.md                       # HF Space card (new)
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── retrieval.py
│   └── evaluation.py
├── data/
│   └── policies/
│       ├── pto_policy.md
│       ├── remote_work_policy.md
│       ├── expense_policy.md
│       ├── security_policy.md
│       └── holiday_policy.md
└── chroma_db/                      # Optional (built at runtime if missing)
    └── [vector store files]
```

## 🔧 Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure `src/` folder is committed:
```bash
git add src/
git commit -m "Add src folder"
git push
```

### "System not initialized"

**Error**: RAG system fails to initialize

**Solutions**:
1. Check logs for specific error
2. Verify `GROQ_API_KEY` is set correctly in secrets
3. Ensure `data/policies/` folder exists with markdown files
4. Try restarting the Space (Settings → Factory reboot)

### Slow First Response

**Expected**: First query after deployment takes 20-30 seconds

**Why**: Vector store is being built from scratch

**Solution**: Commit pre-built `chroma_db/` folder to skip this step

### Out of Memory

**Unlikely on HF Spaces** (16GB RAM available)

**If it happens**:
1. Pre-build and commit `chroma_db/` folder
2. Reduce `CHUNK_SIZE` in `src/config.py`
3. Use smaller embedding model (already using smallest)

## 🎯 Performance Expectations

| Metric | Expected Value |
|--------|---------------|
| Build Time | 3-5 minutes |
| First Query | 20-30 seconds (cold start) |
| Subsequent Queries | 1-3 seconds |
| Memory Usage | ~1-2 GB |
| Uptime | 99.9% |

## 🌟 Post-Deployment

### Verify Everything Works

```bash
# Test health (not applicable for Gradio, but you can chat)
# Just open the Space URL and ask questions

# Test a query
# Use the web interface or curl:
curl -X POST https://YOUR_USERNAME-policy-assistant.hf.space/call/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["How many PTO days do employees get?", []]}'
```

### Share Your Space

1. Copy the Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/policy-assistant`
2. Share with your team
3. Embed in websites using the embed code (Settings → Embed)

### Update Policies

When you need to update policy documents:

```bash
# Update files in your local repo
cd /path/to/policy-assistant

# Edit policy files
nano data/policies/pto_policy.md

# Commit and push
git add data/policies/
git commit -m "Update PTO policy"
git push

# HF will automatically rebuild!
```

## 🎨 Customization

### Change Theme

Edit `app.py`:
```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    # Options: Soft, Base, Default, Glass, Monochrome
```

### Add More Examples

Edit `app.py`:
```python
gr.Examples(
    examples=[
        "Your new example question?",
        "Another example?",
    ],
    inputs=msg,
)
```

### Modify System Message

Edit `app.py` in the `gr.Markdown()` section

## 📞 Support

- **HF Spaces Issues**: https://huggingface.co/spaces/YOUR_USERNAME/policy-assistant/discussions
- **Code Issues**: https://github.com/MehediGit98/rag-policy-chatbot/issues
- **Groq API Issues**: https://console.groq.com/docs

## ✅ Final Checklist

- [ ] HF account created
- [ ] Space created
- [ ] All files copied from GitHub repo
- [ ] `GROQ_API_KEY` added to secrets
- [ ] Files committed and pushed
- [ ] Build completed successfully
- [ ] Can ask questions and get answers
- [ ] Citations are showing
- [ ] Response time is reasonable (< 5 seconds)

## 🎉 Success!

Your RAG Policy Assistant is now live on Hugging Face Spaces!

**Next Steps**:
1. Test thoroughly with various questions
2. Share with your team
3. Monitor usage in HF dashboard
4. Update policies as needed
5. Consider upgrading to better hardware if needed (still free for most use)

**Your Space URL**:
`https://huggingface.co/spaces/YOUR_USERNAME/policy-assistant`

---

Need help? Check the troubleshooting section or create an issue in your GitHub repo!
 Complete Setup Guide - FREE Models (8GB RAM Compatible)

## 🎯 System Requirements

✅ **Your Hardware:**
- 8GB RAM (Sufficient!)
- 4GB NVIDIA GPU (Not needed, we'll use CPU)
- Internet connection for initial model download

✅ **What You Need:**
- **FREE Groq API Key** (No credit card required!)
- **NO** OpenAI account needed
- **NO** paid APIs
- **NO** HuggingFace token for deployment

---

## Step 1: Get FREE Groq API Key (2 minutes)

Groq provides **FREE** LLM API access with NO credit card required!

1. Go to: **https://console.groq.com**
2. Click "Sign Up" (use Google/GitHub)
3. Go to: **https://console.groq.com/keys**
4. Click "Create API Key"
5. Copy your key (starts with `gsk_...`)

**Free Tier Limits:**
- 30 requests/minute
- 14,400 requests/day
- More than enough for development and demo!

---

## Step 2: Project Setup (10 minutes)

### Create Project Structure

```bash
# Create project
mkdir rag-policy-chatbot
cd rag-policy-chatbot

# Create directories
mkdir -p src data/policies static templates tests evaluation .github/workflows

# Create __init__.py files
touch src/__init__.py tests/__init__.py
```

### Copy All Files

Copy these files from the artifacts:

**Core Files:**
- `requirements.txt` → root
- `.env.example` → root
- `.gitignore` → root
- `render.yaml` → root

**Source Code:**
- `src/config.py` → src/
- `src/ingestion.py` → src/ 
- `src/retrieval.py` → src/
- `src/evaluation.py` → src/ 

**Frontend:**
- `templates/index.html` → templates/
- `static/style.css` → static/
- `static/script.js` → static/

**Application:**
- `app.py` → root 

**Tests:**
- `tests/test_app.py` → tests/

**CI/CD:**
- `.github/workflows/deploy.yml` → .github/workflows/

**Policy Documents:**
- All 5 policy .md files → data/policies/

**Evaluation:**
- `evaluation/evaluation_questions.json` → evaluation/
- `evaluation/run_evaluation.py` → evaluation/

---

## Step 3: Local Setup (15 minutes)

### 3.1 Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3.2 Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt
```

**First install will download:**
- sentence-transformers model (~80MB)
- PyTorch CPU version (~200MB)

**Total download:** ~300MB
**Time:** 5-10 minutes on good internet

### 3.3 Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit .env file
nano .env  # or use your editor
```

**Add your Groq API key:**
```env
USE_GROQ=true
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.2-3b-preview
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 3.4 Ingest Documents

```bash
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"
```

**Expected output:**
```
Starting document ingestion...
Loaded: pto_policy.md
Loaded: remote_work_policy.md
...
Creating vector store...
Vector store created successfully!
```

**This creates:** `chroma_db/` folder with embeddings (~5MB)

### 3.5 Test Locally

```bash
python app.py
```

**Expected output:**
```
========================================================
RAG System Configuration (FREE Models)
========================================================
LLM Provider:      Groq (Free)
LLM Model:         llama-3.2-3b-preview
Embedding Model:   sentence-transformers/all-MiniLM-L6-v2
API Key Set:       ✅
========================================================
Loading embedding model (local, no API)...
✅ Embedding model loaded
Loading vector store...
✅ Vector store loaded
Initializing Groq LLM (free API)...
✅ Groq LLM initialized
 * Running on http://127.0.0.1:5000
```

**Visit:** http://localhost:5000

**Test questions:**
- "How many PTO days do employees get?"
- "What is the remote work policy?"
- "What is the expense reimbursement limit?"

---

## Step 4: Run Tests (5 minutes)

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v
```

**Expected:** All tests should pass (some may skip if RAG not initialized)

---

## Step 5: GitHub Setup (5 minutes)

### 5.1 Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: Free RAG chatbot"
```

### 5.2 Create GitHub Repository

1. Go to https://github.com/new
2. Name: `rag-policy-chatbot`
3. **Don't** initialize with README
4. Click "Create repository"

### 5.3 Push to GitHub

```bash
git remote add origin https://github.com/MehediGit98/rag-policy-chatbot.git
git branch -M main
git push -u origin main
```

### 5.4 Add Collaborator

1. Go to: Settings → Collaborators
2. Add: `quantic-grader`

---

## Step 6: Deploy to Render (15 minutes)

### 6.1 Create Render Account

1. Go to: https://render.com
2. Sign up with GitHub
3. Authorize Render

### 6.2 Create Web Service

1. Click "New +" → "Web Service"
2. Connect your repository: `rag-policy-chatbot`
3. Click "Connect"

### 6.3 Configure Service

**Basic Settings:**
```
Name: rag-policy-chatbot
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Instance Type: Free
```

**Build Command:**
```bash
pip install -r requirements.txt && python -c 'from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()'
```

**Start Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --worker-class gthread
```

### 6.4 Add Environment Variables

Click "Advanced" → Add these:

```
GROQ_API_KEY = gsk_your_groq_key_here
USE_GROQ = true
GROQ_MODEL = llama-3.2-3b-preview
EMBEDDING_MODEL = sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE = 400
CHUNK_OVERLAP = 40
TOP_K = 3
MAX_TOKENS = 400
TEMPERATURE = 0.3
```

### 6.5 Deploy!

1. Click "Create Web Service"
2. Wait 10-15 minutes for first build
3. Render will:
   - Download dependencies
   - Download embedding model
   - Ingest documents
   - Start application

**Your app will be at:** `https://rag-policy-chatbot.onrender.com`

### 6.6 Verify Deployment

```bash
# Test health
curl https://rag-policy-chatbot.onrender.com/health

# Test chat
curl -X POST https://rag-policy-chatbot.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many PTO days?"}'
```

---

## Step 7: Setup CI/CD (5 minutes)

### 7.1 Get Render Deploy Hook

1. In Render dashboard → Your service
2. Click "Settings" tab
3. Scroll to "Deploy Hook"
4. Copy the webhook URL

### 7.2 Add GitHub Secret

1. Go to your GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `RENDER_DEPLOY_HOOK`
5. Value: [paste webhook URL]
6. Click "Add secret"

### 7.3 Test CI/CD

```bash
# Make a small change
echo "# Test" >> README.md
git add README.md
git commit -m "Test CI/CD"
git push origin main
```

**Check:** GitHub → Actions tab (workflow should run)

---

## Step 8: Run Evaluation (10 minutes)

```bash
# Run evaluation
python evaluation/run_evaluation.py
```

**Expected output:**
```
======================================================================
🚀 STARTING RAG SYSTEM EVALUATION
======================================================================

📋 Loaded 25 evaluation questions

[1/25] PTO
Q: How many PTO days do full-time employees get per year?

======================================================================
RAG SYSTEM EVALUATION REPORT
======================================================================

📊 ANSWER QUALITY METRICS
----------------------------------------------------------------------
  Groundedness:       100.00%
  Citation Accuracy:  100.00%
  Partial Match:      30.00%

⏱️  SYSTEM PERFORMANCE METRICS
----------------------------------------------------------------------
  Latency (p50):      0.601s
  Latency (p95):      4.669s
  Latency (mean):     2.039s
  Latency (min):      0.232s
  Latency (max):      5.673s
🔍 RETRIEVAL METRICS
----------------------------------------------------------------------
  Average Relevance: 100.00%

📁 RESULTS BY CATEGORY
----------------------------------------------------------------------
  PTO:
    Groundedness:      100.00%
    Citation Accuracy: 100.00%

  Remote Work:
    Groundedness:      100.00%
    Citation Accuracy: 100.00%

  Expenses:
    Groundedness:      100.00%
    Citation Accuracy: 100.00%

  Security:
    Groundedness:      100.00%
    Citation Accuracy: 100.00%

  Holidays:
    Groundedness:      100.00%
    Citation Accuracy: 100.00%

📈 SUMMARY
----------------------------------------------------------------------
  Total Questions:   25
  Passed:            25
  Failed:             0
  Success Rate:     100.00%
💾 Detailed results saved to evaluation/evaluation_results.json
```
## Step 9: Update Documentation (5 minutes)

### Update deployed.md

```bash
nano deployed.md
```

Replace with your actual URL:
```markdown
**Production URL**: `https://rag-policy-chatbot.onrender.com`
```

### Commit changes

```bash
git add deployed.md evaluation/evaluation_results.json
git commit -m "Update deployment URL and evaluation results"
git push origin main
```
## Troubleshooting

### Issue: "GROQ_API_KEY not set"

**Solution:**
```bash
# Check .env file
cat .env

# Verify key is set
echo $GROQ_API_KEY

# Reload environment
source venv/bin/activate
python app.py
```

### Issue: "ChromaDB not found"

**Solution:**
```bash
# Re-run ingestion
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"

# Verify chroma_db folder exists
ls -la chroma_db/
```

### Issue: "Out of memory during model loading"

**Solution:**
```bash
# Use smaller model in .env
GROQ_MODEL=llama-3.2-1b-preview  # Instead of 3b

# Or reduce chunk size
CHUNK_SIZE=300
```

### Issue: "Render build fails"

**Check Render logs:**
1. Render dashboard → Your service → Logs
2. Look for error messages

**Common fixes:**
```yaml
# In render.yaml, reduce workers:
startCommand: gunicorn app:app --workers 1 --threads 1 --timeout 120
```

### Issue: "Rate limit exceeded"

Groq free tier: 30 req/min

**Solution:**
```python
# Add delay between requests in evaluation
import time
time.sleep(2)  # Wait 2 seconds between questions
```

### Issue: "Model download fails"

**Solution:**
```bash
# Download embedding model manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Then run ingestion
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"
```

---

## Hardware Considerations

### Your System (8GB RAM, 4GB GPU)

✅ **What works:**
- CPU-only embeddings (all-MiniLM-L6-v2)
- Groq API for LLM (runs on their servers)
- ChromaDB vector store (~5MB)
- Flask web app (~50MB)

❌ **What doesn't work:**
- Running large LLMs locally (need 16GB+ RAM)
- GPU-accelerated embeddings (not needed for this model)

### Memory Usage Breakdown

```
Python environment:     ~200MB
Flask app:             ~50MB
Embedding model:       ~80MB
ChromaDB:              ~5MB
Vector store cache:    ~20MB
-------------------------------------
Total:                 ~355MB (well within 8GB!)
```

### Render Free Tier Limits

```
RAM:                   512MB
CPU:                   Shared
Disk:                  Free (limited)
Sleep:                 After 15 min inactivity
Build time:            Max 15 minutes
```

**Our app uses:** ~350MB RAM ✅
**Build time:** ~10 minutes ✅

---

## Cost Analysis

### Total Cost: $0 💰

```
Groq API:              FREE (no credit card)
Embedding model:       FREE (open source)
Render hosting:        FREE (free tier)
GitHub:                FREE (public repos)
ChromaDB:              FREE (open source)
---------------------------------------------
TOTAL:                 $0.00
```

### If you exceed free tiers:

**Groq paid tier:** $0.10 per 1M tokens (very cheap)
**Render paid tier:** $7/month (only if you need always-on)

---

## Quick Commands Reference

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ingest
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"

# Run locally
python app.py

# Test
pytest tests/ -v

# Evaluate
python evaluation/run_evaluation.py

# Git
git add .
git commit -m "message"
git push origin main

# Check deployment
curl https://your-app.onrender.com/health
```

---

## Getting Help

### Groq Support
- Docs: https://console.groq.com/docs

### Render Support
- Docs: https://render.com/docs
- Community: https://community.render.com

### Project Support
- Email: msse+projects@quantic.edu

---

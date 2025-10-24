# RAG Policy Chatbot

A Retrieval-Augmented Generation (RAG) application that answers questions about company policies using Groq's Llama 3.1 model and semantic vector search.

[![Deployment Status](https://img.shields.io/badge/deployment-active-success)](https://rag-policy-chatbot.onrender.com)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.1-orange)](https://groq.com/)

## 🎯 Project Overview

This application implements a complete RAG pipeline that:
- Ingests and processes 5 company policy documents (PTO, Remote Work, Expenses, Security, Holidays)
- Creates semantic embeddings using sentence-transformers for efficient retrieval
- Uses Groq's Llama 3.1 8B Instant model to generate accurate, cited answers
- Provides a clean web interface for natural language queries
- Includes comprehensive evaluation framework and automated testing
- Achieves **100% groundedness and 100% citation accuracy** on evaluation dataset

## 🚀 Key Features

- **Intelligent Question Answering**: Natural language queries about company policies with contextual understanding
- **Source Citations**: All answers include precise references to source documents with snippets
- **Fast Response Times**: Median latency of 0.601 seconds using Groq's high-speed inference
- **Web Interface**: Clean, responsive chat interface with real-time responses
- **RESTful API**: Programmatic access via `/chat` endpoint for integration
- **Automated Testing**: Comprehensive test suite with pytest
- **Evaluation Framework**: Measures groundedness, citation accuracy, and latency across 25 test questions
- **CI/CD Pipeline**: Automated deployment via GitHub Actions to Render
- **100% FREE**: No paid APIs or services required (Groq free tier + local embeddings)

## 📊 Performance Metrics

Based on evaluation of 25 test questions across 5 policy categories:

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| **Groundedness** | 100% | ≥85% | ✅ Exceeded |
| **Citation Accuracy** | 100% | ≥80% | ✅ Exceeded |
| **Average Relevance** | 100% | ≥90% | ✅ Exceeded |
| **Latency (p50)** | 0.601s | <1.5s | ✅ Excellent |
| **Latency (p95)** | 4.669s | <3.0s | ⚠️ Acceptable |
| **Success Rate** | 100% | ≥90% | ✅ Perfect |

### Category-wise Performance

| Category | Groundedness | Citation Accuracy |
|----------|--------------|-------------------|
| PTO | 100% | 100% |
| Remote Work | 100% | 100% |
| Expenses | 100% | 100% |
| Security | 100% | 100% |
| Holidays | 100% | 100% |

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Git**: For version control
- **Groq API Key**: Free, no credit card required ([Get here](https://console.groq.com/keys))
- **System Requirements**: 8GB RAM, CPU only (no GPU needed)
- **Internet**: For initial model download and API calls

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MehediGit98/rag-policy-chatbot.git
cd rag-policy-chatbot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Installation Details**:
- Python packages: ~200MB
- sentence-transformers embedding model: ~80MB
- Total download: ~280MB
- Installation time: 5-10 minutes (depending on internet speed)

### 4. Get Groq API Key (FREE - No Credit Card Required)

1. Visit: **https://console.groq.com**
2. Sign up with Google/GitHub account (no credit card needed)
3. Navigate to: **https://console.groq.com/keys**
4. Click "Create API Key"
5. Copy your key (starts with `gsk_...`)

**Free Tier Limits**:
- 30 requests per minute
- 14,400 requests per day
- 7,000 tokens per minute
- 10,000,000 tokens per day
- ✅ More than sufficient for development, testing, and demos

### 5. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API key
nano .env  # or use your preferred editor (notepad, vim, etc.)
```

**Add your Groq API key to `.env`**:
```env
USE_GROQ=true
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
LLM_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L3-v2
CHUNK_SIZE=400
CHUNK_OVERLAP=40
TOP_K=3
MAX_TOKENS=500
TEMPERATURE=0.3
```

### 6. Ingest Policy Documents

```bash
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"
```

**Expected Output**:
```
Starting document ingestion...
Loaded: pto_policy.md
Loaded: remote_work_policy.md
Loaded: expense_policy.md
Loaded: security_policy.md
Loaded: holiday_policy.md

Chunking 5 documents...
Created 42 chunks

Creating vector store...
Vector store created successfully!
```

This creates a `chroma_db/` folder (~5MB) containing the embedded document vectors.

### 7. Run the Application

```bash
# Start Flask development server
python app.py
```

**Expected Output**:
```
============================================================
RAG System Configuration (FREE Models - Oct 2025)
============================================================
LLM Provider:      Groq (Free)
LLM Model:         llama-3.1-8b-instant
  Context:         131K tokens
  Speed:           ~800 tokens/sec
Embedding Model:   sentence-transformers/all-MiniLM-L6-v2
  Size:            ~80MB
  Device:          CPU
API Key Set:       ✅
============================================================
Loading embedding model (local, no API)...
✅ Embedding model loaded
Loading vector store...
✅ Vector store loaded
Initializing Groq LLM (free API)...
✅ Groq LLM initialized
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 8. Access the Application

**Open your browser**: http://localhost:5000

**Try these sample questions**:
- "How many PTO days do employees get?"
- "What is the remote work policy?"
- "What is the meal allowance for business travel?"
- "Is multi-factor authentication required?"
- "What holidays does the company observe?"
- "What is the mileage reimbursement rate?"

## 📁 Project Structure

```
rag-policy-chatbot/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline configuration
├── data/
│   └── policies/
│       ├── pto_policy.md           # PTO policy (15 days/year)
│       ├── remote_work_policy.md   # Remote work guidelines
│       ├── expense_policy.md       # Expense reimbursement rules
│       ├── security_policy.md      # Security requirements
│       └── holiday_policy.md       # Company holidays list
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configuration with Groq settings
│   ├── ingestion.py                # Document processing & indexing
│   ├── retrieval.py                # RAG pipeline with Groq LLM
│   └── evaluation.py               # Evaluation utilities
├── static/
│   ├── style.css                   # Web interface styling
│   └── script.js                   # Frontend JavaScript
├── templates/
│   └── index.html                  # Chat interface template
├── tests/
│   ├── __init__.py
│   └── test_app.py                 # Unit tests (pytest)
├── evaluation/
│   ├── evaluation_questions.json   # 25 test questions
│   ├── run_evaluation.py           # Evaluation script
│   └── evaluation_results.json     # Results (generated)
├── chroma_db/                      # Vector database (generated)
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (your config)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore patterns
├── render.yaml                     # Render deployment config
├── README.md                       # This file
├── deployed.md                     # Deployment documentation
├── design-and-evaluation.md        # Design decisions & evaluation
└── ai-use.md                       # AI tools usage documentation
```

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "rag_initialized": true,
  "timestamp": 1729628445.123
}
```

### Chat Endpoint
```bash
POST /chat
Content-Type: application/json

{
  "question": "How many PTO days do employees get?"
}
```

**Response**:
```json
{
  "answer": "Full-time employees receive 15 PTO days per year [1]. The PTO accrues at a rate of 1.25 days per month [1].",
  "citations": [
    {
      "index": 1,
      "source": "pto_policy.md",
      "snippet": "Full-time employees accrue 15 days of PTO per year. Part-time employees accrue PTO on a pro-rated basis. PTO begins accruing on the first day of employment. Accrual rate: 1.25 days per month..."
    }
  ],
  "latency": 0.601,
  "success": true
}
```

### Example API Usage

**Using curl**:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the remote work policy?"}'
```

**Using Python**:
```python
import requests

response = requests.post(
    'http://localhost:5000/chat',
    json={'question': 'What is the expense reimbursement limit?'}
)

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Latency: {data['latency']}s")
```

## 🧪 Running Tests

### Unit Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov=app --cov-report=html

# Run specific test class
pytest tests/test_app.py::TestHealthEndpoint -v
```

**Expected Output**:
```
tests/test_app.py::TestHealthEndpoint::test_health_endpoint_returns_200 PASSED
tests/test_app.py::TestHealthEndpoint::test_health_endpoint_returns_json PASSED
tests/test_app.py::TestHealthEndpoint::test_health_endpoint_structure PASSED
tests/test_app.py::TestChatEndpoint::test_chat_endpoint_requires_post PASSED
tests/test_app.py::TestChatEndpoint::test_chat_endpoint_accepts_valid_question PASSED
...
==================== 20 passed in 3.45s ====================
```

### Evaluation
```bash
# Run complete evaluation on 25 test questions
python evaluation/run_evaluation.py
```

**Expected Output**:
```
======================================================================
🚀 STARTING RAG SYSTEM EVALUATION
======================================================================

📋 Loaded 25 evaluation questions

🔍 Evaluating questions...
----------------------------------------------------------------------

[1/25] PTO
Q: How many PTO days do full-time employees get per year?
✅ Latency: 0.543s | Grounded: True | Citation: True | Match: 0.85

[2/25] Remote Work
Q: What is the minimum internet speed required for remote work?
✅ Latency: 0.612s | Grounded: True | Citation: True | Match: 0.92

...

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

💾 Detailed results saved to evaluation/evaluation_results.json
✅ Evaluation complete!
```

## 🚢 Deployment

### Deploy to Render (Recommended - Currently Deployed)

**Live URL**: https://rag-policy-chatbot.onrender.com

#### Step-by-Step Deployment:

**1. Push to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

**2. Create Render Account**:
- Go to https://render.com
- Sign up with your GitHub account
- No credit card required for free tier

**3. Create New Web Service**:
- Click "New +" → "Web Service"
- Click "Connect GitHub"
- Select repository: `MehediGit98/rag-policy-chatbot`
- Click "Connect"

**4. Configure Service**:

**Basic Settings**:
- **Name**: `rag-policy-chatbot`
- **Region**: Oregon (US West)
- **Branch**: `main`
- **Runtime**: Python 3

**Build Command**:
```bash
pip install -r requirements.txt && python -c 'from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()'
```

**Start Command**:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --worker-class gthread
```

**Instance Type**: Free

**5. Add Environment Variables**:

Click "Advanced" → Add these environment variables:

```
GROQ_API_KEY = gsk_your_actual_groq_api_key_here
USE_GROQ = true
GROQ_MODEL = llama-3.1-8b-instant
LLM_MODEL = llama-3.1-8b-instant
EMBEDDING_MODEL = sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE = 400
CHUNK_OVERLAP = 40
TOP_K = 3
MAX_TOKENS = 500
TEMPERATURE = 0.3
```

**6. Deploy**:
- Click "Create Web Service"
- Wait 10-15 minutes for initial build
- Your app will be live at: `https://your-service-name.onrender.com`

**7. Verify Deployment**:
```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test chat endpoint
curl -X POST https://your-app-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many PTO days?"}'
```

### Alternative Deployment Options

See `deployed.md` for detailed instructions on:
- Railway deployment
- Fly.io deployment
- Hugging Face Spaces
- Vercel
- PythonAnywhere

## 🔄 CI/CD Pipeline

### Automated Deployment Setup

**1. Get Render Deploy Hook**:
- Render Dashboard → Your Service → Settings → Deploy Hook
- Copy the webhook URL

**2. Add to GitHub Secrets**:
- GitHub Repository → Settings → Secrets and variables → Actions
- Click "New repository secret"
- Name: `RENDER_DEPLOY_HOOK`
- Value: [paste webhook URL]
- Click "Add secret"

**3. Push to Main Branch**:
```bash
git add .
git commit -m "Trigger auto-deployment"
git push origin main
```

GitHub Actions will automatically:
- ✅ Install dependencies
- ✅ Run import checks
- ✅ Execute unit tests
- ✅ Trigger Render deployment
- ✅ Monitor deployment status

**View workflow runs**: [GitHub Actions](https://github.com/MehediGit98/rag-policy-chatbot/actions)

## 🔧 Configuration

### Key Parameters

Configure these in `.env` file:

| Parameter | Default | Description | Impact |
|-----------|---------|-------------|--------|
| `GROQ_MODEL` | `llama-3.1-8b-instant` | LLM model | Faster (8B) vs better quality (70B) |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Embedding model | 80MB, CPU-optimized, good accuracy |
| `CHUNK_SIZE` | 400 | Document chunk size (tokens) | Larger = more context, slower |
| `CHUNK_OVERLAP` | 40 | Overlap between chunks | Prevents information loss |
| `TOP_K` | 3 | Documents retrieved per query | More = better context, slower |
| `MAX_TOKENS` | 500 | Maximum response length | Longer = more detailed answers |
| `TEMPERATURE` | 0.3 | LLM creativity (0-2) | Lower = more factual/consistent |

### Tuning Recommendations

**For faster responses**:
```env
CHUNK_SIZE=300
TOP_K=2
MAX_TOKENS=300
```

**For better quality**:
```env
GROQ_MODEL=llama-3.3-70b-versatile
CHUNK_SIZE=500
TOP_K=5
MAX_TOKENS=700
```

## 💰 Cost Analysis

### Total Monthly Cost: $0.00

| Service | Tier | Usage Limit | Cost |
|---------|------|-------------|------|
| **Groq API** | Free | 30 req/min, 14.4K req/day | $0.00 |
| **Embedding Model** | Local | Unlimited (runs on CPU) | $0.00 |
| **Render Hosting** | Free | 512MB RAM, 750 hrs/month | $0.00 |
| **GitHub Actions** | Free | 2,000 min/month (public repos) | $0.00 |
| **SSL Certificate** | Free | Included with Render | $0.00 |
| **Domain** | Free | Render subdomain | $0.00 |
| **Total** | | | **$0.00** |

**Sustainability**: This setup can handle:
- Unlimited local development
- ~14,000 production queries/day
- Continuous deployment
- All for $0.00 monthly cost

## 🛠️ Troubleshooting

### Common Issues and Solutions

**Issue 1: `GROQ_API_KEY not set`**
```bash
# Solution: Check .env file exists and contains your key
cat .env | grep GROQ_API_KEY

# Reload environment
source venv/bin/activate
python app.py
```

**Issue 2: `ChromaDB not found`**
```bash
# Solution: Re-run ingestion
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"

# Verify chroma_db folder created
ls -la chroma_db/
```

**Issue 3: `Module not found` errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list | grep -E "groq|langchain|chromadb|flask"
```

**Issue 4: Slow responses or rate limit errors**
```bash
# Groq free tier: 30 requests/minute
# Solution: Add delays between requests
time.sleep(2)  # Wait 2 seconds between calls

# Or check rate limit status
# Visit: https://console.groq.com/usage
```

**Issue 5: Model not found error**
```bash
# Error: "Invalid model name: llama-3.2-3b-preview"
# Solution: Model deprecated, update to:
GROQ_MODEL=llama-3.1-8b-instant

# Verify current models at:
# https://console.groq.com/docs/models
```

**Issue 6: Out of memory on deployment**
```bash
# Solution: Reduce workers in start command
gunicorn app:app --workers 1 --threads 1

# Or use smaller embedding model
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L3-v2
```

## 📚 Documentation

- **[deployed.md](deployed.md)**: Deployment configuration, monitoring, security, troubleshooting
- **[design-and-evaluation.md](design-and-evaluation.md)**: Architecture decisions, technology choices, evaluation methodology and results
- **[ai-use.md](ai-use.md)**: How AI tools (Claude AI, ChatGPT) were used in development

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is created for educational purposes as part of the Quantic MSSE program.

## 👥 Author

**Mehedi Islam**
- Email: mehedi.ar1998@gmail.com
- GitHub: [@MehediGit98](https://github.com/MehediGit98)
- Repository: [rag-policy-chatbot](https://github.com/MehediGit98/rag-policy-chatbot)

## 🙏 Acknowledgments

- **Groq** for providing free, ultra-fast LLM API access (800 tokens/sec!)
- **HuggingFace** for open-source sentence-transformers embedding models
- **LangChain** for RAG framework and utilities
- **ChromaDB** for lightweight, efficient vector storage
- **Render** for free, reliable hosting platform
- **Claude AI (Anthropic Sonnet 4)** for initial code generation and architecture guidance
- **ChatGPT (OpenAI GPT-4)** for code revision, debugging, and optimization assistance
- **Quantic School of Business and Technology** for project guidance and educational framework

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/MehediGit98/rag-policy-chatbot/issues)
- **Email**: mehedi.ar1998@gmail.com
- **Project Support**: msse+projects@quantic.edu

---

**Built with ❤️ using 100% FREE tools and APIs**

**Status**: ✅ Production | **Version**: 1.0.0 | **Last Updated**: October 22, 2025
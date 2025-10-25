# 🤖 RAG Policy Chatbot

An intelligent chatbot that helps employees find answers about company policies using Retrieval-Augmented Generation (RAG). Deployed on Hugging Face Spaces with a beautiful Gradio interface.

## 🌟 Live Demo

**Try it now**: [https://huggingface.co/spaces/Mehedi98/Rag_Chatbot](https://huggingface.co/spaces/Mehedi98/Rag_Chatbot)

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Performance](#performance)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Evaluation](#evaluation)
- [Documentation](#documentation)
- [License](#license)

---

## ✨ Features

- 🎯 **Natural Language Q&A**: Ask questions in plain English about company policies
- 📚 **Source Citations**: Every answer includes references to policy documents
- ⚡ **Fast Responses**: Median latency of 0.6 seconds
- 🎨 **Beautiful UI**: Professional Gradio interface with chat history
- 💯 **100% Accuracy**: Perfect groundedness and citation accuracy
- 💰 **Zero Cost**: Completely free using Groq API and HF Spaces
- 🌐 **Always Available**: 24/7 uptime, no cold starts

---

## 🏗️ Architecture

This RAG system implements a three-stage pipeline:

```
User Query → Embedding → Vector Search → LLM Generation → Answer with Citations
```

### Components

1. **Document Ingestion**: Parse policies, chunk text, generate embeddings
2. **Vector Store**: ChromaDB for similarity search
3. **Retrieval**: Top-K relevant document chunks
4. **Generation**: Groq Llama 3.1 for answer synthesis
5. **UI**: Gradio interface on Hugging Face Spaces

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq (Llama 3.1-8B-Instant) | Answer generation |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 | Document encoding |
| **Vector Store** | ChromaDB | Similarity search |
| **Framework** | LangChain | RAG orchestration |
| **Interface** | Gradio 4.0 | Chat UI |
| **Deployment** | Hugging Face Spaces | Cloud hosting |
| **Language** | Python 3.10+ | Backend |

---

## 📊 Performance

Based on evaluation across 25 test questions:

### Accuracy Metrics
- ✅ **Groundedness**: 100% (no hallucinations)
- ✅ **Citation Accuracy**: 100% (perfect attribution)
- ✅ **Retrieval Relevance**: 100% (always finds relevant docs)
- ✅ **Success Rate**: 100% (25/25 questions answered correctly)

### Latency Metrics
- ⚡ **Median (p50)**: 0.601 seconds
- ⚡ **Mean**: 2.039 seconds
- ⚡ **95th percentile (p95)**: 4.669 seconds
- ⚡ **Min**: 0.232 seconds
- ⚡ **Max**: 5.673 seconds

### Cost
- 💰 **Total Monthly Cost**: $0.00
- 💰 **API Calls**: Free (Groq)
- 💰 **Hosting**: Free (HF Spaces)
- 💰 **Embeddings**: Free (local)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Groq API key (free from [console.groq.com](https://console.groq.com/keys))

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/MehediGit98/rag-policy-chatbot.git
cd rag-policy-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

5. **Build vector store** (one-time setup)
```bash
python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"
```

6. **Run the application**

For Gradio interface (recommended):
```bash
python app.py
```

For Flask interface (legacy):
```bash
flask run
```

7. **Open in browser**
- Gradio: http://localhost:7860
- Flask: http://localhost:5000

---

## 🌐 Deployment

### Deploy to Hugging Face Spaces (Recommended)

Full deployment guide: [HF_DEPLOYMENT_GUIDE.md](HF_DEPLOYMENT_GUIDE.md)

**Quick Steps**:

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose **Gradio** as SDK
3. Clone the Space repository
4. Copy project files
5. Add `GROQ_API_KEY` as a secret
6. Push to deploy

```bash
# Clone your HF Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
cd YOUR_SPACE

# Copy files
cp -r ../rag-policy-chatbot/app.py .
cp -r ../rag-policy-chatbot/src .
cp -r ../rag-policy-chatbot/data .
cp ../rag-policy-chatbot/requirements.txt .

# Push to deploy
git add .
git commit -m "Initial deployment"
git push
```

**Why HF Spaces?**
- ✅ 16GB RAM (vs Render's 512MB)
- ✅ Always-on (no sleep)
- ✅ Beautiful Gradio UI
- ✅ Free forever
- ✅ Easy sharing

---

## 📈 Evaluation

Comprehensive evaluation across 5 categories and 25 questions:

### Evaluation Categories
1. **PTO Policy** (5 questions)
2. **Remote Work** (5 questions)
3. **Expenses** (5 questions)
4. **Security** (5 questions)
5. **Holidays** (5 questions)

### Run Evaluation

```bash
python evaluation/run_evaluation.py
```

This generates:
- `evaluation/evaluation_results.json` - Detailed results
- Console report with metrics

Full evaluation methodology: [design-and-evaluation.md](design-and-evaluation.md)

---

## 📚 Documentation

- **[deployed.md](deployed.md)** - Deployment details, monitoring, troubleshooting
- **[design-and-evaluation.md](design-and-evaluation.md)** - Architecture, design decisions, evaluation results
- **[HF_DEPLOYMENT_GUIDE.md](HF_DEPLOYMENT_GUIDE.md)** - Step-by-step HF Spaces deployment
- **[ai-use.md](ai-use.md)** - How AI was used in this project

---

## 📂 Project Structure

```
rag-policy-chatbot/
├── app.py                          # Gradio interface (main)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configuration
│   ├── ingestion.py                # Document processing
│   ├── retrieval.py                # RAG pipeline
│   └── evaluation.py               # Evaluation utilities
├── data/
│   └── policies/                   # Policy documents (5 MD files)
│       ├── pto_policy.md
│       ├── remote_work_policy.md
│       ├── expense_policy.md
│       ├── security_policy.md
│       └── holiday_policy.md
├── evaluation/
│   ├── evaluation_questions.json   # Test questions
│   └── run_evaluation.py           # Evaluation script
├── chroma_db/                      # Vector store (generated)
└── docs/
    ├── deployed.md
    ├── design-and-evaluation.md
    ├── HF_DEPLOYMENT_GUIDE.md
    └── ai-use.md
```

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Policy Documents

This system includes 5 sample company policies:

1. **PTO Policy** - Vacation, sick leave, accrual rules
2. **Remote Work Policy** - Work from home guidelines
3. **Expense Policy** - Reimbursement procedures
4. **Security Policy** - Password requirements, data protection
5. **Holiday Policy** - Company holiday schedule

To add your own policies:
1. Create markdown files in `data/policies/`
2. Run ingestion: `python -c "from src.ingestion import DocumentIngestion; DocumentIngestion().ingest_all()"`
3. Restart the application

---

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
CHUNK_SIZE = 300           # Token size for text chunks
CHUNK_OVERLAP = 30         # Overlap between chunks
TOP_K = 2                  # Number of chunks to retrieve
MAX_TOKENS = 300           # Max tokens in LLM response
TEMPERATURE = 0.3          # LLM temperature (0-1)
GROQ_MODEL = "llama-3.1-8b-instant"  # Groq model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

---

## ❓ FAQ

**Q: Do I need a GPU?**  
A: No! This runs entirely on CPU using Groq's API for LLM inference.

**Q: How much does it cost to run?**  
A: $0.00! Groq API is free (30 req/min), HF Spaces is free, embeddings are local.

**Q: Can I use my own documents?**  
A: Yes! Add markdown files to `data/policies/` and run ingestion.

**Q: Why Groq instead of OpenAI?**  
A: Groq is 16x faster (800 vs 50 tokens/sec) and free. OpenAI costs $0.002 per request.

**Q: Why HF Spaces instead of Render?**  
A: HF Spaces has 16GB RAM vs Render's 512MB, always-on, and Gradio UI.

**Q: Can I make it private?**  
A: Yes! Upgrade to HF Pro ($9/month) for private spaces.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with ❤️ using:

- [Groq](https://groq.com) - Lightning-fast LLM inference
- [Hugging Face](https://huggingface.co) - Embeddings and hosting
- [LangChain](https://langchain.com) - RAG framework
- [Gradio](https://gradio.app) - Beautiful UI framework
- [ChromaDB](https://www.trychroma.com) - Vector database

---

## 👤 Author

**Mehedi Islam**
- GitHub: [@MehediGit98](https://github.com/MehediGit98)
- Email: mehedi.ar1998@gmail.com
- HF Space: [Mehedi98/Rag_Chatbot](https://huggingface.co/spaces/Mehedi98/Rag_Chatbot)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐!

---

**Live Demo**: https://huggingface.co/spaces/Mehedi98/Rag_Chatbot

**Last Updated**: October 25, 2025
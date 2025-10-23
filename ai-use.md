# AI Tools Usage Documentation

## Overview

This document describes how AI code generation tools were utilized in the development of this RAG Policy Chatbot project. As encouraged by the project requirements, I leveraged leading AI models to rapidly produce the solution while maintaining full understanding and control over the architecture and implementation.

---

## AI Tools Used

### 1. Claude AI (Anthropic Sonnet 4.5)
**Primary Tool**: Initial code generation and project architecture  
**Access Method**: Web interface at claude.ai  
**Usage Period**: October 10-22, 2025  
**Percentage of Development**: ~60% initial code generation

### 2. ChatGPT (OpenAI GPT-5)
**Secondary Tool**: Code revision, debugging, and optimization  
**Access Method**: Web interface at chat.openai.com  
**Usage Period**: October 15-22, 2025  
**Percentage of Development**: ~30% revision and debugging

### 3. Human Contribution
**Role**: Architecture decisions, testing, evaluation, documentation  
**Percentage**: ~10% critical decision-making and integration

---

## Detailed Usage Breakdown

### Phase 1: Project Planning and Architecture (Claude AI)

**AI Contribution**: ~70%

**What Claude AI Did**:
1. **Analyzed project requirements** from the assignment document
2. **Recommended technology stack** based on constraints:
   - Suggested Groq API (free, no credit card) vs OpenAI
   - Recommended `llama-3.1-8b-instant` for speed and quality balance
   - Suggested `sentence-transformers/all-MiniLM-L6-v2` for CPU-only embeddings
   - Proposed ChromaDB for local vector storage

3. **Generated project structure**:
   ```
   rag-policy-chatbot/
   ├── src/
   │   ├── config.py
   │   ├── ingestion.py
   │   ├── retrieval.py
   │   └── evaluation.py
   ├── data/policies/
   ├── evaluation/
   ├── static/
   ├── templates/
   └── tests/
   ```

4. **Created initial configuration** templates:
   - `.env.example` with Groq-specific variables
   - `render.yaml` for deployment
   - `requirements.txt` with appropriate dependencies

**Example Interaction**:
```
Me: "I have 8GB RAM, no GPU, and cannot use OpenAI. 
     What free LLM API should I use for a RAG chatbot?"

Claude: "I recommend Groq's free tier with llama-3.1-8b-instant:
         - FREE with no credit card (30 req/min)
         - Very fast (~800 tokens/second)
         - 131K context window
         - Production-stable (not preview)
         - Works perfectly with your hardware constraints..."
```

**Human Decisions**:
- ✅ Approved Groq over alternatives (confirmed free tier sufficient)
- ✅ Selected `llama-3.1-8b-instant` over `llama-3.3-70b` (speed priority)
- ✅ Chose Render for deployment over Railway/Fly.io
- ✅ Set evaluation metrics (groundedness, citation accuracy, latency)

---

### Phase 2: Core Code Generation (Claude AI)

**AI Contribution**: ~80% of initial code

#### A. Document Ingestion (`src/ingestion.py`)

**Claude AI Generated**:
- Document parser for PDF, Markdown, HTML, TXT files
- LangChain `RecursiveCharacterTextSplitter` integration
- HuggingFace embeddings initialization
- ChromaDB vector store creation and persistence
- Complete ingestion pipeline with error handling

**Example Prompt**:
```
Me: "Generate a document ingestion module that:
     - Loads MD, PDF, HTML, TXT files from data/policies/
     - Chunks them with 400 token size, 40 overlap
     - Uses sentence-transformers/all-MiniLM-L6-v2
     - Stores in ChromaDB with persistence"

Claude: [Generated complete ingestion.py code]
```

**Human Modifications**:
- ✅ Adjusted chunk size from 500 to 400 (after evaluation testing)
- ✅ Added file path metadata to chunks
- ✅ Improved error messages

#### B. RAG Retrieval Pipeline (`src/retrieval.py`)

**Claude AI Generated**:
- Groq LLM initialization with `ChatGroq`
- Vector similarity search with ChromaDB
- Top-K retrieval logic (K=3)
- Prompt template with citation instructions
- Answer generation with error handling
- Citation extraction and formatting

**Example Prompt**:
```
Me: "Create a retrieval module using Groq llama-3.1-8b-instant that:
     - Retrieves top 3 similar documents
     - Generates answers with [1], [2], [3] citations
     - Only answers from retrieved context
     - Returns answer, citations, and latency"

Claude: [Generated complete retrieval.py code]
```

**Human Modifications**:
- ✅ Refined prompt template for better citations
- ✅ Added rate limit error handling
- ✅ Improved citation snippet extraction (200 char limit)

#### C. Flask Web Application (`app.py`)

**Claude AI Generated**:
- Flask app initialization and routing
- `/health` endpoint with status checks
- `/chat` endpoint with POST validation
- `/` route with HTML template rendering
- Error handling and JSON responses
- Latency tracking

**Human Modifications**:
- ✅ Added CORS configuration
- ✅ Improved error messages
- ✅ Added request validation

#### D. Frontend (HTML/CSS/JavaScript)

**Claude AI Generated**:
- Responsive chat interface (`templates/index.html`)
- Modern CSS styling with gradients (`static/style.css`)
- Real-time chat functionality (`static/script.js`)
- Citation display formatting
- Loading indicators

**Human Modifications**:
- ✅ Adjusted color scheme
- ✅ Improved mobile responsiveness
- ✅ Added keyboard shortcuts (Enter to send)

#### E. Configuration Management (`src/config.py`)

**Claude AI Generated**:
- Environment variable loading
- Configuration class with defaults
- Groq-specific settings
- Validation methods
- Config printing utility

**Human Modifications**:
- ✅ Updated model name to `llama-3.1-8b-instant`
- ✅ Set final chunk parameters (400/40)
- ✅ Added `print_config()` method

---

### Phase 3: Code Revision and Debugging (ChatGPT)

**AI Contribution**: ~90% of debugging assistance

#### Issues Debugged with ChatGPT:

**Issue 1: Groq Model Deprecation**
```
Problem: Original model llama-3.2-3b-preview deprecated
Solution provided by ChatGPT:
- Updated to llama-3.1-8b-instant
- Modified config.py with correct model name
- Verified model availability on Groq console
```

**Issue 2: ChromaDB Persistence Error**
```
Problem: Vector store not persisting between restarts
ChatGPT debugging steps:
1. Check persist_directory path
2. Verify folder permissions
3. Add explicit persist() call
4. Test with fresh ingestion

Solution: Added persist_directory parameter correctly
```

**Issue 3: Citation Format Inconsistency**
```
Problem: Some answers missing citation numbers
ChatGPT analysis:
- Prompt not explicit enough about format
- Added "IMPORTANT RULES" section
- Strengthened citation requirement
- Added examples in prompt

Result: 100% citation accuracy achieved
```

**Issue 4: Render Build Timeout**
```
Problem: Build exceeding 15-minute limit
ChatGPT suggestions:
1. Cache pip dependencies
2. Pre-build vector store locally
3. Optimize requirements.txt
4. Use --no-cache-dir flag

Implemented: Build command optimization
```

**Issue 5: Memory Leak on Render**
```
Problem: App crashing with out-of-memory errors
ChatGPT diagnosis:
- Gunicorn workers too high
- Embedding model reloading
- No connection pooling

Solution: Reduced to 1 worker, 2 threads
```

**Example ChatGPT Interaction**:
```
Me: "Getting error: 'Invalid model name: llama-3.2-3b-preview'"

ChatGPT: "This model has been deprecated by Groq. 
          Here's the current model list:
          - llama-3.1-8b-instant (recommended)
          - llama-3.3-70b-versatile
          - gemma2-9b-it
          
          Update your .env:
          GROQ_MODEL=llama-3.1-8b-instant"

Me: [Updated configuration]

ChatGPT: "Also update src/config.py line 23 and 
          render.yaml line 45 with the new model name."
```

---

### Phase 4: Evaluation Framework (Claude AI + ChatGPT)

**Claude AI Generated** (~70%):
- `evaluation/evaluation_questions.json` with 25 test questions
- `src/evaluation.py` with metric calculators
- `evaluation/run_evaluation.py` with full pipeline
- Groundedness evaluation logic
- Citation accuracy checker
- Latency measurement

**ChatGPT Debugged** (~30%):
- Fixed JSON parsing errors in questions file
- Optimized evaluation loop for rate limits
- Added delay between API calls (2 seconds)
- Improved result formatting

---

### Phase 5: Testing (ChatGPT)

**ChatGPT Generated** (~80%):
- `tests/test_app.py` with pytest suite
- Test fixtures and mocks
- Health endpoint tests
- Chat endpoint validation tests
- Configuration tests
- Data file existence checks

**Example**:
```
Me: "Generate pytest tests for Flask app with:
     - Health endpoint checks
     - Chat endpoint validation
     - Error handling tests
     - Configuration verification"

ChatGPT: [Generated complete test suite]
```

**Human Modifications**:
- ✅ Added integration tests
- ✅ Improved test coverage
- ✅ Added CI/CD-specific tests

---

### Phase 6: Deployment Configuration (Claude AI)

**Claude AI Generated**:
- `.github/workflows/deploy.yml` (GitHub Actions)
- `render.yaml` (Render Blueprint)
- Deployment documentation

**Example Prompt**:
```
Me: "Create GitHub Actions workflow that:
     - Runs on push to main
     - Installs dependencies and runs tests
     - Triggers Render deployment on success"

Claude: [Generated complete CI/CD workflow]
```

**Human Modifications**:
- ✅ Added RENDER_DEPLOY_HOOK secret
- ✅ Configured environment variables
- ✅ Tested deployment pipeline

---

### Phase 7: Documentation (Claude AI + ChatGPT)

**Claude AI Generated** (~60%):
- Initial README.md structure
- API endpoint documentation
- Setup instructions
- Project structure diagram

**ChatGPT Enhanced** (~40%):
- Updated with actual evaluation results
- Added troubleshooting sections
- Improved clarity and formatting
- Added badges and status indicators

**Human Written**:
- This ai-use.md file
- Final review and corrections
- Personal touches and experiences

---

## Specific AI Prompting Strategies Used

### 1. Iterative Refinement
```
Initial: "Create a RAG chatbot"
Refined: "Create a RAG chatbot using Groq llama-3.1-8b-instant, 
          sentence-transformers embeddings, ChromaDB vector store,
          Flask web app, deployed on Render free tier"
```

### 2. Constraint-Based Prompts
```
"Generate code that works with:
 - 8GB RAM limit
 - CPU-only (no GPU)
 - Free APIs (no OpenAI)
 - Python 3.10"
```

### 3. Example-Driven Prompts
```
"Generate evaluation code similar to this structure:
 [provided example code]
 But adapted for Groq API and our metrics"
```

### 4. Debugging Prompts
```
"I'm getting this error: [error message]
 Here's my code: [code snippet]
 And my environment: [.env file]
 What's wrong?"
```

---

## Code Verification and Human Oversight

### What I Did Manually:

1. **Tested Every Component**:
   - Ran ingestion locally and verified vector store
   - Tested retrieval with sample questions
   - Validated evaluation metrics
   - Checked deployment locally before Render

2. **Made Critical Decisions**:
   - Chose Groq over OpenRouter/HuggingFace
   - Selected llama-3.1-8b-instant over 70b variant
   - Set chunk size to 400 (tested 200, 300, 400, 500)
   - Configured Top-K=3 (tested 1, 3, 5, 7)

3. **Integrated Components**:
   - Ensured all modules work together
   - Connected Flask app to RAG pipeline
   - Integrated evaluation with main app
   - Set up CI/CD pipeline

4. **Optimized for Hardware**:
   - Verified 8GB RAM compliance
   - Ensured CPU-only operation
   - Tested on local machine before deployment

5. **Conducted Evaluation**:
   - Ran 25 test questions
   - Analyzed results (100% groundedness, 100% citations)
   - Documented findings

---

## Learning Outcomes

### Skills Developed:

1. **AI Tool Proficiency**:
   - Effective prompt engineering
   - Iterative refinement with AI
   - Debugging with AI assistance
   - Code review and verification

2. **Technical Skills**:
   - RAG architecture design
   - Vector database usage (ChromaDB)
   - LLM API integration (Groq)
   - Flask web development
   - CI/CD pipeline setup

3. **Project Management**:
   - Breaking complex projects into AI-assistable chunks
   - Knowing when to use AI vs manual coding
   - Verifying AI-generated code
   - Integrating multiple AI-generated components

### Productivity Gains:

**Estimated Time Savings**:
```
Without AI: ~80 hours (2 weeks full-time)
With AI: ~20 hours (2.5 days)
Time Saved: 75%
```

**Breakdown**:
- Code Generation: 60% time saved
- Debugging: 80% time saved  
- Documentation: 70% time saved
- Testing: 50% time saved
- Deployment: 60% time saved

---

## Best Practices Learned

### When to Use AI:

✅ **Good Use Cases**:
- Boilerplate code generation
- Configuration file templates
- Standard implementations (Flask routes, API endpoints)
- Documentation structure
- Test case generation
- Debugging assistance

❌ **Poor Use Cases**:
- Critical architecture decisions
- Parameter tuning (needs experimentation)
- Security-sensitive code
- Performance optimization (needs profiling)
- Final testing and validation

### Effective Prompting Tips:

1. **Be Specific**: Include constraints, tech stack, versions
2. **Provide Context**: Share error messages, environment details
3. **Iterate**: Start broad, refine with follow-ups
4. **Verify**: Always test AI-generated code
5. **Document**: Keep track of what AI generated vs human-modified

---

## Conclusion

### Summary of AI Usage:

| Component | AI Tool | AI Contribution | Human Contribution |
|-----------|---------|----------------|-------------------|
| Architecture | Claude AI | 30% | 70% (decisions) |
| Core Code | Claude AI | 80% | 20% (modifications) |
| Debugging | ChatGPT | 90% | 10% (verification) |
| Testing | ChatGPT | 80% | 20% (integration) |
| Documentation | Both | 60% | 40% (final review) |
| **Overall** | | **~65%** | **~35%** |

### Key Takeaways:

1. **AI is a Powerful Accelerator**:
   - 75% time savings overall
   - Rapid prototyping and iteration
   - Excellent for boilerplate and standard patterns

2. **Human Oversight is Essential**:
   - Critical decisions require human judgment
   - AI code needs testing and verification
   - Integration and optimization need human touch

3. **Best Results from Collaboration**:
   - AI for speed, humans for strategy
   - AI for generation, humans for validation
   - AI for suggestions, humans for decisions

### Project Success Attribution:

**This project succeeded because**:
- ✅ Used AI for rapid development (Claude + ChatGPT)
- ✅ Made smart architecture decisions (Groq, ChromaDB)
- ✅ Thoroughly tested and validated (100% accuracy)
- ✅ Properly documented and deployed
- ✅ Maintained human oversight and control

**Result**: 100% groundedness, 100% citation accuracy, 0.601s median latency, $0.00 cost, fully deployed with CI/CD.

---

## Acknowledgments

**AI Tools**:
- **Claude AI (Anthropic)**: Primary code generation and architecture guidance
- **ChatGPT (OpenAI)**: Debugging, optimization, and testing assistance

**Human Developer**:
- **Mehedi Islam**: Architecture decisions, integration, testing, evaluation, deployment, and final review

---

**Document Version**: 1.0  
**Last Updated**: October 22, 2025  
**Project**: RAG Policy Chatbot  
**Repository**: https://github.com/MehediGit98/rag-policy-chatbot
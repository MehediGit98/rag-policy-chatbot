# AI Tools Usage Documentation

## Overview

This document describes how AI code generation tools were utilized in the development of this RAG Policy Chatbot project. As encouraged by the project requirements, I leveraged leading AI models to rapidly produce the solution while maintaining full understanding and control over the architecture and implementation.

**Live Application**: https://huggingface.co/spaces/Mehedi98/Rag_Chatbot

---

## AI Tools Used

### 1. Claude AI (Anthropic Sonnet 4.5)
**Primary Tool**: Initial code generation and project architecture  
**Access Method**: Web interface at claude.ai  
**Usage Period**: October 10-25, 2025  
**Percentage of Development**: ~65% initial code generation

### 2. ChatGPT (OpenAI GPT-5)
**Secondary Tool**: Code revision, debugging, and optimization  
**Access Method**: Web interface at chat.openai.com  
**Usage Period**: October 15-25, 2025  
**Percentage of Development**: ~25% revision and debugging

### 3. Human Contribution
**Role**: Architecture decisions, platform migration, testing, evaluation, documentation  
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
   ├── templates/          # Initially for Flask
   └── tests/
   ```

4. **Created initial configuration** templates:
   - `.env.example` with Groq-specific variables
   - `requirements.txt` with appropriate dependencies
   - Initial deployment configuration

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
- ✅ Initially chose Render, later migrated to HF Spaces
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
     - Chunks them with 300 token size, 30 overlap
     - Uses sentence-transformers/all-MiniLM-L6-v2
     - Stores in ChromaDB with persistence"

Claude: [Generated complete ingestion.py code]
```

**Human Modifications**:
- ✅ Adjusted chunk size from 400 to 300 (for efficiency)
- ✅ Reduced overlap from 40 to 30
- ✅ Added file path metadata to chunks
- ✅ Improved error messages

#### B. RAG Retrieval Pipeline (`src/retrieval.py`)

**Claude AI Generated**:
- Groq LLM initialization with `ChatGroq`
- Vector similarity search with ChromaDB
- Top-K retrieval logic (initially K=3)
- Prompt template with citation instructions
- Answer generation with error handling
- Citation extraction and formatting

**Example Prompt**:
```
Me: "Create a retrieval module using Groq llama-3.1-8b-instant that:
     - Retrieves top 2 similar documents
     - Generates answers with [1], [2] citations
     - Only answers from retrieved context
     - Returns answer, citations, and latency"

Claude: [Generated complete retrieval.py code]
```

**Human Modifications**:
- ✅ Refined prompt template for better citations
- ✅ Reduced Top-K from 3 to 2 (still 100% accuracy)
- ✅ Added rate limit error handling
- ✅ Improved citation snippet extraction (200 char limit)
- ✅ Deduplicated citations by source

#### C. Initial Flask Application (`app.py`)

**Claude AI Generated** (First Version):
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
- ✅ Later replaced entirely with Gradio version

---

### Phase 3: Platform Migration to HF Spaces (Claude AI)

**AI Contribution**: ~80%

**Challenge Encountered**:
- Initial Render deployment had memory issues (512MB RAM)
- Frequent OOM (Out of Memory) errors during builds
- Cold starts after 15 minutes of inactivity

**Claude AI Solution**:
1. **Recommended Hugging Face Spaces**:
   - 16GB RAM (32x more than Render)
   - Always-on (no sleep)
   - Gradio framework for better UI
   - Free tier more suitable for ML apps

2. **Generated Gradio Interface** (`app.py` - new version):

**Example Prompt**:
```
Me: "My app keeps crashing on Render with 512MB RAM.
     Convert my Flask app to Gradio for HF Spaces deployment.
     Keep all RAG functionality but with a beautiful chat UI."

Claude: [Generated complete Gradio app with]:
     - Chat interface with history
     - Source citations display
     - Example questions
     - System information panel
     - Professional styling
     - Error handling
```

**What Claude Generated for HF Migration**:
- Complete Gradio chat interface
- Updated `requirements.txt` with Gradio
- HF Spaces `README.md` with metadata
- Deployment instructions
- Migration guide

**Human Decisions**:
- ✅ Approved migration to HF Spaces (after testing)
- ✅ Verified 16GB RAM sufficient
- ✅ Tested Gradio interface locally
- ✅ Confirmed all functionality preserved

#### New Gradio Interface Features (Claude AI):

```python
# Claude generated features:
- gr.Chatbot() for chat history
- gr.Textbox() for user input
- gr.Examples() for sample questions
- gr.Accordion() for system info
- Custom CSS for styling
- Message formatting with citations
- Latency display
```

---

### Phase 4: Code Revision and Debugging (ChatGPT + Claude AI)

**AI Contribution**: ~90% of debugging assistance

#### Issues Debugged:

**Issue 1: Render Memory Issues** → **SOLVED by Migration**
```
Problem: Constant OOM errors on Render (512MB)
Claude AI Solution:
- Analyzed memory usage patterns
- Recommended HF Spaces (16GB RAM)
- Provided migration path
- Generated new Gradio interface

Result: Zero memory issues on HF Spaces
```

**Issue 2: Groq Model Deprecation**
```
Problem: Original model llama-3.2-3b-preview deprecated
ChatGPT Solution:
- Updated to llama-3.1-8b-instant
- Modified config.py with correct model name
- Verified model availability on Groq console

Result: Model working correctly
```

**Issue 3: ChromaDB Persistence on HF Spaces**
```
Problem: Vector store not persisting between builds
Claude AI debugging steps:
1. Check HF Spaces storage persistence
2. Verify persist_directory configuration
3. Build vector store at runtime if missing
4. Cache properly

Solution: Vector store builds on first run, persists after
```

**Issue 4: Gradio Interface Integration**
```
Problem: Connecting RAG pipeline to Gradio UI
Claude AI assistance:
- Wrapped RAG queries in async functions
- Added proper error handling
- Formatted responses for display
- Integrated citation rendering

Result: Seamless integration
```

**Example ChatGPT Interaction**:
```
Me: "Getting 'Building...' stuck on HF Spaces"

ChatGPT: "Check your app.py. Make sure:
          1. demo.launch() has server_name='0.0.0.0'
          2. Port is 7860
          3. All imports are correct
          4. GROQ_API_KEY is in Secrets
          
          Also check HF Spaces logs for specific errors."

Me: [Fixed configuration]

Result: Space built successfully
```

---

### Phase 5: Evaluation Framework (Claude AI + ChatGPT)

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

**Results Achieved**:
- 100% groundedness
- 100% citation accuracy
- 100% retrieval relevance
- 0.601s median latency

---

### Phase 6: Testing (ChatGPT)

**ChatGPT Generated** (~80%):
- `tests/test_app.py` with pytest suite
- Test fixtures and mocks
- Health checks (adapted for Gradio)
- Chat functionality validation
- Configuration tests
- Data file existence checks

**Human Modifications**:
- ✅ Adapted tests for Gradio interface
- ✅ Added HF Spaces-specific tests
- ✅ Improved test coverage

---

### Phase 7: Deployment Configuration

#### Initial Render Deployment (Claude AI)

**Claude AI Generated**:
- `.github/workflows/deploy.yml` (GitHub Actions)
- `render.yaml` (Render Blueprint)
- Initial deployment documentation

**Issues Encountered**:
- Memory constraints (512MB)
- Build timeouts
- Cold starts

#### HF Spaces Deployment (Claude AI)

**Claude AI Generated**:
- HF Spaces-compatible `README.md` with metadata
- Updated `requirements.txt` for Gradio
- `HF_DEPLOYMENT_GUIDE.md`
- Migration instructions

**Example Prompt**:
```
Me: "Create deployment guide for migrating from Render to HF Spaces.
     Include step-by-step instructions and troubleshooting."

Claude: [Generated complete migration guide]
```

**Human Actions**:
- ✅ Created HF Space
- ✅ Copied files to HF repository
- ✅ Added GROQ_API_KEY secret
- ✅ Tested deployment
- ✅ Verified functionality

---

### Phase 8: Documentation Updates (Claude AI)

**Claude AI Generated** (~70%):
- Updated `README.md` for GitHub with HF Spaces info
- Updated `deployed.md` with HF Spaces details
- Updated `design-and-evaluation.md` with platform migration
- Created HF Spaces-specific guides

**Example Prompt**:
```
Me: "Update all documentation to reflect migration from Render to 
     HF Spaces. Change URLs, platform specs (16GB RAM), mention 
     Gradio interface, and update deployment instructions."

Claude: [Generated updated documentation for 3 files]
```

**Human Review**:
- ✅ Verified all URLs correct
- ✅ Confirmed technical specs accurate
- ✅ Added personal experiences
- ✅ Final proofreading

---

## Specific AI Prompting Strategies Used

### 1. Iterative Refinement
```
Initial: "Create a RAG chatbot"

Refined: "Create a RAG chatbot using Groq llama-3.1-8b-instant, 
          sentence-transformers embeddings, ChromaDB vector store,
          Gradio interface, deployed on HF Spaces"
```

### 2. Constraint-Based Prompts
```
"Generate code that works with:
 - 16GB RAM on HF Spaces
 - CPU-only (no GPU)
 - Free APIs (Groq, no OpenAI)
 - Python 3.10+
 - Gradio 4.0 framework"
```

### 3. Migration-Specific Prompts
```
"I need to migrate from Render (Flask) to HF Spaces (Gradio):
 - Keep all RAG functionality
 - Convert to Gradio chat interface
 - Ensure 16GB RAM is sufficient
 - Preserve evaluation metrics"
```

### 4. Debugging Prompts
```
"I'm getting this error on HF Spaces: [error message]
 Here's my app.py: [code snippet]
 And my requirements.txt: [dependencies]
 What's wrong?"
```

---

## Code Verification and Human Oversight

### What I Did Manually:

1. **Tested Every Component**:
   - Tested Flask version locally
   - Tested Gradio version locally
   - Deployed to HF Spaces and verified
   - Validated evaluation metrics
   - Tested with multiple queries

2. **Made Critical Decisions**:
   - Chose to migrate from Render to HF Spaces
   - Selected Gradio over Streamlit
   - Approved 16GB RAM allocation
   - Set final chunk parameters (300/30)
   - Configured Top-K=2 (tested 1, 2, 3, 5)

3. **Integrated Components**:
   - Connected Gradio UI to RAG pipeline
   - Ensured evaluation still works
   - Set up HF Spaces secrets
   - Verified deployment workflow

4. **Optimized for Platform**:
   - Verified HF Spaces compatibility
   - Ensured 16GB RAM sufficient
   - Tested build and runtime
   - Confirmed always-on operation

5. **Conducted Evaluation**:
   - Ran 25 test questions on HF deployment
   - Analyzed results (100% accuracy maintained)
   - Documented findings

---

## Platform Migration Journey

### Timeline:

1. **Week 1**: Built with Flask, deployed to Render
2. **Week 2**: Encountered memory issues, frequent OOM
3. **Week 2.5**: Claude AI suggested HF Spaces migration
4. **Week 2.5**: Generated Gradio interface
5. **Week 3**: Deployed to HF Spaces successfully
6. **Week 3**: Updated all documentation

### Lessons Learned:

**Render Challenges**:
- ❌ 512MB RAM too limiting for ML apps
- ❌ Cold starts after 15 minutes
- ❌ Build timeouts frequent
- ❌ Basic Flask UI

**HF Spaces Advantages**:
- ✅ 16GB RAM eliminates memory issues
- ✅ Always-on, no cold starts
- ✅ Beautiful Gradio UI
- ✅ Easy sharing and embedding
- ✅ Better for ML/AI applications

---

## Learning Outcomes

### Skills Developed:

1. **AI Tool Proficiency**:
   - Effective prompt engineering
   - Platform migration with AI guidance
   - Debugging with AI assistance
   - Code review and verification

2. **Technical Skills**:
   - RAG architecture design
   - Vector database usage (ChromaDB)
   - LLM API integration (Groq)
   - Gradio interface development
   - HF Spaces deployment

3. **Project Management**:
   - Platform evaluation and migration
   - Breaking complex projects into AI-assistable chunks
   - Knowing when to use AI vs manual work
   - Integrating AI-generated components

### Productivity Gains:

**Estimated Time Savings**:
```
Without AI: ~100 hours (2.5 weeks full-time)
With AI: ~25 hours (3 days)
Time Saved: 75%
```

**Breakdown**:
- Code Generation: 65% time saved
- Platform Migration: 80% time saved
- Debugging: 80% time saved  
- Documentation: 70% time saved
- Testing: 50% time saved
- Deployment: 70% time saved

---

## Best Practices Learned

### When to Use AI:

✅ **Good Use Cases**:
- Boilerplate code generation
- Framework migrations (Flask → Gradio)
- Configuration file templates
- Standard implementations
- Documentation structure
- Test case generation
- Debugging assistance
- Platform comparison and recommendations

❌ **Poor Use Cases**:
- Critical architecture decisions
- Parameter tuning (needs experimentation)
- Security-sensitive code
- Performance optimization (needs profiling)
- Final testing and validation
- Platform selection (needs human judgment)

### Effective Prompting Tips:

1. **Be Specific**: Include constraints, tech stack, versions, platform
2. **Provide Context**: Share error messages, environment details, platform specs
3. **Iterate**: Start broad, refine with follow-ups
4. **Verify**: Always test AI-generated code
5. **Document**: Keep track of what AI generated vs human-modified
6. **Ask for Comparisons**: When choosing platforms, ask AI for pros/cons

---

## Conclusion

### Summary of AI Usage:

| Component | AI Tool | AI Contribution | Human Contribution |
|-----------|---------|----------------|-------------------|
| Architecture | Claude AI | 30% | 70% (decisions) |
| Core Code | Claude AI | 80% | 20% (modifications) |
| Platform Migration | Claude AI | 80% | 20% (testing) |
| Gradio Interface | Claude AI | 85% | 15% (customization) |
| Debugging | ChatGPT | 90% | 10% (verification) |
| Testing | ChatGPT | 80% | 20% (integration) |
| Documentation | Claude AI | 70% | 30% (final review) |
| **Overall** | | **~70%** | **~30%** |

### Key Takeaways:

1. **AI is a Powerful Accelerator**:
   - 75% time savings overall
   - Rapid prototyping and iteration
   - Excellent for framework migrations
   - Great platform guidance

2. **AI Helped Navigate Challenges**:
   - Identified Render memory limitations
   - Suggested HF Spaces as solution
   - Generated migration code
   - Preserved all functionality

3. **Human Oversight is Essential**:
   - Critical decisions require human judgment
   - Platform migration needed testing
   - AI code needs verification
   - Integration requires human touch

4. **Best Results from Collaboration**:
   - AI for speed, humans for strategy
   - AI for generation, humans for validation
   - AI for suggestions, humans for decisions
   - AI for migration, humans for testing

### Project Success Attribution:

**This project succeeded because**:
- ✅ Used AI for rapid development (Claude + ChatGPT)
- ✅ Made smart platform migration (Render → HF Spaces)
- ✅ Leveraged AI for framework change (Flask → Gradio)
- ✅ Thoroughly tested and validated (100% accuracy)
- ✅ Properly documented and deployed
- ✅ Maintained human oversight and control

**Final Result**: 
- 100% groundedness
- 100% citation accuracy  
- 0.601s median latency
- $0.00 cost
- Professional Gradio UI
- Deployed on HF Spaces with 16GB RAM
- Always-on availability
- Live at: https://huggingface.co/spaces/Mehedi98/Rag_Chatbot

---

## Acknowledgments

**AI Tools**:
- **Claude AI (Anthropic)**: Primary code generation, architecture guidance, and platform migration
- **ChatGPT (OpenAI)**: Debugging, optimization, and testing assistance

**Platforms**:
- **Hugging Face Spaces**: Outstanding ML/AI app hosting
- **Groq**: Lightning-fast free LLM inference
- **Gradio**: Beautiful UI framework

**Human Developer**:
- **Mehedi Islam**: Architecture decisions, platform migration, integration, testing, evaluation, deployment, and final review

---

**Document Version**: 2.0 (Updated for HF Spaces)  
**Last Updated**: October 25, 2025  
**Project**: RAG Policy Chatbot  
**Live Demo**: https://huggingface.co/spaces/Mehedi98/Rag_Chatbot  
**GitHub Repository**: https://github.com/MehediGit98/rag-policy-chatbot
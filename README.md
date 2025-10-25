---
title: Company Policy Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🤖 Company Policy Assistant

An intelligent chatbot that helps employees find answers about company policies using Retrieval-Augmented Generation (RAG).

## 🌟 Features

- **Natural Language Q&A**: Ask questions in plain English
- **Source Citations**: Every answer includes references to policy documents
- **Fast Responses**: Powered by Groq's Llama 3.1 model
- **Comprehensive Coverage**: PTO, Remote Work, Expenses, Security, Holidays

## 🚀 How It Works

This application uses RAG (Retrieval-Augmented Generation) to:
1. **Index** company policy documents into a vector database
2. **Retrieve** relevant policy sections based on your question
3. **Generate** accurate answers with proper citations

## 🛠️ Technology Stack

- **LLM**: Groq (Llama 3.1-8B-Instant)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: ChromaDB
- **Framework**: LangChain
- **Interface**: Gradio

## 📚 Policy Documents

The assistant can answer questions about:
- PTO (Paid Time Off) Policy
- Remote Work Policy
- Expense Reimbursement Policy
- Security Policy
- Holiday Schedule

## 🔧 Configuration

The system is configured with:
- Chunk Size: 300 tokens
- Top-K Retrieval: 2 most relevant chunks
- Temperature: 0.3 (focused responses)
- Max Tokens: 300

## 🏃 Try It Out

Simply type your question in the chat interface. For example:
- "How many PTO days do employees get?"
- "What is the remote work policy?"
- "How do I submit expense reports?"

## 📝 Source Code

Full source code and documentation: [GitHub Repository](https://github.com/MehediGit98/rag-policy-chatbot)

## 📄 License

MIT License - See repository for details

## 🙏 Acknowledgments

Built with ❤️ using:
- [Groq](https://groq.com) for fast LLM inference
- [Hugging Face](https://huggingface.co) for embeddings and hosting
- [LangChain](https://langchain.com) for RAG pipeline
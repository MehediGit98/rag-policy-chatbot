# src/retrieval.py (Improved retrieval and prompt engineering)
from typing import List, Dict, Optional
import logging
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from .config import Config

# CHANGE: Import from the new dedicated package
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Conditional LLM imports
if Config.USE_GROQ:
    from langchain_groq import ChatGroq
else:
    from langchain_openai import ChatOpenAI

# Set up structured logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class RAGRetriever:
    """Retrieval-Augmented Generation (RAG) retriever for company policies."""

    def __init__(self):
        self.config = Config()
        logger.info("Initializing embeddings...")
        self.embeddings = HuggingFaceEmbeddings(model_name=self.config.EMBEDDING_MODEL)

        logger.info("Loading vector store from %s...", self.config.CHROMA_DIR)
        self.vector_store = Chroma(
            persist_directory=self.config.CHROMA_DIR,
            embedding_function=self.embeddings
        )

        # Dynamic LLM selection
        if self.config.USE_GROQ:
            logger.info("Using Groq LLM: %s", self.config.GROQ_MODEL)
            self.llm = ChatGroq(
                model=self.config.GROQ_MODEL,
                groq_api_key=self.config.GROQ_API_KEY,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS
            )
        else:
            logger.info("Using OpenAI LLM")
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS,
                openai_api_key=os.getenv('OPENAI_API_KEY', '')
            )

    def retrieve_documents(self, query: str, k: Optional[int] = None) -> List[Dict]:
        """Retrieve top-k relevant documents from vector store with better scoring."""
        # Use higher K for retrieval, then select best ones
        k_retrieval = (k or self.config.TOP_K) * 2  # Retrieve more, then filter
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k_retrieval)
        except Exception as e:
            logger.error("Error during document retrieval: %s", e)
            return []

        # Process and score results
        retrieved_docs = []
        for doc, score in results:
            retrieved_docs.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", 0),
                "score": float(score),
            })
        
        # Sort by relevance (lower score is better for distance)
        retrieved_docs.sort(key=lambda x: x["score"])
        
        # Take top K after sorting
        final_k = k or self.config.TOP_K
        retrieved_docs = retrieved_docs[:final_k]
        
        logger.info("Retrieved %d documents for query: %s", len(retrieved_docs), query)
        return retrieved_docs

    def generate_answer(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        """Generate answer using retrieved documents with improved prompt."""
        if not retrieved_docs:
            return {
                "answer": "I can only answer questions about our company policies. "
                          "No relevant information found for your question.",
                "citations": [],
                "retrieved_docs": []
            }

        # Build context with all information
        context_parts = []
        for i, doc in enumerate(retrieved_docs):
            context_parts.append(f"[Source {i+1}: {doc['source']}]\n{doc['content']}")

        context = "\n\n---\n\n".join(context_parts)

        # Improved prompt with better instructions
        prompt = f"""You are a helpful company policy assistant. Your job is to answer employee questions based ONLY on the provided policy documents.

CRITICAL INSTRUCTIONS:
1. READ ALL THE CONTEXT CAREFULLY before answering
2. Answer ONLY using information from the context below
3. If the answer is in the context, provide a clear and complete response
4. ALWAYS cite your sources using [1], [2], [3] notation
5. If multiple sources contain relevant information, use all of them
6. If the context doesn't clearly answer the question, say "I don't have enough information in our policy documents to answer that question."
7. Be specific with numbers, dates, and details when available
8. Keep your answer concise but complete

CONTEXT FROM COMPANY POLICIES:

{context}

QUESTION: {query}

ANSWER (include citations [1], [2], etc.):"""

        try:
            response = self.llm.invoke(prompt)
            answer_text = response.content
            
            # Build citations from all retrieved documents
            citations = []
            seen_sources = set()
            
            for i, doc in enumerate(retrieved_docs):
                source = doc["source"]
                # Only add each source once, but include snippet from best match
                if source not in seen_sources:
                    seen_sources.add(source)
                    snippet = doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"]
                    citations.append({
                        "index": len(citations) + 1,
                        "source": source,
                        "snippet": snippet
                    })
            
            logger.info("Generated answer successfully for query: %s", query)
            return {
                "answer": answer_text,
                "citations": citations,
                "retrieved_docs": retrieved_docs
            }
        except Exception as e:
            logger.error("Error generating answer: %s", e)
            return {
                "answer": f"Error generating response: {str(e)}",
                "citations": [],
                "retrieved_docs": retrieved_docs
            }

    def query(self, question: str) -> Dict:
        """Run full RAG pipeline: retrieve documents and generate answer."""
        retrieved_docs = self.retrieve_documents(question)
        result = self.generate_answer(question, retrieved_docs)
        return result
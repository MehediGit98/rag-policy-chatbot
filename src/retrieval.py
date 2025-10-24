# src/retrieval.py
from typing import List, Dict, Optional
import logging
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

from config import Config
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

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
        """Retrieve top-k relevant documents from vector store."""
        k = k or self.config.TOP_K
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
        except Exception as e:
            logger.error("Error during document retrieval: %s", e)
            return []

        retrieved_docs = [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", 0),
                "score": float(score),
            }
            for doc, score in results
        ]
        logger.info("Retrieved %d documents for query: %s", len(retrieved_docs), query)
        return retrieved_docs

    def generate_answer(self, query: str, retrieved_docs: List[Dict]) -> Dict:
        """Generate answer using retrieved documents."""
        if not retrieved_docs:
            return {
                "answer": "I can only answer questions about our company policies. "
                          "No relevant information found.",
                "citations": [],
                "retrieved_docs": []
            }

        # Build context for LLM
        context_parts = [
            f"[{i+1}] Source: {doc['source']}\n{doc['content']}"
            for i, doc in enumerate(retrieved_docs)
        ]

        # ✅ Deduplicate sources — keep only one representative chunk per file (best-scoring one)
        unique_sources = {}
        for doc in retrieved_docs:
            src = doc["source"]
            if src not in unique_sources or doc["score"] < unique_sources[src]["score"]:
                unique_sources[src] = {"content": doc["content"], "score": doc["score"]}

        citations = [
            {
                "index": i + 1,
                "source": src,
                "snippet": (info["content"][:200] + "..." if len(info["content"]) > 200 else info["content"])
            }
            for i, (src, info) in enumerate(unique_sources.items())
        ]

        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = f"""You are a helpful assistant that answers questions about company policies based solely on the provided context.

IMPORTANT RULES:
1. Only answer based on the information in the context below.
2. If the context doesn't contain the answer, say "I can only answer questions about our company policies. The information you're looking for is not in our policy documents."
3. Always cite your sources using [number] notation.
4. Keep answers concise and under 500 tokens.
5. Do not make up information not present in the context.

Context:
{context}

Question: {query}

Answer (with citations):"""

        try:
            response = self.llm.invoke(prompt)
            answer_text = response.content
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

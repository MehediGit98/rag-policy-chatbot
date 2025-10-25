"""
Optimized configuration for better retrieval and answers
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration - Using Groq (Free, no credit card)
    USE_GROQ = os.getenv('USE_GROQ', 'true').lower() == 'true'
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Model Configuration - Groq Models (API-based, no local memory)
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    # Embedding Model - Small and efficient
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # 🔥 IMPROVED: Better chunking and retrieval for more complete answers
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 400))  # Increased from 300 for more context
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))  # Increased overlap for better continuity
    TOP_K = int(os.getenv('TOP_K', 4))  # Increased from 2 to get more relevant chunks
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))  # Increased from 300 for complete answers
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.2))  # Lowered for more focused answers
    
    # Paths
    DATA_DIR = 'data/policies'
    CHROMA_DIR = 'chroma_db'
    
    # Application
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if cls.USE_GROQ and not cls.GROQ_API_KEY:
            print("⚠️  WARNING: GROQ_API_KEY not set!")
            print("   Get a free API key at: https://console.groq.com/keys")
            print("   No credit card required!")
            return False
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (safe for logs)."""
        print("=" * 60)
        print("RAG System Configuration (Optimized for Better Answers)")
        print("=" * 60)
        print(f"LLM Provider:      {'Groq (API)' if cls.USE_GROQ else 'OpenAI'}")
        print(f"LLM Model:         {cls.GROQ_MODEL}")
        print(f"Embedding Model:   {cls.EMBEDDING_MODEL}")
        print(f"Chunk Size:        {cls.CHUNK_SIZE} tokens")
        print(f"Chunk Overlap:     {cls.CHUNK_OVERLAP} tokens")
        print(f"Top-K Retrieval:   {cls.TOP_K} chunks")
        print(f"Max Tokens:        {cls.MAX_TOKENS} tokens")
        print(f"Temperature:       {cls.TEMPERATURE}")
        print(f"API Key Set:       {'✅' if cls.GROQ_API_KEY else '❌'}")
        print("=" * 60)
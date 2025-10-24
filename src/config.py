"""
Configuration for RAG application with compatible versions
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration - Using Groq (Free, no credit card)
    USE_GROQ = os.getenv('USE_GROQ', 'true').lower() == 'true'
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Model Configuration - Groq Models
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    # Embedding Model - Compatible with available versions
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L3-v2')
    
    # RAG Parameters
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 400))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 40))
    TOP_K = int(os.getenv('TOP_K', 3))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.3))
    
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
        print("RAG System Configuration (Compatible Versions)")
        print("=" * 60)
        print(f"LLM Provider:      {'Groq' if cls.USE_GROQ else 'OpenAI'}")
        print(f"LLM Model:         {cls.GROQ_MODEL if cls.USE_GROQ else 'OpenAI Model'}")
        print(f"Embedding Model:   {cls.EMBEDDING_MODEL}")
        print(f"Chunk Size:        {cls.CHUNK_SIZE}")
        print(f"Chunk Overlap:     {cls.CHUNK_OVERLAP}")
        print(f"Top-K Retrieval:   {cls.TOP_K}")
        print(f"Max Tokens:        {cls.MAX_TOKENS}")
        print(f"Temperature:       {cls.TEMPERATURE}")
        print(f"API Key Set:       {'✅' if cls.GROQ_API_KEY else '❌'}")
        print("=" * 60)
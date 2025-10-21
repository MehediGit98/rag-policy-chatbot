"""
Configuration for RAG application using CURRENT Groq FREE models (October 2025)
Updated with latest supported models
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration - Using Groq (Free, no credit card)
    USE_GROQ = os.getenv('USE_GROQ', 'true').lower() == 'true'
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Model Configuration - CURRENT Groq Models (2025)
    # PRODUCTION MODELS (Recommended - Stable):
    # - llama-3.3-70b-versatile (Best quality, 70B params, 131K context)
    # - llama-3.1-8b-instant (Fast, 8B params, 131K context) ✅ RECOMMENDED
    # - gemma2-9b-it (Good quality, 9B params, 8K context)
    #
    # PREVIEW MODELS (May be discontinued):
    # - deepseek-r1-distill-llama-70b (Reasoning model, 70B params)
    # - qwen/qwen3-32b (32B params, 131K context)
    
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')  # Best for free tier
    
    # Embedding Model - Small and local, no API needed
    # CURRENT OPTIONS (All free and work on 8GB RAM):
    # - sentence-transformers/all-MiniLM-L6-v2 (80MB, 384 dim) ✅ RECOMMENDED
    # - sentence-transformers/all-mpnet-base-v2 (420MB, 768 dim, better quality)
    # - sentence-transformers/paraphrase-MiniLM-L3-v2 (60MB, 384 dim, faster)
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # RAG Parameters - Optimized for free tier and low memory
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
        print("RAG System Configuration (FREE Models - Oct 2025)")
        print("=" * 60)
        print(f"LLM Provider:      Groq (Free)")
        print(f"LLM Model:         {cls.GROQ_MODEL}")
        print(f"  Context:         131K tokens")
        print(f"  Speed:           ~800 tokens/sec")
        print(f"Embedding Model:   {cls.EMBEDDING_MODEL}")
        print(f"  Size:            ~80MB")
        print(f"  Device:          CPU")
        print(f"Chunk Size:        {cls.CHUNK_SIZE}")
        print(f"Chunk Overlap:     {cls.CHUNK_OVERLAP}")
        print(f"Top-K Retrieval:   {cls.TOP_K}")
        print(f"Max Tokens:        {cls.MAX_TOKENS}")
        print(f"Temperature:       {cls.TEMPERATURE}")
        print(f"API Key Set:       {'✅' if cls.GROQ_API_KEY else '❌'}")
        print("=" * 60)
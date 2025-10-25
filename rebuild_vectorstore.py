#!/usr/bin/env python3
"""
Rebuild the vector store with improved chunking settings
Run this after updating config.py to get better retrieval
"""

import os
import shutil
from pathlib import Path
from src.ingestion import DocumentIngestion
from src.config import Config

def rebuild_vector_store():
    """Delete old vector store and rebuild with new settings."""
    
    config = Config()
    chroma_path = Path(config.CHROMA_DIR)
    
    print("=" * 70)
    print("REBUILDING VECTOR STORE WITH IMPROVED SETTINGS")
    print("=" * 70)
    print()
    
    # Print new configuration
    config.print_config()
    print()
    
    # Step 1: Delete old vector store
    if chroma_path.exists():
        print(f"🗑️  Deleting old vector store at {chroma_path}...")
        shutil.rmtree(chroma_path)
        print("✅ Old vector store deleted")
    else:
        print(f"ℹ️  No existing vector store found at {chroma_path}")
    
    print()
    
    # Step 2: Rebuild with new settings
    print("🔨 Building new vector store with improved settings...")
    print(f"   - Chunk Size: {config.CHUNK_SIZE} tokens")
    print(f"   - Chunk Overlap: {config.CHUNK_OVERLAP} tokens")
    print(f"   - This will retrieve TOP-{config.TOP_K} chunks per query")
    print()
    
    ingestion = DocumentIngestion()
    vector_store = ingestion.ingest_all()
    
    print()
    print("=" * 70)
    print("✅ VECTOR STORE REBUILT SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("📊 Improvements:")
    print("   ✅ Larger chunks (400 tokens) for more complete context")
    print("   ✅ More overlap (50 tokens) for better continuity")
    print("   ✅ Retrieving 4 chunks instead of 2 for comprehensive answers")
    print("   ✅ Lower temperature (0.2) for more focused responses")
    print()
    print("🚀 You can now test the chatbot with better retrieval!")
    print()

if __name__ == "__main__":
    rebuild_vector_store()
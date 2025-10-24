# src/ingestion.py (Import changes)
import os
from pathlib import Path
from typing import List, Dict

import markdown
from bs4 import BeautifulSoup
from pypdf import PdfReader

# Correct imports for modern LangChain (v0.2.x+)
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from .config import Config

class DocumentIngestion:
    def __init__(self):
        self.config = Config()
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def load_document(self, file_path: str) -> Dict[str, str]:
        """Load a single document and return its content and metadata."""
        path = Path(file_path)
        file_name = path.name

        if path.suffix == ".pdf":
            content = self._load_pdf(file_path)
        elif path.suffix == ".md":
            content = self._load_markdown(file_path)
        elif path.suffix == ".html":
            content = self._load_html(file_path)
        elif path.suffix == ".txt":
            content = self._load_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        return {
            "content": content,
            "source": file_name,
            "file_path": str(file_path)
        }

    def _load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    def _load_markdown(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text().strip()

    def _load_html(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text().strip()

    def _load_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Split documents into chunks with metadata."""
        all_chunks = []

        for doc in documents:
            chunks = self.text_splitter.split_text(doc["content"])
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "content": chunk,
                    "source": doc["source"],
                    "chunk_id": i,
                    "file_path": doc["file_path"]
                })

        return all_chunks

    def create_vector_store(self, chunks: List[Dict]) -> Chroma:
        """Create and persist vector store from chunks."""
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "file_path": chunk["file_path"]
            }
            for chunk in chunks
        ]

        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=self.config.CHROMA_DIR
        )

        return vector_store

    def ingest_all(self):
        """Main ingestion pipeline."""
        print("Starting document ingestion...")

        # Load all documents
        documents = []
        data_path = Path(self.config.DATA_DIR)

        for file_path in data_path.glob("*"):
            if file_path.is_file():
                try:
                    doc = self.load_document(str(file_path))
                    documents.append(doc)
                    print(f"Loaded: {file_path.name}")
                except Exception as e:
                    print(f"Error loading {file_path.name}: {e}")

        # Chunk documents
        print(f"\nChunking {len(documents)} documents...")
        chunks = self.chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")

        # Create vector store
        print("\nCreating vector store...")
        vector_store = self.create_vector_store(chunks)
        print("Vector store created successfully!")

        return vector_store


if __name__ == "__main__":
    ingestion = DocumentIngestion()
    ingestion.ingest_all()
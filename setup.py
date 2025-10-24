# setup.py
from setuptools import setup, find_packages

setup(
    name="rag-policy-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask==2.3.3",
        "python-dotenv==1.0.1",
        "requests==2.32.3",
        "beautifulsoup4==4.12.2",
        "pypdf==3.17.0",
        "markdown==3.6",
        "langchain==0.0.354",
        "langchain-community==0.0.29",
        "chromadb==0.4.22",
        "sentence-transformers==2.2.2",
        "langchain-groq==0.1.2",
        "langchain-openai==0.0.8",
        "huggingface-hub==0.20.3",
        "torch==2.1.2",
        "transformers==4.36.2",
        "numpy==1.24.3",
        "scikit-learn==1.3.2",
    ],
    python_requires=">=3.8",
)
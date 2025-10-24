# setup.py
from setuptools import setup, find_packages

setup(
    name="rag-policy-assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "pypdf",
        "markdown",
        "langchain",
        "langchain-community",
        "chromadb",
        "sentence-transformers",
        "langchain-groq",
        "langchain-openai",
        "huggingface-hub",
        "torch",
        "transformers",
        "numpy",
        "scikit-learn",
        "tqdm",
    ],
    python_requires=">=3.13",
)
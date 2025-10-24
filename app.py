# src/app.py
from flask import Flask, render_template, request, jsonify
from src.retrieval import RAGRetriever
from .config import Config  # FIX: Updated to relative import
import time
import os

app = Flask(__name__)
config = Config()

# -----------------------------------------------------------
# FIX: Lazy Initialization to prevent Out-of-Memory (OOM) error
# -----------------------------------------------------------
rag_retriever = None

def initialize_rag():
    """Initializes the RAGRetriever instance once per worker."""
    global rag_retriever
    # Check if the retriever has already been initialized (None) or failed (False)
    if rag_retriever is None:
        try:
            # This is the memory-intensive step.
            rag_retriever = RAGRetriever()
            print("RAG system initialized successfully (Lazy Load)")
        except Exception as e:
            # If initialization fails, mark it as False to avoid repeated crashes
            print(f"Error initializing RAG system: {e}")
            rag_retriever = False 

# Initialize the retriever when the application is run/first requested
with app.app_context():
    initialize_rag()
# -----------------------------------------------------------

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'rag_initialized': rag_retriever is not None and rag_retriever is not False,
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint."""
    start_time = time.time()
    
    # Check if initialization failed
    if rag_retriever is False:
        return jsonify({
            'error': 'RAG system failed to initialize. Check logs for OOM or dependency errors.'
        }), 500
    
    # Check if initialization is still pending (should not happen with the `with app.app_context` block above)
    if rag_retriever is None:
        return jsonify({
            'error': 'RAG system is still loading. Please try again in a moment.'
        }), 503

    
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({
            'error': 'Question is required'
        }), 400
    
    question = data['question']
    
    if not question.strip():
        return jsonify({
            'error': 'Question cannot be empty'
        }), 400
    
    try:
        # Get answer from RAG system
        result = rag_retriever.query(question)
        
        latency = time.time() - start_time
        
        return jsonify({
            'answer': result['answer'],
            'citations': result['citations'],
            'latency': round(latency, 3),
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': f"An unexpected error occurred during chat: {str(e)}",
            'success': False
        }), 500

if __name__ == '__main__':
    if config.DEBUG:
        app.run(host='0.0.0.0', port=config.PORT, debug=True)
    else:
        # In a production environment, Gunicorn will handle the startup
        # We ensure the rag_retriever is initialized here for local testing
        pass
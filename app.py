### 7. app.py
from flask import Flask, render_template, request, jsonify
from src.retrieval import RAGRetriever
from src.config import Config
import time
import os

app = Flask(__name__)
config = Config()

# Initialize RAG retriever
try:
    rag_retriever = RAGRetriever()
    print("RAG system initialized successfully")
except Exception as e:
    print(f"Error initializing RAG system: {e}")
    rag_retriever = None

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'rag_initialized': rag_retriever is not None,
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint."""
    start_time = time.time()
    
    if not rag_retriever:
        return jsonify({
            'error': 'RAG system not initialized'
        }), 500
    
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
            'error': f'Error processing question: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    port = config.PORT
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)

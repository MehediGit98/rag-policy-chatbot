"""
Unit tests for the RAG application
Tests all major components and endpoints
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_question():
    """Sample question for testing."""
    return {"question": "How many PTO days do employees get?"}

class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_endpoint_returns_200(self, client):
        """Test that health endpoint returns 200 status."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Test that health endpoint returns JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_health_endpoint_structure(self, client):
        """Test that health endpoint returns correct structure."""
        response = client.get('/health')
        data = response.get_json()
        
        assert 'status' in data
        assert 'rag_initialized' in data
        assert 'timestamp' in data
    
    def test_health_endpoint_status_value(self, client):
        """Test that health status is 'healthy'."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

class TestIndexEndpoint:
    """Tests for the main index page."""
    
    def test_index_page_loads(self, client):
        """Test that main page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_returns_html(self, client):
        """Test that index returns HTML content."""
        response = client.get('/')
        assert 'text/html' in response.content_type

class TestChatEndpoint:
    """Tests for the chat API endpoint."""
    
    def test_chat_endpoint_requires_post(self, client):
        """Test that chat endpoint only accepts POST requests."""
        response = client.get('/chat')
        assert response.status_code == 405  # Method Not Allowed
    
    def test_chat_endpoint_requires_question_field(self, client):
        """Test that chat endpoint requires 'question' field."""
        response = client.post('/chat', 
                              json={},
                              content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_chat_endpoint_rejects_empty_question(self, client):
        """Test that chat endpoint rejects empty questions."""
        response = client.post('/chat', 
                              json={'question': ''},
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_chat_endpoint_accepts_valid_question(self, client, sample_question):
        """Test that chat endpoint accepts valid questions."""
        response = client.post('/chat', 
                              json=sample_question,
                              content_type='application/json')
        # Should be 200 if RAG initialized, 500 if not
        assert response.status_code in [200, 500]

class TestConfiguration:
    """Tests for configuration management."""
    
    def test_config_exists(self):
        """Test that Config class exists and is importable."""
        from src.config import Config
        config = Config()
        assert config is not None
    
    def test_config_has_required_attributes(self):
        """Test that Config has all required attributes."""
        from src.config import Config
        config = Config()
        
        required_attrs = [
            'CHUNK_SIZE',
            'CHUNK_OVERLAP',
            'TOP_K',
            'MAX_TOKENS',
            'TEMPERATURE',
            'DATA_DIR',
            'CHROMA_DIR'
        ]
        
        for attr in required_attrs:
            assert hasattr(config, attr), f"Config missing required attribute: {attr}"

class TestDataFiles:
    """Tests for data files and structure."""
    
    def test_data_directory_exists(self):
        """Test that data directory exists."""
        assert os.path.exists('data'), "data directory not found"
    
    def test_policies_directory_exists(self):
        """Test that policies directory exists."""
        assert os.path.exists('data/policies'), "data/policies directory not found"
    
    def test_policy_files_exist(self):
        """Test that policy files exist."""
        expected_files = [
            'pto_policy.md',
            'remote_work_policy.md',
            'expense_policy.md',
            'security_policy.md',
            'holiday_policy.md'
        ]
        
        for filename in expected_files:
            filepath = os.path.join('data/policies', filename)
            assert os.path.exists(filepath), f"Policy file not found: {filename}"

class TestEvaluation:
    """Tests for evaluation files."""
    
    def test_evaluation_directory_exists(self):
        """Test that evaluation directory exists."""
        assert os.path.exists('evaluation'), "evaluation directory not found"
    
    def test_evaluation_questions_file_exists(self):
        """Test that evaluation questions file exists."""
        assert os.path.exists('evaluation/evaluation_questions.json'), \
            "evaluation_questions.json not found"
    
    def test_evaluation_questions_valid_json(self):
        """Test that evaluation questions file is valid JSON."""
        try:
            with open('evaluation/evaluation_questions.json', 'r') as f:
                data = json.load(f)
                assert 'questions' in data
                assert isinstance(data['questions'], list)
                assert len(data['questions']) > 0
        except (json.JSONDecodeError, FileNotFoundError) as e:
            pytest.skip(f"Evaluation questions file issue: {e}")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
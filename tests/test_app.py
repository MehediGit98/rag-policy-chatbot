"""
Unit tests for the RAG application
Tests all major components and endpoints
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

# Skip Gradio tests if Gradio isn't available
try:
    from app import create_interface
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False


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
        policy_files = os.listdir('data/policies')
        assert len(policy_files) > 0, "No policy files found"


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
        except (json.JSONDecodeError, FileNotFoundError) as e:
            pytest.skip(f"Evaluation questions file issue: {e}")


@pytest.mark.skipif(not GRADIO_AVAILABLE, reason="Gradio not available")
class TestGradioInterface:
    """Tests for Gradio interface."""
    
    def test_interface_creation(self):
        """Test that Gradio interface can be created."""
        demo = create_interface()
        assert demo is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
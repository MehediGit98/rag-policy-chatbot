"""
Evaluation script for RAG system
Runs comprehensive evaluation on test questions and generates report
with compatible versions
"""

import json
import time
import sys
import os
from typing import List, Dict
from collections import defaultdict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval import RAGRetriever
from src.config import Config
from src.evaluation import (
    AnswerEvaluator, 
    LatencyEvaluator, 
    RetrievalEvaluator,
    format_evaluation_report
)


class RAGSystemEvaluator:
    """Complete evaluation framework for RAG system."""
    
    def __init__(self, questions_file: str = 'evaluation/evaluation_questions.json'):
        self.questions_file = questions_file
        self.config = Config()
        self.retriever = RAGRetriever()  # Dynamic LLM selection inside

        # Initialize evaluators
        self.answer_evaluator = AnswerEvaluator()
        self.latency_evaluator = LatencyEvaluator()
        self.retrieval_evaluator = RetrievalEvaluator()

        # Results storage
        self.detailed_results = []
        self.category_results = defaultdict(lambda: {
            'groundedness': [],
            'citation_accuracy': [],
            'partial_match': [],
            'latencies': []
        })
    
    def load_evaluation_questions(self) -> List[Dict]:
        """Load evaluation questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                data = json.load(f)
            return data.get('questions', [])
        except FileNotFoundError:
            print(f"❌ Could not find {self.questions_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {self.questions_file}: {e}")
            sys.exit(1)
    
    def evaluate_single_question(self, question_data: Dict) -> Dict:
        """Evaluate a single question."""
        question_text = question_data['question']
        gold_answer = question_data.get('gold_answer', '')
        expected_source = question_data.get('expected_source', None)
        category = question_data.get('category', 'Unknown')
        
        # Measure latency
        start_time = time.time()
        try:
            result = self.retriever.query(question_text)
            latency = time.time() - start_time
        except Exception as e:
            return {
                'question': question_text,
                'category': category,
                'error': str(e),
                'latency': 0,
                'grounded': False,
                'citation_accurate': False,
                'partial_match': 0.0
            }
        
        # Extract results
        answer = result.get('answer', '')
        citations = result.get('citations', [])
        retrieved_docs = result.get('retrieved_docs', [])

        # Evaluate
        is_grounded, _ = self.answer_evaluator.evaluate_groundedness(answer, retrieved_docs)
        citation_score, _ = self.answer_evaluator.evaluate_citation_accuracy(answer, citations, expected_source)
        partial_match_score, _ = self.answer_evaluator.calculate_partial_match(answer, gold_answer)
        retrieval_score, _ = self.retrieval_evaluator.evaluate_relevance(question_text, retrieved_docs, expected_source)
        self.latency_evaluator.add_latency(latency)
        
        return {
            'question': question_text,
            'category': category,
            'answer': answer,
            'gold_answer': gold_answer,
            'expected_source': expected_source,
            'latency': round(latency, 3),
            'grounded': is_grounded,
            'citation_accurate': citation_score >= 0.5,
            'citation_score': citation_score,
            'partial_match': partial_match_score,
            'retrieval_score': retrieval_score,
            'num_citations': len(citations),
            'num_retrieved': len(retrieved_docs)
        }
    
    def run_evaluation(self) -> Dict:
        """Run complete evaluation on all questions."""
        questions = self.load_evaluation_questions()
        total_questions = len(questions)
        
        for question_data in questions:
            result = self.evaluate_single_question(question_data)
            self.detailed_results.append(result)
            
            category = result['category']
            cat_results = self.category_results[category]
            cat_results['groundedness'].append(1 if result['grounded'] else 0)
            cat_results['citation_accuracy'].append(1 if result['citation_accurate'] else 0)
            cat_results['partial_match'].append(result['partial_match'])
            cat_results['latencies'].append(result['latency'])
        
        metrics = self._calculate_aggregate_metrics()
        self._save_results(metrics)
        print(format_evaluation_report(metrics))
        return metrics
    
    def _calculate_aggregate_metrics(self) -> Dict:
        """Calculate aggregate metrics from results."""
        groundedness_scores = [r['grounded'] for r in self.detailed_results]
        citation_scores = [r['citation_accurate'] for r in self.detailed_results]
        partial_match_scores = [r['partial_match'] for r in self.detailed_results]
        latency_stats = self.latency_evaluator.get_statistics()
        retrieval_scores = [r['retrieval_score'] for r in self.detailed_results]

        category_breakdown = {}
        for category, results in self.category_results.items():
            category_breakdown[category] = {
                'groundedness': sum(results['groundedness']) / len(results['groundedness']) if results['groundedness'] else 0,
                'citation_accuracy': sum(results['citation_accuracy']) / len(results['citation_accuracy']) if results['citation_accuracy'] else 0,
                'partial_match': sum(results['partial_match']) / len(results['partial_match']) if results['partial_match'] else 0,
                'avg_latency': sum(results['latencies']) / len(results['latencies']) if results['latencies'] else 0,
                'count': len(results['groundedness'])
            }

        passed = sum(1 for r in self.detailed_results if r['grounded'] and r['citation_accurate'])
        summary = {
            'total_questions': len(self.detailed_results),
            'passed': passed,
            'failed': len(self.detailed_results) - passed,
            'success_rate': passed / len(self.detailed_results) if self.detailed_results else 0
        }

        return {
            'answer_quality': {
                'groundedness': sum(groundedness_scores)/len(groundedness_scores) if groundedness_scores else 0,
                'citation_accuracy': sum(citation_scores)/len(citation_scores) if citation_scores else 0,
                'partial_match': sum(partial_match_scores)/len(partial_match_scores) if partial_match_scores else 0
            },
            'system_metrics': {
                'latency_p50': latency_stats['p50'],
                'latency_p95': latency_stats['p95'],
                'latency_mean': latency_stats['mean'],
                'latency_min': latency_stats['min'],
                'latency_max': latency_stats['max']
            },
            'retrieval_metrics': {
                'avg_relevance': sum(retrieval_scores)/len(retrieval_scores) if retrieval_scores else 0
            },
            'category_breakdown': category_breakdown,
            'summary': summary
        }
    
    def _save_results(self, metrics: Dict):
        """Save evaluation results to JSON file."""
        output_data = {
            'summary': metrics,
            'detailed_results': self.detailed_results,
            'evaluation_config': {
                'chunk_size': self.config.CHUNK_SIZE,
                'chunk_overlap': self.config.CHUNK_OVERLAP,
                'top_k': self.config.TOP_K,
                'llm_model': self.config.GROQ_MODEL if self.config.USE_GROQ else 'OpenAI',
                'embedding_model': self.config.EMBEDDING_MODEL,
                'temperature': self.config.TEMPERATURE,
                'max_tokens': self.config.MAX_TOKENS
            },
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        os.makedirs('evaluation', exist_ok=True)
        with open('evaluation/evaluation_results.json', 'w') as f:
            json.dump(output_data, f, indent=2)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run RAG system evaluation')
    parser.add_argument('--questions', type=str, default='evaluation/evaluation_questions.json')
    args = parser.parse_args()

    evaluator = RAGSystemEvaluator(questions_file=args.questions)
    evaluator.run_evaluation()
    print("✅ Evaluation complete!")


if __name__ == "__main__":
    main()
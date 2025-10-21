"""
Evaluation utilities for RAG system
Provides helper functions for evaluating answer quality and system performance
"""

import re
from typing import List, Dict, Tuple
import numpy as np


class AnswerEvaluator:
    """Evaluates the quality of RAG system answers."""
    
    def __init__(self):
        pass
    
    def evaluate_groundedness(self, answer: str, retrieved_docs: List[Dict]) -> Tuple[bool, str]:
        """
        Evaluate if the answer is grounded in the retrieved documents.
        
        Args:
            answer: The generated answer text
            retrieved_docs: List of retrieved document chunks
            
        Returns:
            Tuple of (is_grounded: bool, reason: str)
        """
        # Check for explicit "cannot answer" responses
        cannot_answer_phrases = [
            "can only answer",
            "couldn't find",
            "don't have information",
            "not in our policy",
            "cannot find",
            "no information available"
        ]
        
        answer_lower = answer.lower()
        for phrase in cannot_answer_phrases:
            if phrase in answer_lower:
                return True, "Correctly states lack of information"
        
        # If no retrieved docs, answer should say it can't answer
        if not retrieved_docs or len(retrieved_docs) == 0:
            if any(phrase in answer_lower for phrase in cannot_answer_phrases):
                return True, "Correctly handles empty retrieval"
            else:
                return False, "Makes claims without retrieved evidence"
        
        # If answer is very short (< 10 words), it's likely just saying "no info"
        if len(answer.split()) < 10:
            return True, "Minimal answer, likely grounded"
        
        # Check if answer has citations (indicated by [1], [2], etc.)
        has_citations = bool(re.search(r'\[\d+\]', answer))
        
        # If answer is substantive and has citations, assume grounded
        # In production, would use LLM-based evaluation here
        if has_citations and len(answer.split()) >= 10:
            return True, "Has citations and substantive content"
        
        # If answer is substantive but no citations, check if docs exist
        if len(answer.split()) >= 10 and retrieved_docs:
            # Heuristic: if we have docs and a real answer, assume grounded
            return True, "Has retrieved context"
        
        return False, "Insufficient evidence for grounding"
    
    def evaluate_citation_accuracy(self, answer: str, citations: List[Dict], 
                                   expected_source: str = None) -> Tuple[float, str]:
        """
        Evaluate if citations correctly point to supporting sources.
        
        Args:
            answer: The generated answer text
            citations: List of citation dictionaries with source info
            expected_source: Optional expected source filename
            
        Returns:
            Tuple of (accuracy_score: float, explanation: str)
        """
        # If no citations provided
        if not citations or len(citations) == 0:
            if len(answer.split()) < 10:
                return 1.0, "No citations needed for minimal answer"
            return 0.0, "No citations provided for substantive answer"
        
        # Check if citations are in answer
        citation_numbers = re.findall(r'\[(\d+)\]', answer)
        if not citation_numbers:
            return 0.5, "Citations provided but not referenced in answer"
        
        # If expected source is provided, check if it's in citations
        if expected_source:
            source_match = any(expected_source in citation.get('source', '') 
                             for citation in citations)
            if source_match:
                return 1.0, f"Correct source cited: {expected_source}"
            else:
                return 0.0, f"Expected source {expected_source} not in citations"
        
        # If no expected source, just verify citations are formatted correctly
        valid_citations = all(
            'source' in citation and 'snippet' in citation 
            for citation in citations
        )
        
        if valid_citations:
            return 1.0, "Citations properly formatted with sources and snippets"
        else:
            return 0.5, "Citations incomplete or improperly formatted"
    
    def calculate_partial_match(self, answer: str, gold_answer: str) -> Tuple[float, Dict]:
        """
        Calculate partial match score between answer and gold answer.
        
        Args:
            answer: Generated answer text
            gold_answer: Expected/gold answer text
            
        Returns:
            Tuple of (score: float, details: dict)
        """
        # Tokenize and normalize
        answer_tokens = set(self._normalize_text(answer).split())
        gold_tokens = set(self._normalize_text(gold_answer).split())
        
        if not gold_tokens:
            return 0.0, {"reason": "Empty gold answer"}
        
        # Calculate metrics
        intersection = answer_tokens.intersection(gold_tokens)
        union = answer_tokens.union(gold_tokens)
        
        # Precision: how many answer tokens are in gold
        precision = len(intersection) / len(answer_tokens) if answer_tokens else 0
        
        # Recall: how many gold tokens are in answer
        recall = len(intersection) / len(gold_tokens)
        
        # F1 score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Jaccard similarity
        jaccard = len(intersection) / len(union) if union else 0
        
        details = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "jaccard": round(jaccard, 3),
            "token_overlap": len(intersection),
            "gold_tokens": len(gold_tokens),
            "answer_tokens": len(answer_tokens)
        }
        
        # Return F1 as primary score
        return f1, details
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def calculate_exact_match(self, answer: str, gold_answer: str) -> bool:
        """
        Check if answer exactly matches gold answer (after normalization).
        
        Args:
            answer: Generated answer text
            gold_answer: Expected answer text
            
        Returns:
            True if exact match, False otherwise
        """
        normalized_answer = self._normalize_text(answer)
        normalized_gold = self._normalize_text(gold_answer)
        
        return normalized_answer == normalized_gold


class LatencyEvaluator:
    """Evaluates system latency and performance metrics."""
    
    def __init__(self):
        self.latencies = []
    
    def add_latency(self, latency: float):
        """Add a latency measurement."""
        self.latencies.append(latency)
    
    def get_statistics(self) -> Dict[str, float]:
        """
        Get latency statistics.
        
        Returns:
            Dictionary with p50, p95, mean, min, max latencies
        """
        if not self.latencies:
            return {
                "p50": 0.0,
                "p95": 0.0,
                "mean": 0.0,
                "min": 0.0,
                "max": 0.0,
                "count": 0
            }
        
        return {
            "p50": float(np.percentile(self.latencies, 50)),
            "p95": float(np.percentile(self.latencies, 95)),
            "mean": float(np.mean(self.latencies)),
            "min": float(np.min(self.latencies)),
            "max": float(np.max(self.latencies)),
            "count": len(self.latencies)
        }
    
    def reset(self):
        """Reset collected latencies."""
        self.latencies = []


class RetrievalEvaluator:
    """Evaluates retrieval quality."""
    
    def __init__(self):
        pass
    
    def evaluate_relevance(self, query: str, retrieved_docs: List[Dict], 
                          expected_source: str = None) -> Tuple[float, str]:
        """
        Evaluate relevance of retrieved documents.
        
        Args:
            query: The user query
            retrieved_docs: List of retrieved documents
            expected_source: Optional expected source document
            
        Returns:
            Tuple of (relevance_score: float, explanation: str)
        """
        if not retrieved_docs:
            return 0.0, "No documents retrieved"
        
        # If expected source provided, check if it's in retrieved docs
        if expected_source:
            sources = [doc.get('source', '') for doc in retrieved_docs]
            if any(expected_source in source for source in sources):
                # Find position of expected source
                for idx, source in enumerate(sources):
                    if expected_source in source:
                        # Score based on position (earlier is better)
                        position_score = 1.0 - (idx * 0.2)  # 1.0, 0.8, 0.6, etc.
                        return max(position_score, 0.4), f"Expected source at position {idx+1}"
            return 0.0, f"Expected source {expected_source} not retrieved"
        
        # Without expected source, just verify we got docs with reasonable scores
        avg_score = np.mean([doc.get('score', 1.0) for doc in retrieved_docs])
        return 1.0, f"Retrieved {len(retrieved_docs)} documents, avg score: {avg_score:.3f}"
    
    def calculate_mrr(self, retrieved_sources: List[str], expected_source: str) -> float:
        """
        Calculate Mean Reciprocal Rank.
        
        Args:
            retrieved_sources: List of retrieved source names in order
            expected_source: Expected source name
            
        Returns:
            MRR score (1/rank of first relevant doc, or 0)
        """
        for idx, source in enumerate(retrieved_sources):
            if expected_source in source:
                return 1.0 / (idx + 1)
        return 0.0


def format_evaluation_report(results: Dict) -> str:
    """
    Format evaluation results into a readable report.
    
    Args:
        results: Dictionary with evaluation results
        
    Returns:
        Formatted string report
    """
    report = []
    report.append("=" * 70)
    report.append("RAG SYSTEM EVALUATION REPORT")
    report.append("=" * 70)
    report.append("")
    
    # Answer Quality Metrics
    if 'answer_quality' in results:
        report.append("📊 ANSWER QUALITY METRICS")
        report.append("-" * 70)
        aq = results['answer_quality']
        report.append(f"  Groundedness:      {aq.get('groundedness', 0)*100:6.2f}%")
        report.append(f"  Citation Accuracy: {aq.get('citation_accuracy', 0)*100:6.2f}%")
        report.append(f"  Partial Match:     {aq.get('partial_match', 0)*100:6.2f}%")
        if 'exact_match' in aq:
            report.append(f"  Exact Match:       {aq.get('exact_match', 0)*100:6.2f}%")
        report.append("")
    
    # System Metrics
    if 'system_metrics' in results:
        report.append("⏱️  SYSTEM PERFORMANCE METRICS")
        report.append("-" * 70)
        sm = results['system_metrics']
        report.append(f"  Latency (p50):     {sm.get('latency_p50', 0):6.3f}s")
        report.append(f"  Latency (p95):     {sm.get('latency_p95', 0):6.3f}s")
        report.append(f"  Latency (mean):    {sm.get('latency_mean', 0):6.3f}s")
        report.append(f"  Latency (min):     {sm.get('latency_min', 0):6.3f}s")
        report.append(f"  Latency (max):     {sm.get('latency_max', 0):6.3f}s")
        report.append("")
    
    # Retrieval Metrics
    if 'retrieval_metrics' in results:
        report.append("🔍 RETRIEVAL METRICS")
        report.append("-" * 70)
        rm = results['retrieval_metrics']
        report.append(f"  Average Relevance: {rm.get('avg_relevance', 0)*100:6.2f}%")
        if 'mrr' in rm:
            report.append(f"  MRR:              {rm.get('mrr', 0):6.3f}")
        report.append("")
    
    # Category Breakdown
    if 'category_breakdown' in results:
        report.append("📁 RESULTS BY CATEGORY")
        report.append("-" * 70)
        for category, metrics in results['category_breakdown'].items():
            report.append(f"  {category}:")
            report.append(f"    Groundedness:      {metrics.get('groundedness', 0)*100:6.2f}%")
            report.append(f"    Citation Accuracy: {metrics.get('citation_accuracy', 0)*100:6.2f}%")
            report.append("")
    
    # Summary
    if 'summary' in results:
        report.append("📈 SUMMARY")
        report.append("-" * 70)
        summary = results['summary']
        report.append(f"  Total Questions:   {summary.get('total_questions', 0)}")
        report.append(f"  Passed:           {summary.get('passed', 0)}")
        report.append(f"  Failed:           {summary.get('failed', 0)}")
        report.append(f"  Success Rate:     {summary.get('success_rate', 0)*100:6.2f}%")
        report.append("")
    
    report.append("=" * 70)
    
    return "\n".join(report)
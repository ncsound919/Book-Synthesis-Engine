"""
Validity Comparator Module
Compares synthesized knowledge against source materials and web results for validation
"""

from typing import List, Dict
import re
from collections import defaultdict


class ValidityComparator:
    """Validates synthesized knowledge against multiple sources"""
    
    def __init__(self, config):
        """Initialize validity comparator with configuration"""
        self.config = config
        self.min_similarity = float(config.get('Synthesis', 'min_similarity_threshold', 0.7))
    
    def compare(self, synthesized_knowledge: Dict, web_results: Dict, 
                book_contents: List[Dict]) -> Dict:
        """
        Compare synthesized knowledge against sources for validation
        
        Args:
            synthesized_knowledge: Synthesized knowledge to validate
            web_results: Web search results
            book_contents: Original book contents
            
        Returns:
            Dictionary containing validity report
        """
        print("  Analyzing validity of synthesized knowledge...")
        
        report = {
            'overall_confidence': 0.0,
            'sources_validated': 0,
            'findings': [],
            'concept_validation': {},
            'cross_reference_score': 0.0
        }
        
        # Extract key concepts from synthesis
        key_concepts = synthesized_knowledge.get('key_concepts', [])
        synthesis_text = synthesized_knowledge.get('text', '')
        
        # Validate against book sources
        book_validation = self._validate_against_books(
            synthesis_text, key_concepts, book_contents
        )
        
        # Validate against web results
        web_validation = self._validate_against_web(
            key_concepts, web_results
        )
        
        # Calculate cross-reference score
        cross_ref_score = self._calculate_cross_reference_score(
            book_contents, key_concepts
        )
        
        # Compile findings
        report['findings'].extend(book_validation['findings'])
        report['findings'].extend(web_validation['findings'])
        
        # Calculate overall confidence
        book_confidence = book_validation['confidence']
        web_confidence = web_validation['confidence']
        
        # Weighted average (books are more reliable than web)
        report['overall_confidence'] = (book_confidence * 0.7 + web_confidence * 0.3)
        report['sources_validated'] = len(book_contents) + len(web_results.get('search_results', []))
        report['cross_reference_score'] = cross_ref_score
        
        report['concept_validation'] = {
            'book_supported_concepts': book_validation['supported_concepts'],
            'web_supported_concepts': web_validation['supported_concepts'],
            'total_concepts_checked': len(key_concepts)
        }
        
        # Add summary finding
        if report['overall_confidence'] >= 0.8:
            report['findings'].insert(0, 
                "HIGH CONFIDENCE: Synthesized knowledge is well-supported by multiple sources.")
        elif report['overall_confidence'] >= 0.6:
            report['findings'].insert(0, 
                "MODERATE CONFIDENCE: Synthesized knowledge has reasonable support from sources.")
        else:
            report['findings'].insert(0, 
                "LOW CONFIDENCE: Synthesized knowledge may need additional verification.")
        
        return report
    
    def _validate_against_books(self, synthesis_text: str, key_concepts: List[str],
                                book_contents: List[Dict]) -> Dict:
        """Validate synthesis against original book contents"""
        supported_concepts = []
        findings = []
        
        # Check how many concepts appear in source books
        for concept in key_concepts[:20]:  # Check top 20
            concept_lower = concept.lower()
            found_in_books = []
            
            for book in book_contents:
                if concept_lower in book['content'].lower():
                    found_in_books.append(book['filename'])
            
            if found_in_books:
                supported_concepts.append(concept)
                if len(found_in_books) > 1:
                    findings.append(
                        f"Concept '{concept}' validated across {len(found_in_books)} source books"
                    )
        
        # Calculate confidence based on concept support
        if key_concepts:
            confidence = len(supported_concepts) / len(key_concepts[:20])
        else:
            confidence = 0.5  # Neutral if no concepts
        
        findings.append(
            f"Book validation: {len(supported_concepts)}/{len(key_concepts[:20])} "
            f"key concepts found in source materials"
        )
        
        return {
            'confidence': confidence,
            'supported_concepts': len(supported_concepts),
            'findings': findings
        }
    
    def _validate_against_web(self, key_concepts: List[str], 
                             web_results: Dict) -> Dict:
        """Validate concepts against web search results"""
        supported_concepts = []
        findings = []
        
        search_results = web_results.get('search_results', [])
        
        if not search_results:
            findings.append("Web validation: No web results available for comparison")
            return {
                'confidence': 0.5,
                'supported_concepts': 0,
                'findings': findings
            }
        
        # Check which concepts have web search results
        searched_topics = [r['topic'] for r in search_results]
        
        for concept in key_concepts[:20]:
            if concept in searched_topics:
                supported_concepts.append(concept)
        
        # Calculate confidence
        if key_concepts:
            confidence = min(1.0, len(supported_concepts) / len(key_concepts[:20]) * 1.2)
        else:
            confidence = 0.5
        
        findings.append(
            f"Web validation: {len(supported_concepts)}/{len(key_concepts[:20])} "
            f"concepts have web search results"
        )
        
        if web_results.get('summary', {}).get('total_results_found', 0) > 0:
            findings.append(
                f"Found {web_results['summary']['total_results_found']} "
                f"web references across searched topics"
            )
        
        return {
            'confidence': confidence,
            'supported_concepts': len(supported_concepts),
            'findings': findings
        }
    
    def _calculate_cross_reference_score(self, book_contents: List[Dict], 
                                        key_concepts: List[str]) -> float:
        """
        Calculate how well concepts cross-reference across books
        
        Args:
            book_contents: Original book contents
            key_concepts: Key concepts to check
            
        Returns:
            Cross-reference score (0.0 to 1.0)
        """
        if len(book_contents) < 2:
            return 1.0  # Single source, assume valid
        
        cross_references = 0
        total_checks = 0
        
        # Check top concepts across books
        for concept in key_concepts[:15]:
            concept_lower = concept.lower()
            books_with_concept = 0
            
            for book in book_contents:
                if concept_lower in book['content'].lower():
                    books_with_concept += 1
            
            total_checks += 1
            # If concept appears in multiple books, it's cross-referenced
            if books_with_concept > 1:
                cross_references += 1
        
        if total_checks == 0:
            return 0.5
        
        return cross_references / total_checks

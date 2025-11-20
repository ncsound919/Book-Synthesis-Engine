"""
Knowledge Synthesizer Module
Synthesizes information from multiple book sources
"""

from typing import List, Dict
import re
from collections import Counter


class KnowledgeSynthesizer:
    """Synthesizes knowledge from multiple book sources"""
    
    def __init__(self, config):
        """Initialize knowledge synthesizer with configuration"""
        self.config = config
        self.max_length = int(config.get('Synthesis', 'max_synthesis_length', 5000))
    
    def synthesize(self, book_contents: List[Dict]) -> Dict:
        """
        Synthesize knowledge from multiple books
        
        Args:
            book_contents: List of dictionaries containing book content
            
        Returns:
            Dictionary containing synthesized knowledge
        """
        # Extract key concepts and themes from all books
        all_concepts = []
        all_sentences = []
        
        for book in book_contents:
            content = book['content']
            # Extract sentences
            sentences = self._extract_sentences(content)
            all_sentences.extend([(sent, book['filename']) for sent in sentences])
            
            # Extract key concepts
            concepts = self._extract_concepts(content)
            all_concepts.extend(concepts)
        
        # Find common themes
        common_concepts = self._find_common_themes(all_concepts)
        
        # Generate synthesis
        synthesized_text = self._generate_synthesis(all_sentences, common_concepts, book_contents)
        
        return {
            'text': synthesized_text,
            'key_concepts': common_concepts[:20],  # Top 20 concepts
            'sources': [book['filename'] for book in book_contents],
            'total_sources': len(book_contents)
        }
    
    def extract_key_topics(self, synthesized_knowledge: Dict) -> List[str]:
        """
        Extract key topics from synthesized knowledge for web scanning
        
        Args:
            synthesized_knowledge: Dictionary containing synthesized knowledge
            
        Returns:
            List of key topics to search
        """
        # Get top concepts
        concepts = synthesized_knowledge.get('key_concepts', [])
        
        # Extract noun phrases from text
        text = synthesized_knowledge.get('text', '')
        noun_phrases = self._extract_noun_phrases(text)
        
        # Combine and deduplicate
        topics = list(set(concepts[:10] + noun_phrases[:10]))
        
        return topics[:10]  # Return top 10 topics
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        # Clean and filter
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Remove common words and extract potential concepts
        # This is a simplified version - in production, use NLP libraries
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Also extract capitalized words and common nouns
        words.extend(re.findall(r'\b[a-z]{4,}\b', text.lower()))
        
        return words
    
    def _find_common_themes(self, concepts: List[str]) -> List[str]:
        """Find most common themes across all concepts"""
        # Count concept frequency
        concept_counter = Counter(concepts)
        
        # Filter out very rare concepts (appear in < 2 sources)
        common_concepts = [concept for concept, count in concept_counter.most_common(100) 
                          if count >= 2]
        
        return common_concepts
    
    def _extract_noun_phrases(self, text: str) -> List[str]:
        """Extract noun phrases from text"""
        # Simple extraction of multi-word capitalized phrases
        phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b', text)
        # Count and return most common
        phrase_counter = Counter(phrases)
        return [phrase for phrase, _ in phrase_counter.most_common(20)]
    
    def _generate_synthesis(self, all_sentences: List[tuple], common_concepts: List[str], 
                           book_contents: List[Dict]) -> str:
        """
        Generate synthesized text from sentences and concepts
        
        Args:
            all_sentences: List of (sentence, source) tuples
            common_concepts: List of common concepts
            book_contents: Original book contents
            
        Returns:
            Synthesized text
        """
        synthesis_parts = []
        
        # Introduction
        synthesis_parts.append(
            f"SYNTHESIZED KNOWLEDGE FROM {len(book_contents)} SOURCES\n\n"
        )
        
        # Overview of common themes
        synthesis_parts.append("KEY THEMES:\n")
        synthesis_parts.append(
            "The following analysis synthesizes information from multiple sources, "
            "identifying common themes and complementary insights.\n\n"
        )
        
        # Main concepts
        if common_concepts:
            synthesis_parts.append("CENTRAL CONCEPTS:\n")
            for i, concept in enumerate(common_concepts[:10], 1):
                # Find relevant sentences for this concept
                relevant_sentences = [
                    sent for sent, _ in all_sentences 
                    if concept.lower() in sent.lower()
                ][:3]
                
                if relevant_sentences:
                    synthesis_parts.append(f"\n{i}. {concept.upper()}\n")
                    for sent in relevant_sentences:
                        synthesis_parts.append(f"   - {sent}\n")
        
        # Cross-source insights
        synthesis_parts.append("\n\nCROSS-SOURCE INSIGHTS:\n")
        synthesis_parts.append(
            "By analyzing multiple sources together, we can identify "
            "patterns, agreements, and unique perspectives that emerge "
            "when different authors address similar topics.\n\n"
        )
        
        # Select representative sentences from each source
        for book in book_contents:
            sentences = self._extract_sentences(book['content'])
            if sentences:
                synthesis_parts.append(f"From '{book['filename']}':\n")
                # Get diverse sentences
                step = max(1, len(sentences) // 3)
                for sent in sentences[::step][:3]:
                    synthesis_parts.append(f"  • {sent}\n")
                synthesis_parts.append("\n")
        
        # Combine all parts
        full_synthesis = ''.join(synthesis_parts)
        
        # Truncate if too long
        if len(full_synthesis) > self.max_length:
            full_synthesis = full_synthesis[:self.max_length] + "...\n\n[Synthesis truncated to maximum length]"
        
        return full_synthesis

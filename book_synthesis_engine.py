#!/usr/bin/env python3
"""
Book Synthesis Engine - Main Application
Synthesizes knowledge from multiple books with webscan, validity comparison, and illustration generation
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import json

from modules.document_processor import DocumentProcessor
from modules.knowledge_synthesizer import KnowledgeSynthesizer
from modules.webscan import WebScanner
from modules.validity_comparator import ValidityComparator
from modules.illustration_generator import IllustrationGenerator
from modules.config_manager import ConfigManager


class BookSynthesisEngine:
    """Main class for the Book Synthesis Engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Book Synthesis Engine"""
        self.config = ConfigManager(config_path)
        self.doc_processor = DocumentProcessor(self.config)
        self.synthesizer = KnowledgeSynthesizer(self.config)
        self.web_scanner = WebScanner(self.config)
        self.validity_comparator = ValidityComparator(self.config)
        self.illustration_generator = IllustrationGenerator(self.config)
        
        # Create necessary directories
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in [
            self.config.get('Paths', 'upload_dir', 'uploads'),
            self.config.get('Paths', 'output_dir', 'outputs'),
            self.config.get('Paths', 'illustration_dir', 'illustrations'),
            self.config.get('Paths', 'model_cache_dir', 'models')
        ]:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def process_books(self, book_paths: List[str]) -> Dict:
        """
        Process multiple books and synthesize knowledge
        
        Args:
            book_paths: List of paths to book files
            
        Returns:
            Dictionary containing synthesized knowledge and metadata
        """
        max_books = int(self.config.get('Synthesis', 'max_books', 5))
        if len(book_paths) > max_books:
            raise ValueError(f"Maximum {max_books} books allowed, got {len(book_paths)}")
        
        print(f"\n{'='*60}")
        print(f"Book Synthesis Engine - Processing {len(book_paths)} books")
        print(f"{'='*60}\n")
        
        # Step 1: Extract text from all books
        print("[1/6] Extracting text from books...")
        book_contents = []
        for i, book_path in enumerate(book_paths, 1):
            print(f"  Processing book {i}/{len(book_paths)}: {Path(book_path).name}")
            content = self.doc_processor.extract_text(book_path)
            book_contents.append({
                'filename': Path(book_path).name,
                'content': content,
                'path': book_path
            })
        
        # Step 2: Synthesize knowledge from books
        print("\n[2/6] Synthesizing knowledge from books...")
        synthesized_knowledge = self.synthesizer.synthesize(book_contents)
        
        # Step 3: Web scan for additional context and validation
        print("\n[3/6] Performing web scan for additional context...")
        key_topics = self.synthesizer.extract_key_topics(synthesized_knowledge)
        web_results = self.web_scanner.scan_topics(key_topics)
        
        # Step 4: Validate synthesized knowledge against web sources
        print("\n[4/6] Validating synthesized knowledge...")
        validity_report = self.validity_comparator.compare(
            synthesized_knowledge, 
            web_results,
            book_contents
        )
        
        # Step 5: Generate illustrations for key concepts
        print("\n[5/6] Generating illustrations for key concepts...")
        illustrations = self.illustration_generator.generate_illustrations(
            synthesized_knowledge,
            validity_report
        )
        
        # Step 6: Compile final output
        print("\n[6/6] Compiling final synthesis report...")
        result = {
            'synthesized_knowledge': synthesized_knowledge,
            'source_books': [book['filename'] for book in book_contents],
            'web_scan_results': web_results,
            'validity_report': validity_report,
            'illustrations': illustrations,
            'metadata': {
                'num_books_processed': len(book_paths),
                'total_source_words': sum(len(book['content'].split()) for book in book_contents),
                'synthesis_confidence': validity_report.get('overall_confidence', 0.0)
            }
        }
        
        return result
    
    def save_results(self, results: Dict, output_name: str = "synthesis_output"):
        """Save synthesis results to files"""
        output_dir = Path(self.config.get('Paths', 'output_dir', 'outputs'))
        
        # Save JSON report
        json_path = output_dir / f"{output_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save human-readable text report
        text_path = output_dir / f"{output_name}.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write("BOOK SYNTHESIS ENGINE - REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("SOURCE BOOKS:\n")
            for i, book in enumerate(results['source_books'], 1):
                f.write(f"  {i}. {book}\n")
            
            f.write(f"\n\nSYNTHESIZED KNOWLEDGE:\n")
            f.write("-" * 60 + "\n")
            f.write(results['synthesized_knowledge'].get('text', ''))
            
            f.write("\n\n\nVALIDITY REPORT:\n")
            f.write("-" * 60 + "\n")
            validity = results['validity_report']
            f.write(f"Overall Confidence: {validity.get('overall_confidence', 0.0):.2%}\n")
            f.write(f"Sources Validated: {validity.get('sources_validated', 0)}\n")
            f.write(f"\nFindings:\n")
            for finding in validity.get('findings', []):
                f.write(f"  - {finding}\n")
            
            f.write("\n\n\nILLUSTRATIONS GENERATED:\n")
            f.write("-" * 60 + "\n")
            for ill in results['illustrations']:
                f.write(f"  - {ill['description']}\n")
                f.write(f"    File: {ill['path']}\n")
        
        print(f"\n{'='*60}")
        print(f"Results saved:")
        print(f"  JSON Report: {json_path}")
        print(f"  Text Report: {text_path}")
        print(f"{'='*60}\n")
        
        return json_path, text_path


def main():
    """Main entry point for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Book Synthesis Engine - Synthesize knowledge from multiple books"
    )
    parser.add_argument(
        'books',
        nargs='+',
        help='Paths to book files (PDF, EPUB, DOCX, TXT)'
    )
    parser.add_argument(
        '-c', '--config',
        help='Path to config file',
        default='config.ini'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output name prefix',
        default='synthesis_output'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize engine
        engine = BookSynthesisEngine(args.config)
        
        # Process books
        results = engine.process_books(args.books)
        
        # Save results
        engine.save_results(results, args.output)
        
        print("\n✓ Synthesis completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

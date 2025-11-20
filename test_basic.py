#!/usr/bin/env python3
"""
Basic test script for Book Synthesis Engine
Tests core functionality without requiring external dependencies
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    try:
        from modules.config_manager import ConfigManager
        from modules.document_processor import DocumentProcessor
        from modules.knowledge_synthesizer import KnowledgeSynthesizer
        from modules.webscan import WebScanner
        from modules.validity_comparator import ValidityComparator
        from modules.illustration_generator import IllustrationGenerator
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration manager"""
    print("\nTesting configuration manager...")
    try:
        from modules.config_manager import ConfigManager
        config = ConfigManager()
        
        # Test getting default values
        upload_dir = config.get('Paths', 'upload_dir')
        max_books = config.get('Synthesis', 'max_books')
        
        assert upload_dir is not None
        assert max_books is not None
        
        print(f"✓ Configuration manager working (upload_dir: {upload_dir}, max_books: {max_books})")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_document_processor():
    """Test document processor with sample files"""
    print("\nTesting document processor...")
    try:
        from modules.config_manager import ConfigManager
        from modules.document_processor import DocumentProcessor
        
        config = ConfigManager()
        processor = DocumentProcessor(config)
        
        # Test with sample text file
        sample_file = Path("examples/sample_book1.txt")
        if sample_file.exists():
            content = processor.extract_text(str(sample_file))
            assert len(content) > 0
            print(f"✓ Document processor working (extracted {len(content)} characters)")
            return True
        else:
            print("⚠ Sample file not found, skipping test")
            return True
    except Exception as e:
        print(f"✗ Document processor test failed: {e}")
        return False

def test_knowledge_synthesizer():
    """Test knowledge synthesizer"""
    print("\nTesting knowledge synthesizer...")
    try:
        from modules.config_manager import ConfigManager
        from modules.knowledge_synthesizer import KnowledgeSynthesizer
        
        config = ConfigManager()
        synthesizer = KnowledgeSynthesizer(config)
        
        # Test with dummy content
        book_contents = [
            {'filename': 'book1.txt', 'content': 'Artificial Intelligence and Machine Learning are important.'},
            {'filename': 'book2.txt', 'content': 'Machine Learning uses Neural Networks for deep learning.'}
        ]
        
        result = synthesizer.synthesize(book_contents)
        
        assert 'text' in result
        assert 'key_concepts' in result
        assert len(result['key_concepts']) > 0
        
        print(f"✓ Knowledge synthesizer working (found {len(result['key_concepts'])} concepts)")
        return True
    except Exception as e:
        print(f"✗ Knowledge synthesizer test failed: {e}")
        return False

def test_webscan():
    """Test web scanner"""
    print("\nTesting web scanner...")
    try:
        from modules.config_manager import ConfigManager
        from modules.webscan import WebScanner
        
        config = ConfigManager()
        scanner = WebScanner(config)
        
        # Test with simple topics
        topics = ['Machine Learning', 'Artificial Intelligence']
        results = scanner.scan_topics(topics)
        
        assert 'topics_searched' in results
        assert 'search_results' in results
        assert len(results['search_results']) > 0
        
        print(f"✓ Web scanner working (scanned {len(topics)} topics)")
        return True
    except Exception as e:
        print(f"✗ Web scanner test failed: {e}")
        return False

def test_validity_comparator():
    """Test validity comparator"""
    print("\nTesting validity comparator...")
    try:
        from modules.config_manager import ConfigManager
        from modules.validity_comparator import ValidityComparator
        
        config = ConfigManager()
        comparator = ValidityComparator(config)
        
        # Test with dummy data
        synthesized = {
            'text': 'Test synthesis about Machine Learning',
            'key_concepts': ['Machine Learning', 'AI']
        }
        web_results = {
            'search_results': [
                {'topic': 'Machine Learning', 'results': []}
            ]
        }
        book_contents = [
            {'filename': 'book1.txt', 'content': 'Machine Learning is important'}
        ]
        
        result = comparator.compare(synthesized, web_results, book_contents)
        
        assert 'overall_confidence' in result
        assert 'findings' in result
        
        print(f"✓ Validity comparator working (confidence: {result['overall_confidence']:.2f})")
        return True
    except Exception as e:
        print(f"✗ Validity comparator test failed: {e}")
        return False

def test_illustration_generator():
    """Test illustration generator (basic setup only)"""
    print("\nTesting illustration generator...")
    try:
        from modules.config_manager import ConfigManager
        from modules.illustration_generator import IllustrationGenerator
        
        config = ConfigManager()
        generator = IllustrationGenerator(config)
        
        # Just test initialization
        assert generator is not None
        assert generator.output_dir is not None
        
        print(f"✓ Illustration generator initialized")
        return True
    except Exception as e:
        print(f"✗ Illustration generator test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Book Synthesis Engine - Basic Tests")
    print("="*60)
    
    tests = [
        test_imports,
        test_config,
        test_document_processor,
        test_knowledge_synthesizer,
        test_webscan,
        test_validity_comparator,
        test_illustration_generator
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} tests passed")
    print("="*60)
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())

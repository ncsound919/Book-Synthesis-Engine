# Book Synthesis Engine - Usage Guide

Complete guide for using the Book Synthesis Engine to synthesize knowledge from multiple book sources.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Usage](#advanced-usage)
5. [Understanding Output](#understanding-output)
6. [Configuration](#configuration)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Quick Start

### 5-Minute Tutorial

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run with sample books:**
```bash
python book_synthesis_engine.py examples/sample_book1.txt examples/sample_book2.txt examples/sample_book3.txt
```

3. **Check results:**
```bash
cat outputs/synthesis_output.txt
ls illustrations/
```

That's it! You've just synthesized knowledge from multiple books.

## Installation

### System Requirements
- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended for Stable Diffusion)
- Internet connection (optional, for web scanning)

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ncsound919/Book-Synthesis-Engine.git
cd Book-Synthesis-Engine
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

**Option A: Full installation (with Stable Diffusion)**
```bash
pip install -r requirements.txt
```

**Option B: Minimal installation (faster, uses placeholder illustrations)**
```bash
pip install PyPDF2 python-docx ebooklib beautifulsoup4 lxml requests Pillow
```

4. **Verify installation:**
```bash
python test_basic.py
```

## Basic Usage

### Command Line Interface

The basic syntax is:
```bash
python book_synthesis_engine.py [OPTIONS] book1 book2 [book3...]
```

### Simple Examples

**Synthesize from PDF files:**
```bash
python book_synthesis_engine.py books/book1.pdf books/book2.pdf
```

**Mix different formats:**
```bash
python book_synthesis_engine.py book1.pdf book2.epub book3.docx book4.txt
```

**Custom output name:**
```bash
python book_synthesis_engine.py book1.pdf book2.pdf -o my_synthesis
```

**Use custom config:**
```bash
python book_synthesis_engine.py book1.pdf book2.pdf -c my_config.ini
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-o`, `--output` | Output filename prefix | `-o my_report` |
| `-c`, `--config` | Path to config file | `-c config.ini` |
| `-h`, `--help` | Show help message | `-h` |

## Advanced Usage

### Using as a Python Library

```python
from book_synthesis_engine import BookSynthesisEngine

# Initialize engine
engine = BookSynthesisEngine('config.ini')

# Process books
results = engine.process_books([
    'path/to/book1.pdf',
    'path/to/book2.epub',
    'path/to/book3.docx'
])

# Access results
print(f"Confidence: {results['metadata']['synthesis_confidence']:.2%}")
print(f"Key concepts: {results['synthesized_knowledge']['key_concepts'][:5]}")

# Save results
engine.save_results(results, 'my_synthesis')
```

### Processing Specific Components

#### Just Extract Text
```python
from modules.document_processor import DocumentProcessor
from modules.config_manager import ConfigManager

config = ConfigManager()
processor = DocumentProcessor(config)
text = processor.extract_text('mybook.pdf')
print(text)
```

#### Just Synthesize (no web scan)
```python
from modules.knowledge_synthesizer import KnowledgeSynthesizer
from modules.config_manager import ConfigManager

config = ConfigManager()
synthesizer = KnowledgeSynthesizer(config)

book_contents = [
    {'filename': 'book1.txt', 'content': 'text content here...'},
    {'filename': 'book2.txt', 'content': 'more text content...'}
]

result = synthesizer.synthesize(book_contents)
print(result['text'])
```

#### Just Web Scan
```python
from modules.webscan import WebScanner
from modules.config_manager import ConfigManager

config = ConfigManager()
scanner = WebScanner(config)

topics = ['Machine Learning', 'Neural Networks']
results = scanner.scan_topics(topics)
print(results['summary'])
```

## Understanding Output

### Output Structure

After processing, you'll find:

```
Book-Synthesis-Engine/
├── outputs/
│   ├── synthesis_output.json    # Machine-readable full report
│   └── synthesis_output.txt     # Human-readable summary
└── illustrations/
    ├── illustration_01_concept1.png
    ├── illustration_02_concept2.png
    └── ...
```

### JSON Output Format

```json
{
  "synthesized_knowledge": {
    "text": "Full synthesis text...",
    "key_concepts": ["concept1", "concept2", ...],
    "sources": ["book1.pdf", "book2.epub"],
    "total_sources": 2
  },
  "web_scan_results": {
    "topics_searched": [...],
    "search_results": [...],
    "summary": {...}
  },
  "validity_report": {
    "overall_confidence": 0.85,
    "sources_validated": 10,
    "findings": [...],
    "concept_validation": {...}
  },
  "illustrations": [...],
  "metadata": {...}
}
```

### Text Output Format

The text report includes:
1. **Source Books**: List of input files
2. **Synthesized Knowledge**: Main synthesis text with key concepts
3. **Validity Report**: Confidence score and validation findings
4. **Illustrations Generated**: List of created illustration files

### Interpreting Confidence Scores

| Score | Meaning | Action |
|-------|---------|--------|
| 80-100% | HIGH CONFIDENCE | Synthesis well-supported, reliable |
| 60-79% | MODERATE CONFIDENCE | Generally reliable, some verification recommended |
| 0-59% | LOW CONFIDENCE | Needs additional verification |

## Configuration

### Creating a Config File

1. **Copy the example:**
```bash
cp config.example.ini config.ini
```

2. **Edit settings:**
```ini
[Synthesis]
max_books = 5                    # Maximum number of books
max_synthesis_length = 5000      # Maximum synthesis text length

[WebScan]
max_search_results = 10          # Results per topic
timeout_seconds = 30             # Request timeout

[StableDiffusion]
model_name = runwayml/stable-diffusion-v1-5
num_inference_steps = 50         # Quality vs speed tradeoff
image_size = 512                 # Output image dimensions
```

### Environment Variables

For API keys (optional):
```bash
export HUGGINGFACE_TOKEN=your_token_here
export OPENAI_API_KEY=your_key_here
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your values
```

## Examples

### Example 1: Academic Research

Synthesize multiple research papers:
```bash
python book_synthesis_engine.py \
    papers/paper1.pdf \
    papers/paper2.pdf \
    papers/paper3.pdf \
    -o research_synthesis
```

### Example 2: Book Series Analysis

Analyze a book series:
```bash
python book_synthesis_engine.py \
    series/book1.epub \
    series/book2.epub \
    series/book3.epub \
    -o series_analysis
```

### Example 3: Technical Documentation

Combine multiple technical manuals:
```bash
python book_synthesis_engine.py \
    docs/manual1.pdf \
    docs/guide.docx \
    docs/tutorial.txt \
    -o technical_synthesis
```

### Example 4: Batch Processing

Process multiple sets of books:
```bash
#!/bin/bash
for topic in ai ml nlp; do
    python book_synthesis_engine.py \
        books/${topic}/*.pdf \
        -o ${topic}_synthesis
done
```

### Example 5: Programmatic Processing

```python
import glob
from book_synthesis_engine import BookSynthesisEngine

engine = BookSynthesisEngine()

# Process all PDFs in a directory
pdf_files = glob.glob('books/*.pdf')[:5]  # Max 5 books

if pdf_files:
    results = engine.process_books(pdf_files)
    engine.save_results(results, 'auto_synthesis')
    
    # Print summary
    print(f"Processed {len(pdf_files)} books")
    print(f"Confidence: {results['metadata']['synthesis_confidence']:.2%}")
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError"
**Cause**: Missing dependencies  
**Solution**:
```bash
pip install -r requirements.txt
```

#### Issue: "FileNotFoundError: File not found"
**Cause**: Incorrect file path  
**Solution**: Use absolute paths or verify relative paths:
```bash
python book_synthesis_engine.py /full/path/to/book.pdf
```

#### Issue: "ValueError: Unsupported file format"
**Cause**: File format not supported  
**Solution**: Convert to PDF, EPUB, DOCX, or TXT format

#### Issue: "Out of memory"
**Cause**: Stable Diffusion requires too much RAM  
**Solution**: The system automatically falls back to placeholder mode. Or:
```bash
# Use minimal installation
pip install PyPDF2 python-docx ebooklib beautifulsoup4 lxml requests Pillow
```

#### Issue: Web scanning fails
**Cause**: No internet connection or blocked domains  
**Solution**: The system automatically uses offline validation. No action needed.

#### Issue: "Maximum 5 books allowed"
**Cause**: Too many input files  
**Solution**: Process in batches or modify `max_books` in config.ini

#### Issue: PDF extraction returns gibberish
**Cause**: PDF contains scanned images, not text  
**Solution**: Use OCR software to convert to text first, or use a different PDF version

### Performance Issues

**Slow processing:**
- Reduce `max_synthesis_length` in config.ini
- Reduce `num_inference_steps` for Stable Diffusion
- Use placeholder mode instead of Stable Diffusion
- Process fewer books at once

**High memory usage:**
- Close other applications
- Use minimal installation
- Reduce `image_size` in config.ini
- Process books sequentially rather than in batch

### Getting Help

If you encounter issues:

1. **Check the logs**: Look for error messages in console output
2. **Run tests**: `python test_basic.py` to verify installation
3. **Check examples**: Try sample books to isolate the issue
4. **Review documentation**: Check FEATURES.md for detailed info
5. **Open an issue**: Report bugs on GitHub with error details

## Best Practices

### For Best Results

1. **Use related books**: Books on similar topics produce better synthesis
2. **Check source quality**: Higher quality inputs = better outputs
3. **Review validity scores**: Pay attention to confidence metrics
4. **Verify web results**: Cross-check synthesized information when needed
5. **Use appropriate formats**: Text-based PDFs work better than scanned images

### Performance Optimization

1. **Start small**: Test with 2-3 books before scaling up
2. **Use config wisely**: Adjust settings based on your needs
3. **Monitor resources**: Watch memory usage for large documents
4. **Batch processing**: Process multiple sets separately rather than all at once

### Security

1. **Trusted sources**: Only process books from trusted sources
2. **Update regularly**: Keep dependencies updated for security patches
3. **Review output**: Always verify synthesized information before use
4. **Secure API keys**: Use environment variables, not hardcoded keys

## Next Steps

Once you're comfortable with basic usage:

1. **Customize config**: Tune settings for your specific needs
2. **Integrate into workflows**: Use as library in your Python projects
3. **Automate processing**: Create scripts for batch processing
4. **Explore features**: Try web scanning, validity comparison, illustrations
5. **Contribute**: Share improvements or report issues on GitHub

## Additional Resources

- **FEATURES.md**: Detailed feature documentation
- **README.md**: Project overview and installation
- **examples/**: Sample books and scripts
- **test_basic.py**: Test script to verify installation

## Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example files

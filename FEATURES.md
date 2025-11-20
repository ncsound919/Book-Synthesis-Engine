# Book Synthesis Engine - Feature Documentation

This document provides detailed information about each feature of the Book Synthesis Engine.

## 1. Multi-Format Book Processing

### Supported Formats
- **PDF** - Uses PyPDF2 to extract text from PDF documents
- **EPUB** - Uses ebooklib to parse EPUB format ebooks
- **DOCX** - Uses python-docx to extract text from Microsoft Word documents
- **TXT** - Direct text file reading with UTF-8 and Latin-1 encoding support

### How It Works
The `DocumentProcessor` module handles all document format conversions:
1. Detects file format by extension
2. Uses appropriate library to extract text content
3. Returns clean text for further processing
4. Handles encoding issues gracefully with fallback encodings

### Usage Example
```python
from modules.document_processor import DocumentProcessor
from modules.config_manager import ConfigManager

config = ConfigManager()
processor = DocumentProcessor(config)
text = processor.extract_text('mybook.pdf')
```

## 2. Knowledge Synthesis

### What It Does
The `KnowledgeSynthesizer` combines information from multiple books to create new synthesized knowledge:

- **Concept Extraction**: Identifies key concepts from all sources
- **Theme Analysis**: Finds common themes across multiple books
- **Cross-Reference**: Links related information from different sources
- **Summary Generation**: Creates coherent synthesis text

### Synthesis Process
1. **Extract Sentences**: Breaks down each book into individual sentences
2. **Identify Concepts**: Extracts important terms and concepts
3. **Find Common Themes**: Counts and ranks concepts by frequency
4. **Generate Synthesis**: Creates structured output with:
   - Overview of key themes
   - Central concepts with supporting quotes
   - Cross-source insights
   - Representative samples from each book

### Configuration
Customize synthesis behavior in `config.ini`:
```ini
[Synthesis]
max_books = 5
min_similarity_threshold = 0.7
max_synthesis_length = 5000
```

## 3. Web Scanning

### Purpose
The `WebScanner` module searches the web for additional context and validation of synthesized concepts.

### Features
- **Automatic Topic Search**: Extracts key topics and searches for them online
- **Multiple Search Results**: Gathers information from web sources
- **Fallback Mode**: Works offline when internet is unavailable
- **Rate Limiting**: Includes delays to avoid overwhelming servers

### Search Strategy
1. Extracts top 10 key concepts from synthesized knowledge
2. Performs web search for each concept
3. Collects and organizes search results
4. Provides summary statistics

### Configuration
```ini
[WebScan]
max_search_results = 10
timeout_seconds = 30
user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

### Fallback Behavior
If web search fails (no internet, blocked domain, etc.):
- Creates fallback validation results
- Continues with offline validation
- Marks results as "offline mode"

## 4. Validity Comparison

### Purpose
The `ValidityComparator` validates synthesized knowledge against multiple sources to ensure accuracy and reliability.

### Validation Methods

#### Book Source Validation
- Checks if key concepts appear in original source materials
- Counts how many books support each concept
- Calculates confidence based on cross-referencing

#### Web Results Validation
- Compares concepts against web search results
- Verifies external sources confirm synthesized information
- Provides additional confidence metrics

#### Cross-Reference Scoring
- Measures how well concepts appear across multiple books
- Higher scores indicate concepts validated by multiple independent sources
- Single-source information receives lower confidence

### Confidence Scoring
The system calculates an overall confidence score (0-100%):
- **80-100%**: HIGH CONFIDENCE - Well-supported by multiple sources
- **60-79%**: MODERATE CONFIDENCE - Reasonable support
- **0-59%**: LOW CONFIDENCE - Needs additional verification

Formula: `(Book Confidence × 0.7) + (Web Confidence × 0.3)`

### Output
The validity report includes:
- Overall confidence percentage
- Number of sources validated
- Detailed findings for each concept
- Concept validation statistics
- Cross-reference score

## 5. Stable Diffusion Illustration Generation

### Purpose
The `IllustrationGenerator` creates visual representations of key concepts using AI-powered image generation.

### How It Works

#### With Stable Diffusion (GPU Available)
1. Loads the Stable Diffusion model (runwayml/stable-diffusion-v1-5)
2. Creates descriptive prompts for each concept
3. Generates high-quality illustrations
4. Saves as PNG images in the illustrations directory

#### Placeholder Mode (No GPU/Model)
- Creates simple colored placeholder images
- Includes concept name in filename
- Works without heavy dependencies
- Useful for testing and low-resource environments

### Configuration
```ini
[StableDiffusion]
model_name = runwayml/stable-diffusion-v1-5
guidance_scale = 7.5
num_inference_steps = 50
image_size = 512
```

### Requirements
- **For Full Functionality**: CUDA-capable GPU with 6GB+ VRAM
- **For Placeholder Mode**: Just Pillow/PIL library
- **Automatic Fallback**: System detects capabilities and adjusts

### Generated Files
- Images saved as: `illustration_XX_concept_name.png`
- Organized in the `illustrations/` directory
- Referenced in final synthesis report

## 6. Comprehensive Reporting

### Output Files

#### JSON Report (`synthesis_output.json`)
Complete machine-readable report containing:
- Full synthesized knowledge
- Source book information
- Web scan results
- Validity report with all metrics
- Illustration metadata
- Processing statistics

#### Text Report (`synthesis_output.txt`)
Human-readable formatted report with:
- Source book list
- Synthesized knowledge text
- Validity findings and confidence score
- List of generated illustrations

### Report Structure
```
outputs/
├── synthesis_output.json    # Machine-readable
└── synthesis_output.txt     # Human-readable

illustrations/
├── illustration_01_concept1.png
├── illustration_02_concept2.png
└── ...
```

## Integration Example

Here's how all features work together in the main workflow:

```python
# 1. Initialize engine
engine = BookSynthesisEngine('config.ini')

# 2. Process books (Document Processing)
results = engine.process_books([
    'book1.pdf',
    'book2.epub',
    'book3.docx'
])

# Internal workflow:
# - Extract text from all books (Document Processor)
# - Synthesize knowledge (Knowledge Synthesizer)
# - Scan web for topics (Web Scanner)
# - Validate synthesis (Validity Comparator)
# - Generate illustrations (Illustration Generator)

# 3. Save comprehensive report
engine.save_results(results, 'my_synthesis')
```

## Performance Considerations

### Memory Usage
- **Basic Processing**: ~500MB (document processing, synthesis)
- **With Web Scan**: +100MB (web results caching)
- **With Stable Diffusion**: +4-8GB (model loading)

### Processing Time
- **Document Processing**: ~1-2 seconds per book
- **Knowledge Synthesis**: ~5-10 seconds for 5 books
- **Web Scanning**: ~1 second per topic (10 topics total)
- **Validity Comparison**: ~2-5 seconds
- **Illustration Generation**:
  - Placeholder mode: ~1 second total
  - Stable Diffusion: ~30-60 seconds per image (GPU)

### Optimization Tips
1. Use placeholder mode for faster testing
2. Reduce `max_synthesis_length` for quicker processing
3. Limit `max_search_results` to speed up web scanning
4. Use GPU for illustration generation if available

## Security Considerations

### Dependency Security
All dependencies are regularly updated to patch security vulnerabilities:
- Transformers: >= 4.48.0 (patches deserialization vulnerabilities)
- Torch: >= 2.6.0 (patches buffer overflow and RCE vulnerabilities)
- Pillow: >= 10.2.0 (patches arbitrary code execution)

### Safe File Processing
- All file processing uses safe parsing libraries
- No execution of code from uploaded files
- Input validation on file types and sizes

### Web Scanning Safety
- Configurable user agent
- Request timeouts to prevent hanging
- Fallback mode for failed requests
- No execution of downloaded code

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'torch'"
**Solution**: Torch is optional. Run in placeholder mode or install: `pip install torch>=2.6.0`

**Issue**: "Out of memory" during illustration generation
**Solution**: Use placeholder mode or reduce `image_size` in config

**Issue**: Web scanning fails
**Solution**: Check internet connection or continue with offline validation (automatic)

**Issue**: PDF extraction returns gibberish
**Solution**: Some PDFs have image-based text. Consider using OCR preprocessing.

## Future Enhancements

Potential improvements for future versions:
- OCR support for scanned documents
- Multi-language support
- Custom illustration style selection
- Advanced NLP with transformers
- Interactive web interface
- Batch processing of multiple book sets
- Export to various formats (Markdown, HTML, etc.)

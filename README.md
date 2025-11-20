# Book Synthesis Engine

A powerful tool that synthesizes knowledge from multiple book sources with advanced features including web scanning, validity comparison, and AI-generated illustrations.

## Features

✨ **Multi-Book Processing**: Upload and process up to 5 books simultaneously (PDF, EPUB, DOCX, TXT formats)

🔍 **Web Scanning**: Automatically searches the web for additional context and validation of synthesized concepts

✅ **Validity Comparison**: Cross-references synthesized knowledge against source materials and web results to ensure accuracy

🎨 **Stable Diffusion Illustrations**: Generates AI-powered illustrations for key concepts to visualize the synthesized information

📊 **Comprehensive Reports**: Produces detailed JSON and human-readable text reports with confidence scores

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ncsound919/Book-Synthesis-Engine.git
cd Book-Synthesis-Engine
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up configuration:
```bash
cp config.example.ini config.ini
# Edit config.ini with your preferences
```

## Quick Start

### Basic Usage

Process multiple books and generate a synthesis:

```bash
python book_synthesis_engine.py book1.pdf book2.epub book3.txt
```

### With Custom Output Name

```bash
python book_synthesis_engine.py book1.pdf book2.pdf -o my_synthesis
```

### With Custom Config

```bash
python book_synthesis_engine.py book1.pdf book2.pdf -c my_config.ini
```

## Supported File Formats

- **PDF** (.pdf)
- **EPUB** (.epub)
- **Microsoft Word** (.docx, .doc)
- **Plain Text** (.txt)

## How It Works

The Book Synthesis Engine follows a comprehensive 6-step process:

1. **Document Processing**: Extracts text content from all uploaded books
2. **Knowledge Synthesis**: Identifies common themes, key concepts, and synthesizes information across sources
3. **Web Scanning**: Performs web searches on key topics to gather additional context and validation data
4. **Validity Comparison**: Cross-references synthesized knowledge against source materials and web results
5. **Illustration Generation**: Uses Stable Diffusion to create visual representations of key concepts
6. **Report Generation**: Compiles comprehensive reports with confidence scores and validation metrics

## Output

The engine generates several output files:

- `synthesis_output.json`: Complete JSON report with all data
- `synthesis_output.txt`: Human-readable synthesis report
- `illustrations/`: Directory containing generated illustrations for key concepts

### Sample Output Structure

```
outputs/
├── synthesis_output.json
└── synthesis_output.txt

illustrations/
├── illustration_01_concept_name.png
├── illustration_02_another_concept.png
└── ...
```

## Configuration

Edit `config.ini` to customize:

- API keys for enhanced features
- Maximum number of books to process
- Web scanning parameters
- Stable Diffusion model settings
- Output directories

## Requirements

- Python 3.8 or higher
- 8GB+ RAM recommended (16GB+ for Stable Diffusion)
- GPU with CUDA support (optional, for faster illustration generation)

## Advanced Features

### Web Scanning

The web scanner automatically:
- Searches for key concepts identified in the synthesis
- Gathers additional context from online sources
- Provides validation data for cross-referencing

### Validity Comparison

The validity comparator:
- Calculates confidence scores for synthesized knowledge
- Identifies concepts supported by multiple sources
- Provides detailed validation reports
- Cross-references information across all sources

### Stable Diffusion Illustrations

The illustration generator:
- Creates visual representations of key concepts
- Uses state-of-the-art AI image generation
- Produces educational-style diagrams
- Falls back to placeholders if GPU unavailable

## Troubleshooting

### Out of Memory Errors

If you encounter memory errors:
1. Reduce the number of books processed at once
2. Use CPU-only mode for Stable Diffusion (automatic fallback)
3. Reduce image size in config.ini

### Web Scanning Issues

If web scanning fails:
- The engine will use fallback mode with offline validation
- Check your internet connection
- Adjust timeout settings in config.ini

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

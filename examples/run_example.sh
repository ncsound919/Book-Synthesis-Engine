#!/bin/bash
# Example script to run the Book Synthesis Engine with sample books

echo "Book Synthesis Engine - Example Run"
echo "===================================="
echo ""
echo "This script demonstrates the Book Synthesis Engine using sample books."
echo ""

# Navigate to the repository root
cd "$(dirname "$0")/.." || exit

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Processing sample books..."
echo ""

# Run the synthesis engine with sample books
python3 book_synthesis_engine.py \
    examples/sample_book1.txt \
    examples/sample_book2.txt \
    examples/sample_book3.txt \
    -o example_synthesis

echo ""
echo "Example complete! Check the outputs/ directory for results."

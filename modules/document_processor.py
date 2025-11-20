"""
Document Processor Module
Extracts text content from various document formats
"""

import os
from pathlib import Path
from typing import Optional
import PyPDF2
import docx
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


class DocumentProcessor:
    """Handles extraction of text from various document formats"""
    
    def __init__(self, config):
        """Initialize document processor with configuration"""
        self.config = config
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a document file
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return self._extract_from_pdf(path)
        elif extension in ['.docx', '.doc']:
            return self._extract_from_docx(path)
        elif extension in ['.epub']:
            return self._extract_from_epub(path)
        elif extension in ['.txt', '.text']:
            return self._extract_from_txt(path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _extract_from_pdf(self, path: Path) -> str:
        """Extract text from PDF file"""
        text = []
        try:
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
        
        return '\n'.join(text)
    
    def _extract_from_docx(self, path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(path)
            text = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")
    
    def _extract_from_epub(self, path: Path) -> str:
        """Extract text from EPUB file"""
        try:
            book = epub.read_epub(path)
            text = []
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text.append(soup.get_text())
            
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error reading EPUB: {str(e)}")
    
    def _extract_from_txt(self, path: Path) -> str:
        """Extract text from plain text file"""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading text file: {str(e)}")

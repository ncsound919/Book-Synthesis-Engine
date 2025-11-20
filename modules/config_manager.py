"""
Configuration Manager Module
Handles loading and accessing configuration settings
"""

import os
import configparser
from pathlib import Path
from typing import Optional, Any


class ConfigManager:
    """Manages configuration settings for the Book Synthesis Engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = configparser.ConfigParser()
        
        # Set defaults
        self._set_defaults()
        
        # Load config file if provided and exists
        if config_path and Path(config_path).exists():
            self.config.read(config_path)
        elif Path('config.ini').exists():
            self.config.read('config.ini')
    
    def _set_defaults(self):
        """Set default configuration values"""
        self.config['API'] = {
            'huggingface_token': os.getenv('HUGGINGFACE_TOKEN', ''),
            'openai_api_key': os.getenv('OPENAI_API_KEY', '')
        }
        
        self.config['Paths'] = {
            'upload_dir': 'uploads',
            'output_dir': 'outputs',
            'illustration_dir': 'illustrations',
            'model_cache_dir': 'models'
        }
        
        self.config['Synthesis'] = {
            'max_books': '5',
            'min_similarity_threshold': '0.7',
            'max_synthesis_length': '5000'
        }
        
        self.config['WebScan'] = {
            'max_search_results': '10',
            'timeout_seconds': '30',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.config['StableDiffusion'] = {
            'model_name': 'runwayml/stable-diffusion-v1-5',
            'guidance_scale': '7.5',
            'num_inference_steps': '50',
            'image_size': '512'
        }
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            fallback: Fallback value if not found
            
        Returns:
            Configuration value or fallback
        """
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

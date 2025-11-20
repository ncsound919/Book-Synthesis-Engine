"""
Illustration Generator Module
Generates illustrations using Stable Diffusion for key concepts
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image


class IllustrationGenerator:
    """Generates illustrations for key concepts using Stable Diffusion"""
    
    def __init__(self, config):
        """Initialize illustration generator with configuration"""
        self.config = config
        self.model_name = config.get('StableDiffusion', 'model_name', 
                                     'runwayml/stable-diffusion-v1-5')
        self.guidance_scale = float(config.get('StableDiffusion', 'guidance_scale', 7.5))
        self.num_inference_steps = int(config.get('StableDiffusion', 'num_inference_steps', 50))
        self.image_size = int(config.get('StableDiffusion', 'image_size', 512))
        self.output_dir = Path(config.get('Paths', 'illustration_dir', 'illustrations'))
        
        self.pipeline = None
        self._initialize_pipeline()
    
    def _initialize_pipeline(self):
        """Initialize Stable Diffusion pipeline (lazy loading)"""
        # Pipeline will be loaded when first needed to save memory
        pass
    
    def _load_pipeline(self):
        """Load the Stable Diffusion pipeline"""
        if self.pipeline is None:
            print("    Loading Stable Diffusion model (this may take a while)...")
            try:
                # Check if CUDA is available
                device = "cuda" if torch.cuda.is_available() else "cpu"
                
                # Load pipeline
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                    safety_checker=None,  # Disable safety checker for faster loading
                )
                self.pipeline = self.pipeline.to(device)
                
                # Enable memory optimizations
                if device == "cuda":
                    self.pipeline.enable_attention_slicing()
                
                print(f"    Model loaded successfully on {device}")
                
            except Exception as e:
                print(f"    Warning: Could not load Stable Diffusion model: {str(e)}")
                print(f"    Will use placeholder illustrations instead.")
                self.pipeline = "placeholder"  # Use placeholder mode
    
    def generate_illustrations(self, synthesized_knowledge: Dict, 
                              validity_report: Dict) -> List[Dict]:
        """
        Generate illustrations for key concepts
        
        Args:
            synthesized_knowledge: Synthesized knowledge containing concepts
            validity_report: Validity report for context
            
        Returns:
            List of generated illustrations with metadata
        """
        key_concepts = synthesized_knowledge.get('key_concepts', [])
        
        if not key_concepts:
            print("    No key concepts found for illustration generation")
            return []
        
        # Select top concepts to illustrate (limit to avoid long generation time)
        concepts_to_illustrate = key_concepts[:5]  # Top 5 concepts
        
        print(f"    Generating illustrations for {len(concepts_to_illustrate)} key concepts...")
        
        illustrations = []
        
        for i, concept in enumerate(concepts_to_illustrate, 1):
            print(f"      [{i}/{len(concepts_to_illustrate)}] Generating illustration for: {concept}")
            
            try:
                # Generate illustration
                illustration = self._generate_single_illustration(concept, i)
                illustrations.append(illustration)
                
            except Exception as e:
                print(f"        Warning: Failed to generate illustration: {str(e)}")
                # Create placeholder
                illustrations.append(self._create_placeholder_illustration(concept, i))
        
        return illustrations
    
    def _generate_single_illustration(self, concept: str, index: int) -> Dict:
        """Generate a single illustration for a concept"""
        # Load pipeline if not already loaded
        if self.pipeline is None:
            self._load_pipeline()
        
        # If using placeholder mode or pipeline failed to load
        if self.pipeline == "placeholder" or self.pipeline is None:
            return self._create_placeholder_illustration(concept, index)
        
        # Create prompt for illustration
        prompt = self._create_prompt(concept)
        
        try:
            # Generate image
            image = self.pipeline(
                prompt,
                guidance_scale=self.guidance_scale,
                num_inference_steps=self.num_inference_steps,
                height=self.image_size,
                width=self.image_size
            ).images[0]
            
            # Save image
            filename = f"illustration_{index:02d}_{self._sanitize_filename(concept)}.png"
            filepath = self.output_dir / filename
            image.save(filepath)
            
            return {
                'concept': concept,
                'description': prompt,
                'path': str(filepath),
                'method': 'stable_diffusion'
            }
            
        except Exception as e:
            print(f"        Error during generation: {str(e)}")
            return self._create_placeholder_illustration(concept, index)
    
    def _create_placeholder_illustration(self, concept: str, index: int) -> Dict:
        """Create a placeholder illustration"""
        # Create a simple colored placeholder image
        filename = f"illustration_{index:02d}_{self._sanitize_filename(concept)}.png"
        filepath = self.output_dir / filename
        
        # Create placeholder image
        img = Image.new('RGB', (self.image_size, self.image_size), color=(100, 150, 200))
        
        # You could add text to the image here using PIL ImageDraw if desired
        
        img.save(filepath)
        
        return {
            'concept': concept,
            'description': f"Placeholder illustration for concept: {concept}",
            'path': str(filepath),
            'method': 'placeholder'
        }
    
    def _create_prompt(self, concept: str) -> str:
        """
        Create an illustration prompt from a concept
        
        Args:
            concept: Concept to illustrate
            
        Returns:
            Prompt for image generation
        """
        # Create a descriptive prompt
        prompt = (
            f"A detailed, professional illustration representing the concept of {concept}, "
            f"educational diagram style, clean and clear, high quality, "
            f"suitable for a textbook or educational material"
        )
        
        return prompt
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filename"""
        # Remove or replace invalid filename characters
        sanitized = text.lower().replace(' ', '_')
        sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
        return sanitized[:50]  # Limit length

"""
Free Image Generator using Pollinations.AI
Truly free AI image generation - no API key needed!
Uses curl for reliable downloads.
"""
import subprocess
import urllib.parse
from pathlib import Path
from typing import Dict, List
from PIL import Image
import time
import os


class ImageGenerator:
    """Generate Instagram carousel images using Pollinations.AI (free, unlimited)."""
    
    # Slide-specific prompts for AI generation
    PROMPTS = {
        "hook": {
            "prompt": "Professional business social media post, dark background, bold green neon typography saying STOP THE LEAD LEAK, modern real estate marketing, high contrast, clean design, Instagram story format",
        },
        "timeline": {
            "prompt": "Professional infographic timeline showing 3AM to 9AM, dark theme, green and red accent colors, business style, clean layout with time markers, corporate design, vertical Instagram format",
        },
        "stats": {
            "prompt": "Professional data visualization infographic, dark background, large bold numbers in neon green and red, statistics display, clean corporate business style, modern design",
        },
        "rival": {
            "prompt": "Professional split screen comparison infographic, left side showing stressed agent checking email late, right side showing successful agent with instant response, dark background, modern corporate style",
        },
        "cta": {
            "prompt": "Professional social media call-to-action post, dark background, glowing neon green button design, minimal clean marketing style, modern business aesthetic, Instagram vertical format",
        }
    }
    
    def __init__(self, output_dir: str = "/app/generated/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_image(self, prompt_key: str, slide_num: int = 1) -> str:
        """Generate a single image using Pollinations.AI via curl."""
        prompt_data = self.PROMPTS.get(prompt_key, self.PROMPTS["hook"])
        prompt = prompt_data["prompt"]
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Pollinations.AI URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1344&nologo=true"
        filepath = self.output_dir / f"slide_{slide_num:02d}_{prompt_key}.png"
        
        print(f"   Generating {prompt_key} image...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use curl for reliable download
                result = subprocess.run(
                    ["curl", "-s", "-o", str(filepath), url],
                    capture_output=True,
                    timeout=60
                )
                
                # Verify the image
                if os.path.exists(filepath):
                    try:
                        with Image.open(filepath) as img:
                            if img.size[0] > 100:  # Valid image
                                print(f"   ✅ Saved: {filepath.name}")
                                return str(filepath)
                    except:
                        pass
                        
                print(f"   ⚠️ Attempt {attempt+1}: Invalid image")
                        
            except Exception as e:
                print(f"   ⚠️ Attempt {attempt+1} failed: {e}")
                
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
                    
        print(f"   ❌ Failed to generate {prompt_key}")
        return None
    
    def generate_carousel(self, content: Dict, city: str) -> List[str]:
        """Generate full carousel using AI."""
        slides = []
        
        # Generate each slide
        slide_order = ["hook", "timeline", "stats", "rival", "cta"]
        
        for i, slide_type in enumerate(slide_order, 1):
            filepath = self.generate_image(slide_type, i)
            if filepath:
                slides.append(filepath)
            time.sleep(2)  # Rate limiting
        
        return slides


def get_image_generator() -> ImageGenerator:
    return ImageGenerator()

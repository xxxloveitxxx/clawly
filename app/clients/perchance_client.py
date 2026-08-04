"""
Perchance AI Image Generator Client
Uses unofficial Perchance API for free image generation
Based on: https://github.com/eeemoon/perchance
"""
import asyncio
import aiohttp
from pathlib import Path
from typing import Optional
from PIL import Image
from io import BytesIO


class PerchanceClient:
    """Generate images using Perchance AI (free, unlimited)."""
    
    def __init__(self, output_dir: str = "/app/generated/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = "https://perchance.org/api/generate"
    
    async def generate_image(self, prompt: str, negative_prompt: str = "",
                           seed: Optional[int] = None) -> Optional[bytes]:
        """
        Generate a single image from text prompt.
        
        Args:
            prompt: Description of the image to generate
            negative_prompt: What to avoid in the image
            seed: Optional seed for reproducibility
        
        Returns:
            Image binary data or None if failed
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Perchance API endpoint
                url = "https://perchance.org/api/generate"
                
                payload = {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "aspect_ratio": "9:16",  # Instagram portrait
                }
                
                if seed:
                    payload["seed"] = seed
                
                async with session.post(url, json=payload, timeout=60) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "image_url" in data:
                            # Download the image
                            async with session.get(data["image_url"]) as img_resp:
                                if img_resp.status == 200:
                                    return await img_resp.read()
                    return None
        except Exception as e:
            print(f"Perchance generation error: {e}")
            return None
    
    async def generate_carousel_images(self, slides: list) -> list:
        """
        Generate images for each slide of a carousel.
        
        Args:
            slides: List of slide descriptions
        
        Returns:
            List of image file paths
        """
        results = []
        
        prompts = {
            "hook": "Professional business infographic, dark background, neon green accent lighting, bold typography, clean modern design, real estate agent concept, high contrast",
            "timeline": "Professional timeline infographic, dark theme, glowing green and red elements, business style, clean layout, modern corporate design",
            "stats": "Professional statistics visualization, dark background, large numbers displayed, neon green data highlights, clean corporate infographic style",
            "rival": "Professional comparison infographic, split screen design, dark background, contrasting elements showing competition, modern business style",
            "cta": "Professional call-to-action design, dark background, glowing neon green button, clean minimal style, modern marketing design"
        }
        
        for i, slide_type in enumerate(slides):
            prompt = prompts.get(slide_type, prompts["hook"])
            
            print(f"Generating slide {i+1}: {slide_type}...")
            image_data = await self.generate_image(prompt)
            
            if image_data:
                filepath = self.output_dir / f"slide_{i+1:02d}_{slide_type}.png"
                with open(filepath, "wb") as f:
                    f.write(image_data)
                results.append(str(filepath))
                print(f"✅ Saved: {filepath}")
            else:
                print(f"⚠️ Failed to generate {slide_type}")
                results.append(None)
        
        return results
    
    def generate_sync(self, prompt: str) -> Optional[str]:
        """Synchronous wrapper for generate_image."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            image_data = loop.run_until_complete(self.generate_image(prompt))
            if image_data:
                filepath = self.output_dir / f"perchance_{hash(prompt)}.png"
                with open(filepath, "wb") as f:
                    f.write(image_data)
                return str(filepath)
        finally:
            loop.close()
        return None


def get_perchance_client() -> PerchanceClient:
    return PerchanceClient()

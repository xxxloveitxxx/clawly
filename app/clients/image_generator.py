"""
Free Image Generator for Instagram Carousels
Uses Pillow + ImageMagick for text overlay and graphics
"""
import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Any, Optional

# Instagram carousel dimensions
IG_PORTRAIT = (1080, 1350)
IG_SQUARE = (1080, 1080)

# Colors (high contrast for real estate)
COLORS = {
    "dark_bg": (26, 26, 26),           # #1a1a1a
    "neon_green": (0, 255, 136),       # #00ff88
    "neon_red": (255, 51, 102),         # #ff3366
    "white": (255, 255, 255),
    "light_gray": (200, 200, 200),
    "gold": (255, 193, 7),             # For emphasis
    "blue_accent": (33, 150, 243),     # #2196f3
}

class ImageGenerator:
    """Generate Instagram carousel images using free tools (Pillow)."""
    
    def __init__(self, output_dir: str = "/app/generated/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_gradient_background(self, width: int, height: int, 
                                   color1: tuple, color2: tuple, 
                                   direction: str = "vertical") -> Image.Image:
        """Create a gradient background."""
        base = Image.new('RGB', (width, height), color1)
        draw = ImageDraw.Draw(base)
        
        for i in range(height if direction == "vertical" else width):
            ratio = i / (height if direction == "vertical" else width)
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            
            if direction == "vertical":
                draw.line([(0, i), (width, i)], fill=(r, g, b))
            else:
                draw.line([(i, 0), (i, height)], fill=(r, g, b))
        
        return base
    
    def add_text(self, img: Image.Image, text: str, 
                 position: str = "center", fontsize: int = 60,
                 color: tuple = COLORS["white"], 
                 font_path: Optional[str] = None,
                 max_width: Optional[int] = None,
                 stroke_color: Optional[tuple] = None,
                 stroke_width: int = 2) -> Image.Image:
        """Add text to image with word wrapping."""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to load a bold font
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, fontsize)
            else:
                # Use default bold font
                font = ImageFont.load_default(size=fontsize)
        except:
            font = ImageFont.load_default(size=fontsize)
        
        # Word wrap text
        lines = self._wrap_text(text, font, max_width or (width - 100))
        
        # Calculate starting Y position
        line_height = fontsize + 10
        total_height = len(lines) * line_height
        
        if position == "center":
            start_y = (height - total_height) // 2
        elif position == "top":
            start_y = 80
        elif position == "bottom":
            start_y = height - total_height - 80
        else:
            start_y = int(position) if isinstance(position, int) else height // 2
        
        # Draw each line centered
        for i, line in enumerate(lines):
            y = start_y + i * line_height
            x = width // 2
            
            if stroke_color:
                # Draw stroke first
                for adj in range(-stroke_width, stroke_width + 1):
                    for adj_y in range(-stroke_width, stroke_width + 1):
                        if adj != 0 or adj_y != 0:
                            draw.text((x + adj, y + adj_y), line, font=font, 
                                     fill=stroke_color, anchor="mm")
            
            draw.text((x, y), line, font=font, fill=color, anchor="mm")
        
        return img
    
    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = font.getbbox(test_line)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]
    
    def draw_circle(self, img: Image.Image, center: tuple, 
                    radius: int, color: tuple, width: int = 3) -> Image.Image:
        """Draw a circle on the image."""
        draw = ImageDraw.Draw(img)
        bbox = [center[0] - radius, center[1] - radius,
                center[0] + radius, center[1] + radius]
        draw.ellipse(bbox, outline=color, width=width)
        return img
    
    def draw_arrow(self, img: Image.Image, start: tuple, end: tuple,
                   color: tuple = COLORS["neon_green"], width: int = 3) -> Image.Image:
        """Draw an arrow."""
        draw = ImageDraw.Draw(img)
        draw.line([start, end], fill=color, width=width)
        # Arrow head
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            dx, dy = dx/length, dy/length
            arrow_size = 15
            draw.polygon([
                (end[0], end[1]),
                (end[0] - arrow_size*dx + arrow_size*0.5*dy, 
                 end[1] - arrow_size*dy - arrow_size*0.5*dx),
                (end[0] - arrow_size*dx - arrow_size*0.5*dy,
                 end[1] - arrow_size*dy + arrow_size*0.5*dx)
            ], fill=color)
        return img
    
    def add_progress_bar(self, img: Image.Image, y_position: int,
                         filled_percent: float, color: tuple = COLORS["neon_green"],
                         bg_color: tuple = COLORS["light_gray"]) -> Image.Image:
        """Add a progress/decay bar."""
        draw = ImageDraw.Draw(img)
        width, _ = img.size
        bar_width = width - 200
        bar_height = 30
        x = 100
        
        # Background
        draw.rectangle([x, y_position, x + bar_width, y_position + bar_height], 
                       fill=bg_color, outline=None)
        
        # Filled portion
        filled_width = int(bar_width * filled_percent)
        if filled_width > 0:
            draw.rectangle([x, y_position, x + filled_width, y_position + bar_height],
                          fill=color, outline=None)
        
        return img
    
    def create_hook_slide(self, headline: str, subtext: str = "") -> str:
        """Create Slide 1: The Hook with bold M.A.G.I.C. headline."""
        img = self.create_gradient_background(
            IG_PORTRAIT[0], IG_PORTRAIT[1],
            COLORS["dark_bg"], (40, 40, 40)
        )
        
        # Main headline
        self.add_text(img, headline, position="center", fontsize=72,
                     color=COLORS["neon_green"], stroke_color=COLORS["dark_bg"],
                     stroke_width=3)
        
        # Subtext
        if subtext:
            self.add_text(img, subtext, position="+250", fontsize=36,
                         color=COLORS["white"])
        
        # Bottom accent bar
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, IG_PORTRAIT[1]-10, IG_PORTRAIT[0], IG_PORTRAIT[1]], 
                       fill=COLORS["neon_green"])
        
        filepath = self.output_dir / "slide_01_hook.png"
        img.save(filepath, "PNG", quality=95)
        return str(filepath)
    
    def create_timeline_slide(self, timeline_data: Dict[str, str]) -> str:
        """Create Slide 2: Timeline showing lead decay."""
        img = self.create_gradient_background(
            IG_PORTRAIT[0], IG_PORTRAIT[1],
            COLORS["dark_bg"], (30, 30, 50)
        )
        
        # Title
        self.add_text(img, "THE TIMELINE OF A LOST COMMISSION",
                     position=100, fontsize=48, color=COLORS["neon_red"],
                     stroke_color=COLORS["dark_bg"], stroke_width=2)
        
        # Timeline entries
        y_start = 300
        for i, (time, event) in enumerate(timeline_data.items()):
            y = y_start + i * 140
            
            # Time badge
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle([100, y, 280, y+60], radius=10, 
                                   fill=COLORS["neon_green"])
            self.add_text(img, time, position=(190, y+30), fontsize=28,
                         color=COLORS["dark_bg"])
            
            # Event text
            self.add_text(img, event, position=(320, y+30), fontsize=32,
                         color=COLORS["white"])
            
            # Arrow down (except last)
            if i < len(timeline_data) - 1:
                self.draw_arrow(img, (190, y+70), (190, y+100),
                              color=COLORS["light_gray"], width=2)
        
        filepath = self.output_dir / "slide_02_timeline.png"
        img.save(filepath, "PNG", quality=95)
        return str(filepath)
    
    def create_math_slide(self, stats: List[Dict[str, Any]]) -> str:
        """Create Slide 3: Data/math breakdown."""
        img = self.create_gradient_background(
            IG_PORTRAIT[0], IG_PORTRAIT[1],
            COLORS["dark_bg"], (20, 40, 20)
        )
        
        # Title
        self.add_text(img, "THE MATH", position=80, fontsize=60,
                     color=COLORS["neon_green"], stroke_color=COLORS["dark_bg"],
                     stroke_width=2)
        
        # Stats
        y = 300
        for stat in stats:
            # Big number
            self.add_text(img, stat["value"], position=(540, y), fontsize=96,
                         color=stat.get("color", COLORS["neon_green"]),
                         stroke_color=COLORS["dark_bg"], stroke_width=3)
            
            # Label
            self.add_text(img, stat["label"], position=(540, y+100), fontsize=32,
                         color=COLORS["white"])
            
            y += 200
        
        filepath = self.output_dir / "slide_03_math.png"
        img.save(filepath, "PNG", quality=95)
        return str(filepath)
    
    def create_rival_slide(self, you_text: str, rival_text: str) -> str:
        """Create Slide 4: You vs Rival comparison."""
        img = self.create_gradient_background(
            IG_PORTRAIT[0], IG_PORTRAIT[1],
            COLORS["dark_bg"], COLORS["dark_bg"]
        )
        
        # Center divider
        draw = ImageDraw.Draw(img)
        draw.line([(540, 150), (540, 1200)], fill=COLORS["neon_red"], width=3)
        
        # Left side (YOU - bad)
        self.add_text(img, "YOU", position=(270, 120), fontsize=48,
                     color=COLORS["neon_red"], stroke_color=COLORS["dark_bg"])
        self.add_text(img, you_text, position=(270, 600), fontsize=40,
                     color=COLORS["light_gray"])
        
        # Right side (RIVAL - good)
        self.add_text(img, "RIVAL", position=(810, 120), fontsize=48,
                     color=COLORS["neon_green"], stroke_color=COLORS["dark_bg"])
        self.add_text(img, rival_text, position=(810, 600), fontsize=40,
                     color=COLORS["white"])
        
        # VS badge
        draw.ellipse([490, 350, 590, 450], fill=COLORS["gold"])
        self.add_text(img, "VS", position=(540, 400), fontsize=36,
                     color=COLORS["dark_bg"])
        
        filepath = self.output_dir / "slide_04_rival.png"
        img.save(filepath, "PNG", quality=95)
        return str(filepath)
    
    def create_cta_slide(self, main_text: str, secondary_text: str = "") -> str:
        """Create Slide 5: Call to Action."""
        img = self.create_gradient_background(
            IG_PORTRAIT[0], IG_PORTRAIT[1],
            (10, 30, 20), COLORS["dark_bg"]
        )
        
        # Main CTA button
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([140, 400, 940, 600], radius=30,
                               fill=COLORS["neon_green"])
        self.add_text(img, main_text, position=(540, 500), fontsize=56,
                     color=COLORS["dark_bg"])
        
        # Secondary text
        if secondary_text:
            self.add_text(img, secondary_text, position="+200", fontsize=32,
                         color=COLORS["light_gray"])
        
        # Top accent
        draw.rectangle([0, 0, IG_PORTRAIT[0], 8], fill=COLORS["neon_green"])
        
        filepath = self.output_dir / "slide_05_cta.png"
        img.save(filepath, "PNG", quality=95)
        return str(filepath)
    
    def generate_carousel(self, content: Dict[str, Any], city: str) -> List[str]:
        """Generate full carousel from content data."""
        slides = []
        
        # Slide 1: Hook
        slides.append(self.create_hook_slide(
            content.get("hook", "STOP THE LEAD LEAK"),
            content.get("subtext", f"For Top Agents in {city}")
        ))
        
        # Slide 2: Timeline
        if "timeline" in content:
            slides.append(self.create_timeline_slide(content["timeline"]))
        
        # Slide 3: Math
        if "stats" in content:
            slides.append(self.create_math_slide(content["stats"]))
        
        # Slide 4: Rival
        if "you_vs_rival" in content:
            slides.append(self.create_rival_slide(
                content["you_vs_rival"]["you"],
                content["you_vs_rival"]["rival"]
            ))
        
        # Slide 5: CTA
        slides.append(self.create_cta_slide(
            content.get("cta", "DM 'LEAK'"),
            content.get("scarcity", "Limited to 3 reports this week")
        ))
        
        return slides


def get_image_generator() -> ImageGenerator:
    """Factory function."""
    return ImageGenerator()

"""
Free Image Generator for Instagram Carousels
Uses Pillow for text overlay and graphics - no API costs!
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Any, Tuple

# Instagram carousel dimensions
IG_WIDTH = 1080
IG_HEIGHT = 1350

# Colors (RGB tuples)
BLACK = (0, 0, 0)
DARK_GRAY = (26, 26, 26)
WHITE = (255, 255, 255)
LIGHT_GRAY = (180, 180, 180)
NEON_GREEN = (0, 255, 136)
NEON_RED = (255, 51, 102)
GOLD = (255, 193, 7)


class ImageGenerator:
    """Generate Instagram carousel images - clean, readable, professional."""
    
    def __init__(self, output_dir: str = "/app/generated/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = IG_WIDTH
        self.height = IG_HEIGHT
    
    def create_solid_bg(self, color: Tuple[int, int, int]) -> Image.Image:
        """Create solid color background."""
        return Image.new('RGB', (self.width, self.height), color)
    
    def get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get a bold font - tries common system fonts."""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ]
        
        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    pass
        
        # Fallback to default
        return ImageFont.load_default()
    
    def draw_centered_text(self, draw: ImageDraw.Draw, text: str, 
                           y: int, font: ImageFont.FreeTypeFont,
                           color: Tuple[int, int, int],
                           max_width: int = 900) -> int:
        """Draw text centered, return actual height used."""
        # Simple word wrap
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test = (current_line + " " + word).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        if not lines:
            lines = [text]
        
        # Draw each line
        line_height = font.size + 15
        total_height = len(lines) * line_height
        start_y = y - total_height // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            draw.text((x, start_y + i * line_height), line, font=font, fill=color)
        
        return total_height
    
    def draw_rounded_rect(self, draw: ImageDraw.Draw, 
                          x1: int, y1: int, x2: int, y2: int,
                          color: Tuple[int, int, int], radius: int = 15):
        """Draw rounded rectangle."""
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=color)
    
    # ========== SLIDE 1: HOOK ==========
    def create_hook_slide(self, headline: str, subtext: str = "") -> str:
        """Bold hook slide with headline."""
        img = self.create_solid_bg(BLACK)
        draw = ImageDraw.Draw(img)
        
        # Top accent bar
        draw.rectangle([0, 0, self.width, 8], fill=NEON_GREEN)
        
        # Main headline - BIG and centered
        font = self.get_font(80)
        self.draw_centered_text(draw, headline.upper(), self.height // 2 - 50, 
                               font, NEON_GREEN)
        
        # Subtext below
        if subtext:
            font_small = self.get_font(36)
            self.draw_centered_text(draw, subtext, self.height // 2 + 100,
                                  font_small, WHITE)
        
        # Bottom accent bar
        draw.rectangle([0, self.height - 15, self.width, self.height], 
                      fill=NEON_GREEN)
        
        filepath = self.output_dir / "slide_01_hook.png"
        img.save(filepath, "PNG")
        return str(filepath)
    
    # ========== SLIDE 2: TIMELINE ==========
    def create_timeline_slide(self, timeline: Dict[str, str]) -> str:
        """Clean timeline slide."""
        img = self.create_solid_bg(DARK_GRAY)
        draw = ImageDraw.Draw(img)
        
        # Title
        font_title = self.get_font(48)
        self.draw_centered_text(draw, "TIMELINE OF A LOST DEAL", 80, 
                               font_title, NEON_RED)
        
        # Timeline entries
        entries = list(timeline.items())
        start_y = 250
        spacing = 220
        
        for i, (time_str, event) in enumerate(entries):
            y = start_y + i * spacing
            
            # Time box
            self.draw_rounded_rect(draw, 80, y, 300, y + 70, NEON_GREEN, 10)
            
            # Time text
            font_time = self.get_font(28)
            bbox = draw.textbbox((0, 0), time_str, font=font_time)
            text_w = bbox[2] - bbox[0]
            draw.text((80 + (220 - text_w) // 2, y + 22), time_str, 
                     font=font_time, fill=BLACK)
            
            # Event text
            font_event = self.get_font(32)
            draw.text((340, y + 20), event, font=font_event, fill=WHITE)
            
            # Arrow between (except last)
            if i < len(entries) - 1:
                arrow_y = y + 85
                draw.line([(190, arrow_y), (190, arrow_y + 120)], 
                         fill=LIGHT_GRAY, width=4)
                # Arrow head
                draw.polygon([(190, arrow_y + 130), 
                            (175, arrow_y + 110),
                            (205, arrow_y + 110)], fill=LIGHT_GRAY)
        
        filepath = self.output_dir / "slide_02_timeline.png"
        img.save(filepath, "PNG")
        return str(filepath)
    
    # ========== SLIDE 3: STATS ==========
    def create_stats_slide(self, stats: List[Dict]) -> str:
        """Stats/metrics slide with big numbers."""
        img = self.create_solid_bg(BLACK)
        draw = ImageDraw.Draw(img)
        
        # Title
        font_title = self.get_font(52)
        self.draw_centered_text(draw, "THE NUMBERS DON'T LIE", 80, 
                               font_title, WHITE)
        
        # Stats
        y = 300
        for stat in stats:
            # Big number
            font_big = self.get_font(100)
            color = NEON_GREEN if stat.get("positive") else NEON_RED
            self.draw_centered_text(draw, stat["value"], y, font_big, color)
            
            # Label
            font_label = self.get_font(32)
            self.draw_centered_text(draw, stat["label"], y + 100, 
                                   font_label, LIGHT_GRAY)
            
            y += 220
        
        filepath = self.output_dir / "slide_03_stats.png"
        img.save(filepath, "PNG")
        return str(filepath)
    
    # ========== SLIDE 4: YOU VS RIVAL ==========
    def create_rival_slide(self, you_text: str, rival_text: str) -> str:
        """Side by side comparison."""
        img = self.create_solid_bg(BLACK)
        draw = ImageDraw.Draw(img)
        
        center_x = self.width // 2
        
        # Left side - YOU (red)
        font_label = self.get_font(52)
        self.draw_centered_text(draw, "YOU", center_x // 2, 150, 
                               font_label, NEON_RED)
        
        font_text = self.get_font(36)
        self.draw_centered_text(draw, you_text, 600, font_text, LIGHT_GRAY)
        
        # Right side - RIVAL (green)
        self.draw_centered_text(draw, "RIVAL", center_x + center_x // 2, 150,
                               font_label, NEON_GREEN)
        self.draw_centered_text(draw, rival_text, 600, font_text, WHITE)
        
        # Center divider
        draw.line([(center_x, 80), (center_x, self.height - 80)], 
                 fill=WHITE, width=3)
        
        # VS circle
        draw.ellipse([center_x - 40, 380, center_x + 40, 460], fill=GOLD)
        font_vs = self.get_font(32)
        bbox = draw.textbbox((0, 0), "VS", font=font_vs)
        vs_w = bbox[2] - bbox[0]
        draw.text((center_x - vs_w // 2, 395), "VS", font=font_vs, fill=BLACK)
        
        filepath = self.output_dir / "slide_04_rival.png"
        img.save(filepath, "PNG")
        return str(filepath)
    
    # ========== SLIDE 5: CTA ==========
    def create_cta_slide(self, main_text: str, subtext: str = "") -> str:
        """Call to action slide."""
        img = self.create_solid_bg(BLACK)
        draw = ImageDraw.Draw(img)
        
        # Top accent
        draw.rectangle([0, 0, self.width, 10], fill=NEON_GREEN)
        
        # Main CTA button
        btn_y = self.height // 2 - 80
        self.draw_rounded_rect(draw, 100, btn_y, self.width - 100, btn_y + 160, 
                              NEON_GREEN, 20)
        
        font_cta = self.get_font(64)
        bbox = draw.textbbox((0, 0), main_text, font=font_cta)
        text_w = bbox[2] - bbox[0]
        draw.text(((self.width - text_w) // 2, btn_y + 55), main_text,
                 font=font_cta, fill=BLACK)
        
        # Subtext
        if subtext:
            font_sub = self.get_font(32)
            self.draw_centered_text(draw, subtext, btn_y + 220, font_sub, WHITE)
        
        # Bottom accent
        draw.rectangle([0, self.height - 15, self.width, self.height],
                      fill=NEON_GREEN)
        
        filepath = self.output_dir / "slide_05_cta.png"
        img.save(filepath, "PNG")
        return str(filepath)
    
    # ========== GENERATE ALL ==========
    def generate_carousel(self, content: Dict, city: str) -> List[str]:
        """Generate full carousel."""
        slides = []
        
        slides.append(self.create_hook_slide(
            content.get("hook", "STOP THE LEAD LEAK"),
            f"For Top 1% {city} Agents"
        ))
        
        if "timeline" in content:
            slides.append(self.create_timeline_slide(content["timeline"]))
        
        if "stats" in content:
            slides.append(self.create_stats_slide(content["stats"]))
        
        if "you_vs_rival" in content:
            slides.append(self.create_rival_slide(
                content["you_vs_rival"]["you"],
                content["you_vs_rival"]["rival"]
            ))
        
        slides.append(self.create_cta_slide(
            content.get("cta", "DM 'LEAK'"),
            content.get("scarcity", "Only 3 reports this week")
        ))
        
        return slides


def get_image_generator() -> ImageGenerator:
    return ImageGenerator()

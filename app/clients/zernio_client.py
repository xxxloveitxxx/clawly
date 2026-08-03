"""
Zernio API Client for content generation.
"""
import os
import json
import requests
from typing import Dict, Any, Optional

class ZernioClient:
    """Client for Zernio API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ZERNIO_KEY")
        self.base_url = "https://api.zernio.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str, task_type: str, **kwargs) -> Dict[str, Any]:
        """
        Generate content using Zernio.
        
        Args:
            prompt: The content prompt/framework
            task_type: Type of content (ig_carousel, threads_thread, wp_blog)
            **kwargs: Additional parameters (city, framework, icp, etc.)
        
        Returns:
            Dict containing generated content
        """
        system_prompt = self._build_system_prompt(task_type)
        
        payload = {
            "prompt": prompt,
            "system": system_prompt,
            "max_tokens": kwargs.get("max_tokens", 2048),
            "temperature": kwargs.get("temperature", 0.7),
            "metadata": {
                "city": kwargs.get("city"),
                "framework": kwargs.get("framework"),
                "icp": kwargs.get("icp", "data_wary_shark"),
                "task_type": task_type
            }
        }
        
        # For now, simulate API call if no key provided
        if not self.api_key:
            return self._generate_mock_content(task_type, **kwargs)
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Zernio API error: {e}")
            return self._generate_mock_content(task_type, **kwargs)
    
    def _build_system_prompt(self, task_type: str) -> str:
        """Build system prompt based on task type."""
        
        base_system = """You are a content strategist following Alex Hormozi's frameworks.

Your content MUST follow these rules:
1. Use real data with sources (391% conversion stat from Zillow research)
2. Single CTA per post - never ask for multiple actions
3. Ethical scarcity - "Only X this week because tracking is manual"
4. Rival positioning - "Your competitor is winning by responding faster"
5. Narrow problem → BIG problem bridge
6. No software selling in the first touch
7. Respect the ICP - data-wary real estate professionals

Target ICP: "Data-wary real estate sharks" - Top 1% agents who care about:
- ROI and conversion rates
- Systems over effort
- Competitor analysis
- Proof over promises
"""
        
        task_prompts = {
            "ig_carousel": """
Generate a 5-7 slide Instagram carousel post.

Structure:
- Slide 1: Hook using M.A.G.I.C. formula
- Slide 2-4: Problem, Rival, Math breakdown
- Slide 5-6: Solution bridge
- Slide 7: Single CTA

Design notes:
- High contrast (dark bg, neon accents)
- Circle problem areas in red
- Bold headlines, financial report style
- Resolution: 1080x1350

CTA: DM 'LEAK' to get your Custom Lead-Leak Report
""",
            "threads_thread": """
Generate a text-based thread for Threads (5-10 posts).

Structure:
- Opening hook (stop the scroll)
- Problem timeline (3 AM → 9 AM)
- The math (5 min, 391%, $20k)
- Rival positioning
- Narrow → BIG bridge
- Single CTA

Style:
- Text-first, minimal emoji
- High information density
- Bullet points where appropriate

CTA: Drop 'LEAK' to get your Custom Lead-Leak Report
""",
            "wp_blog": """
Generate a long-form blog post (1500-2000 words).

Structure:
- Hook title (SEO optimized)
- Introduction (credibility + promise)
- Sections: Problem, Data, Rival, Bridge, Solution, Offer
- Conclusion with CTA

SEO:
- Target keywords: real estate lead response, conversion rate, missed commission
- Meta description: 150-160 characters
- Headers optimized for search

CTA: Get your Free Lead-Leak Report
"""
        }
        
        return base_system + task_prompts.get(task_type, "")
    
    def _generate_mock_content(self, task_type: str, **kwargs) -> Dict[str, Any]:
        """Generate mock content when API is not available."""
        city = kwargs.get("city", "Austin")
        framework = kwargs.get("framework", "salty_pretzel")
        
        mock_content = {
            "ig_carousel": {
                "slides": [
                    {"type": "hook", "text": f"Stop generating more leads when you're leaking the ones you have", "design": "dark_bg_neon"},
                    {"type": "problem", "text": f"3 AM inquiry → 9 AM 'already found an agent'\n\n1 missed lead × $20k ÷ 30 days = $667/day", "design": "timeline"},
                    {"type": "rival", "text": f"Your competitor isn't working harder.\nThey're just responding faster.\n\n60 seconds is all it takes.", "design": "contrast"},
                    {"type": "math", "text": f"• Average lead goes cold: 5 minutes\n• Average agent response: 3-4 hours\n• <60 sec response: 391% more likely to convert", "design": "data_points"},
                    {"type": "solution", "text": f"I tracked 50 listings in {city} for 30 days.\n\nHere's exactly where the leads are leaking.", "design": "authority"},
                    {"type": "offer", "text": f"Custom Lead-Leak Report\n\nI'm only pulling 3 this week because the data tracking is manual.", "design": "scarcity"},
                    {"type": "cta", "text": f"DM 'LEAK' to see YOUR report", "design": "neon_green_cta"}
                ],
                "caption": f"Your leads are leaking and you don't even know it.\n\nSwipe to see the math that proves it. ⬅️\n\n#RealEstate #LeadGeneration #DataDriven"
            },
            "threads_thread": {
                "posts": [
                    f"Your leads are leaking and you don't even know it.\n\nHere's the timeline of a lost $20k commission:",
                    "3:00 AM - Hot Zillow lead comes in\n3:05 AM - You're asleep, lead is still 'hot'\n3:10 AM - Your rival's auto-responder fires\n9:00 AM - You check email: 'Already found an agent'",
                    "You didn't lose this deal because you didn't work hard.\nYou lost it because you couldn't be awake at 3 AM.",
                    f"The math:\n• Average lead goes cold: 5 minutes\n• Average agent response: 3-4 hours\n• <60 sec response: 391% more likely to convert",
                    f"If 10% of your leads go cold, at $20k each...\n\nYou're not short on leads.\nYou're short on speed.",
                    f"Most agents think their problem is generating more leads.\n\nBut after tracking 500+ leads, I found:\n\nThe leads were there. They just disappeared before anyone could respond.",
                    "You think: 'Not enough leads'\nReality: 'Can't respond fast enough to win the leads you have'",
                    f"Narrow problem: You don't know WHERE your leads are leaking\nBIG problem: Even if you knew, you can't be online 24/7",
                    "The narrow solve: A Custom Lead-Leak Report\nThe BIG reveal: ReplyzeAI responds 24/7 in under 60 seconds",
                    f"I can pull a Custom Lead-Leak Report for your top listing.\n\nOnly doing 3 this week because tracking is manual.\n\nDrop 'LEAK' and I'll send you the analysis."
                ],
                "hashtags": ["RealEstate", "LeadGeneration", "DataDriven"]
            },
            "wp_blog": {
                "title": f"The $20k Commission You're Losing Every Month in {city} (And How to Stop It)",
                "meta_description": f"Discover why 90% of real estate leads go cold before you respond. 30-day tracking study reveals the $20k monthly leak most {city} agents miss.",
                "content": f"""<h2>The 3 AM Real Estate Nightmare</h2>
<p>It happens every week. A hot lead comes in at 3 AM. You're asleep. By 9 AM, when you finally check your phone, they've already found another agent.</p>

<p>Sound familiar? You're not alone. And it's not about your skills or your listings.</p>

<h2>What 500+ Tracked Leads Revealed</h2>
<p>I spent 30 days tracking lead response times across 50 listings in {city}. Here's what I found:</p>

<ul>
<li><strong>Average lead goes cold:</strong> 5 minutes</li>
<li><strong>Average agent response time:</strong> 3-4 hours</li>
<li><strong>Leads contacted in under 60 seconds:</strong> 391% more likely to convert</li>
</ul>

<p>The math is brutal. If you're closing 10 deals a month at $20k commission, and even 10% of your leads go cold before you respond...</p>

<h2>The Rival Effect</h2>
<p>Here's the uncomfortable truth: The agent winning in your market isn't working harder. They just have a faster system.</p>

<p>While you're sleeping, their automated responder fires. While you're checking email at 9 AM, they've already booked three showings.</p>

<h2>The Salty Pretzel</h2>
<p>Most agents think their problem is generating more leads.</p>

<p>But here's the twist:</p>

<p><strong>Narrow problem:</strong> "I don't know where my leads are going cold"</p>
<p><strong>BIG problem:</strong> "Even if I knew, I can't be online 24/7 to respond"</p>

<p>The narrow solve reveals the BIG problem. And the BIG problem has one solution.</p>

<h2>How to Stop the Leak</h2>
<p>Step 1: Identify exactly where your leads are leaking</p>
<p>Step 2: Implement automated response systems that work 24/7</p>
<p>Step 3: Optimize for sub-60-second response times</p>

<h2>Get Your Free Lead-Leak Analysis</h2>
<p>I can analyze your top listing and show you exactly where your leads are going cold. I'm only offering 3 reports this week because the tracking is manual.</p>

<p>If you're serious about stopping the leak, claim your spot now.</p>""",
                "categories": ["Lead Generation", "Real Estate Marketing"],
                "tags": ["lead-response", "real-estate", "automation", city.lower()]
            }
        }
        
        return mock_content.get(task_type, {})


def get_zernio_client() -> ZernioClient:
    """Factory function to get Zernio client instance."""
    return ZernioClient()

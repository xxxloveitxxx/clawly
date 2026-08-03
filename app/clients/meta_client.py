"""
Meta API Client for Instagram and Threads publishing.
"""
import os
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class MetaClient:
    """Client for Meta (Instagram/Threads) API integration."""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("META_TOKEN")
        self.graph_base = "https://graph.facebook.com/v18.0"
        
        # For demo/testing, we'll simulate posts
        self._demo_mode = not bool(self.access_token)
    
    def publish_ig_carousel(self, content: Dict[str, Any], page_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Publish an Instagram carousel post.
        
        Args:
            content: Dict with keys:
                - slides: List of slide content
                - caption: Post caption
                - city: Target city
                - framework: Framework used
            page_id: Instagram page ID
        
        Returns:
            Dict with post status and details
        """
        if self._demo_mode:
            print("🎭 Demo mode: Would publish IG carousel")
            print(f"   Caption: {content.get('caption', '')[:100]}...")
            print(f"   Slides: {len(content.get('slides', []))} slides")
            return {
                "status": "demo",
                "platform": "instagram",
                "type": "carousel",
                "demo_content": content
            }
        
        # Real API implementation would:
        # 1. Upload each slide as an image
        # 2. Create carousel container
        # 3. Publish with caption
        
        try:
            # Placeholder for real implementation
            # Requires: Instagram Business Account, Facebook Page, App Review
            return {
                "status": "not_implemented",
                "message": "Real IG API requires app review and business account setup"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def publish_threads_post(self, content: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Publish a Threads thread.
        
        Args:
            content: Dict with keys:
                - posts: List of thread posts
                - hashtags: Optional hashtags
                - city: Target city
                - framework: Framework used
            user_id: Threads user ID
        
        Returns:
            Dict with post status and details
        """
        if self._demo_mode:
            print("🎭 Demo mode: Would publish Threads thread")
            post_count = len(content.get("posts", []))
            hashtags = content.get("hashtags", [])
            print(f"   Posts: {post_count} in thread")
            print(f"   Hashtags: {', '.join(hashtags)}")
            return {
                "status": "demo",
                "platform": "threads",
                "type": "thread",
                "post_count": post_count,
                "demo_content": content
            }
        
        try:
            # Threads API endpoint
            threads_url = f"{self.graph_base}/me/threads"
            
            # Build thread content
            full_text = "\n\n".join(content.get("posts", []))
            if content.get("hashtags"):
                full_text += "\n\n" + " ".join([f"#{h}" for h in content["hashtags"]])
            
            payload = {
                "message": full_text,
                "access_token": self.access_token
            }
            
            response = requests.post(threads_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "status": "success",
                "platform": "threads",
                "post_id": result.get("id"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Threads API error: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_post_metrics(self, post_id: str, platform: str = "threads") -> Dict[str, Any]:
        """Get metrics for a published post."""
        if self._demo_mode:
            return {
                "status": "demo",
                "metrics": {
                    "impressions": 0,
                    "likes": 0,
                    "replies": 0,
                    "reposts": 0
                }
            }
        
        try:
            # Placeholder for metrics API
            return {"status": "not_implemented"}
        except Exception as e:
            return {"status": "error", "error": str(e)}


def get_meta_client() -> MetaClient:
    """Factory function to get Meta client instance."""
    return MetaClient()

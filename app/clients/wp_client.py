"""
WordPress REST API Client for blog publishing.
Uses Application Password authentication.
"""
import os
import base64
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class WordPressClient:
    """Client for WordPress REST API integration."""
    
    def __init__(self, site_url: Optional[str] = None, username: Optional[str] = None, app_password: Optional[str] = None):
        self.site_url = site_url or os.getenv("WP_URL", "").rstrip("/")
        self.username = username or os.getenv("WP_USER", "hermes_agent")
        self.app_password = app_password or os.getenv("WP_PASS")
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        
        # Build auth header
        credentials = f"{self.username}:{self.app_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    def publish_blog(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish a blog post to WordPress.
        
        Args:
            content: Dict with keys:
                - title: Post title
                - content: HTML content
                - meta_description: SEO description
                - categories: List of category names
                - tags: List of tag names
                - city: Target city (for metadata)
                - framework: Framework used (for metadata)
        
        Returns:
            Dict with post details including ID and URL
        """
        # First, ensure categories exist
        category_ids = []
        for cat_name in content.get("categories", []):
            cat_id = self._get_or_create_category(cat_name)
            if cat_id:
                category_ids.append(cat_id)
        
        # Ensure tags exist
        tag_ids = []
        for tag_name in content.get("tags", []):
            tag_id = self._get_or_create_tag(tag_name)
            if tag_id:
                tag_ids.append(tag_id)
        
        # Build post payload
        post_data = {
            "title": content.get("title", "Untitled"),
            "content": content.get("content", ""),
            "status": "draft",  # Start as draft for review
            "categories": category_ids,
            "tags": tag_ids,
            "meta": {
                "city": content.get("city", ""),
                "framework": content.get("framework", ""),
                "icp": "data_wary_shark",
                "generated_at": datetime.utcnow().isoformat()
            }
        }
        
        # Add excerpt for SEO
        if content.get("meta_description"):
            post_data["excerpt"] = f"<p>{content['meta_description']}</p>"
        
        # Make the API call
        if not self.app_password:
            print("⚠️ No WordPress app password configured. Skipping publish.")
            return {"status": "skipped", "reason": "no_credentials"}
        
        try:
            response = requests.post(
                f"{self.api_base}/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "status": "success",
                "id": result.get("id"),
                "url": result.get("link"),
                "edit_url": f"{self.site_url}/wp-admin/post.php?post={result.get('id')}&action=edit"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ WordPress API error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _get_or_create_category(self, name: str) -> Optional[int]:
        """Get category ID by name, or create it if not exists."""
        # Search for existing category
        try:
            search_response = requests.get(
                f"{self.api_base}/categories",
                headers=self.headers,
                params={"search": name},
                timeout=10
            )
            
            if search_response.ok:
                categories = search_response.json()
                for cat in categories:
                    if cat["name"].lower() == name.lower():
                        return cat["id"]
            
            # Create new category
            create_response = requests.post(
                f"{self.api_base}/categories",
                headers=self.headers,
                json={"name": name},
                timeout=10
            )
            
            if create_response.ok:
                return create_response.json().get("id")
                
        except requests.exceptions.RequestException:
            pass
        
        return None
    
    def _get_or_create_tag(self, name: str) -> Optional[int]:
        """Get tag ID by name, or create it if not exists."""
        try:
            search_response = requests.get(
                f"{self.api_base}/tags",
                headers=self.headers,
                params={"search": name},
                timeout=10
            )
            
            if search_response.ok:
                tags = search_response.json()
                for tag in tags:
                    if tag["name"].lower() == name.lower():
                        return tag["id"]
            
            # Create new tag
            create_response = requests.post(
                f"{self.api_base}/tags",
                headers=self.headers,
                json={"name": name},
                timeout=10
            )
            
            if create_response.ok:
                return create_response.json().get("id")
                
        except requests.exceptions.RequestException:
            pass
        
        return None
    
    def update_post(self, post_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing post."""
        try:
            response = requests.post(
                f"{self.api_base}/posts/{post_id}",
                headers=self.headers,
                json=updates,
                timeout=30
            )
            response.raise_for_status()
            return {"status": "success", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}
    
    def publish_post(self, post_id: int) -> Dict[str, Any]:
        """Change post status to published."""
        return self.update_post(post_id, {"status": "publish"})
    
    def get_recent_posts(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent posts."""
        try:
            response = requests.get(
                f"{self.api_base}/posts",
                headers=self.headers,
                params={"per_page": count, "status": "any"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching posts: {e}")
            return []


def get_wordpress_client() -> WordPressClient:
    """Factory function to get WordPress client instance."""
    return WordPressClient()

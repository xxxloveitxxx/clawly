import os
import time
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Add app to path for imports
sys.path.insert(0, "/app")

from rag_engine import get_hormozi_guardrails
from clients import get_zernio_client, get_wordpress_client, get_meta_client, get_image_generator


def load_prompt_template(framework: str, task_type: str) -> str:
    """Load the prompt template for the given framework and task type."""
    prompt_path = f"/app/prompts/{task_type}.md"
    try:
        with open(prompt_path, "r") as f:
            template = f.read()
            # Replace placeholders
            return template
    except FileNotFoundError:
        print(f"⚠️ Prompt template not found: {prompt_path}")
        return ""


def save_generated_content(content: Dict, task_type: str, city: str) -> str:
    """Save generated content for review."""
    output_dir = "/app/generated"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{task_type}_{city}_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(content, f, indent=2)
    
    print(f"📄 Content saved to: {filename}")
    return filename


def main():
    print("=" * 60)
    print("🤖 HERMES AGENT - Content Executor")
    print("=" * 60)
    
    # Get task parameters from environment
    task_type = os.getenv("TASK_TYPE", "threads_thread")
    framework = os.getenv("FRAMEWORK", "salty_pretzel")
    city = os.getenv("CITY", "Austin")
    icp = os.getenv("TARGET_ICP", "data_wary_shark")
    
    # Sleep duration config (for mimicking human cadence)
    sleep_minutes = int(os.getenv("SLEEP_MINUTES", "30"))
    
    print(f"\n📋 Task Parameters:")
    print(f"   • Task Type: {task_type}")
    print(f"   • Framework: {framework}")
    print(f"   • Target City: {city}")
    print(f"   • ICP: {icp}")
    print(f"   • Sleep Duration: {sleep_minutes} minutes")
    
    # Step 1: Enforce Guardrails from Hormozi Books
    print("\n📖 Step 1: Querying Hormozi Books for guardrails...")
    try:
        guardrails = get_hormozi_guardrails(framework)
        print(f"   ✅ Loaded {len(guardrails)} characters of guardrails")
    except Exception as e:
        print(f"   ⚠️ Could not load Hormozi guardrails: {e}")
        guardrails = "Use Alex Hormozi's frameworks: Overgive value first, use specific data, ethical scarcity, rival positioning."
    
    # Step 2: Load Prompt Template
    print(f"\n📝 Step 2: Loading {framework} prompt template...")
    prompt_template = load_prompt_template(framework, task_type)
    print(f"   ✅ Template loaded ({len(prompt_template)} characters)")
    
    # Step 3: Generate Content via Zernio
    print(f"\n🎨 Step 3: Generating content via Zernio...")
    zernio_client = get_zernio_client()
    
    try:
        content = zernio_client.generate(
            prompt=prompt_template,
            task_type=task_type,
            city=city,
            framework=framework,
            icp=icp
        )
        print(f"   ✅ Content generated successfully")
    except Exception as e:
        print(f"   ⚠️ Zernio generation error: {e}")
        content = {}
    
    # Save content for review
    content_file = save_generated_content(content, task_type, city)
    
    # Step 4: THE SLEEP - Mimic human review cadence
    print(f"\n⏳ Step 4: Sleep for {sleep_minutes} minutes...")
    print("   (Simulating human content review to avoid API spam flags)")
    
    # In production, this would be the actual sleep
    # For testing, we can use a shorter sleep or skip it
    if os.getenv("SKIP_SLEEP", "").lower() != "true":
        print(f"   Sleeping until: {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(sleep_minutes * 60)
    else:
        print("   ⏭️  Sleep skipped (SKIP_SLEEP=true)")
    
    # Step 5: Publish the ONE task
    print(f"\n📤 Step 5: Publishing to {task_type}...")
    
    publish_results = {}
    
    if task_type == "wp_blog":
        print("   Publishing WordPress blog...")
        wp_client = get_wordpress_client()
        content["city"] = city
        content["framework"] = framework
        result = wp_client.publish_blog(content)
        publish_results["wordpress"] = result
        
    elif task_type == "ig_carousel":
        print("   Generating Instagram carousel images...")
        # Generate images using free Pillow library
        img_gen = get_image_generator()
        
        # Prepare carousel content for image generation
        carousel_content = {
            "hook": "STOP THE LEAD LEAK",
            "subtext": f"For Top 1% {city} Agents",
            "timeline": {
                "3:00 AM": "Hot Zillow lead",
                "3:05 AM": "You're asleep",
                "3:10 AM": "Rival responds",
                "9:00 AM": "Already found agent"
            },
            "stats": [
                {"value": "5 MIN", "label": "Average lead goes cold"},
                {"value": "391%", "label": "More likely to convert (<60 sec)"},
                {"value": "$667/DAY", "label": "You're leaving on the table"}
            ],
            "you_vs_rival": {
                "you": "Checking email\nat 9 AM",
                "rival": "Auto-responder\nfires instantly"
            },
            "cta": "DM 'LEAK'",
            "scarcity": "Only 3 reports this week"
        }
        
        # Generate the image slides
        slides = img_gen.generate_carousel(carousel_content, city)
        print(f"   ✅ Generated {len(slides)} slides")
        
        # Add slides to content for publishing
        content["slides"] = slides
        content["city"] = city
        content["framework"] = framework
        
        # Publish to Instagram (demo mode without real API)
        meta_client = get_meta_client()
        result = meta_client.publish_ig_carousel(content)
        publish_results["instagram"] = result
        
    elif task_type == "threads_thread":
        print("   Publishing Threads thread...")
        meta_client = get_meta_client()
        content["city"] = city
        content["framework"] = framework
        result = meta_client.publish_threads_post(content)
        publish_results["threads"] = result
    
    # Print publish summary
    print("\n📊 Publish Summary:")
    for platform, result in publish_results.items():
        status = result.get("status", "unknown")
        print(f"   • {platform}: {status}")
        if status == "success":
            print(f"     URL: {result.get('url', result.get('post_id', 'N/A'))}")
    
    # Step 6: Log completion
    print("\n" + "=" * 60)
    print("✅ TASK COMPLETE")
    print("=" * 60)
    print(f"   • Content: {content_file}")
    print(f"   • Platform: {task_type}")
    print(f"   • City: {city}")
    print(f"   • Framework: {framework}")
    print("\n🛏️ Container shutting down...")
    
    # Exit cleanly for Docker
    sys.exit(0)


if __name__ == "__main__":
    main()

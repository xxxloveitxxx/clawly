# WordPress Blog Post Prompt

## Task
Generate a long-form blog post for WordPress targeting data-wary real estate agents.

---

## Input Parameters
- **City:** {CITY}
- **Framework:** {FRAMEWORK} (magic_headline | salty_pretzel | big_fast_value)
- **Target ICP:** data_wary_shark

---

## Blog Post Structure

### Title Options
- "The $20k Commission You're Losing Every Month (And How to Stop It)"
- "I Tracked 50 Listings in {CITY} for 30 Days. Here's What I Found."
- "Why Your Real Estate Leads Are Going Cold (And the 60-Second Fix)"
- "The Math Behind Every Missed Real Estate Commission"

### Meta Description
"Discover why 90% of real estate leads go cold before you can respond, and how tracking lead decay revealed the $20k monthly leak most agents miss."

### Introduction (200 words)
- Hook: "You're not short on leads. You're short on speed."
- Credibility: "I tracked 50 listings in {CITY} for 30 days"
- Promise: "By the end of this post, you'll know exactly where YOUR leads are going cold"

### Section 1: The Problem (400 words)
**Headline:** "The 3 AM Real Estate Nightmare"

- Timeline of a missed lead
- The $20k commission that got away
- Why speed matters more than ever
- The contradiction: More leads, less conversions

### Section 2: The Data (500 words)
**Headline:** "What 500+ Tracked Leads Revealed"

- Average lead response time in real estate
- The 5-minute window
- 391% conversion boost stat (with source)
- The decay curve visualization

### Section 3: The Rival Effect (300 words)
**Headline:** "Your Competitor Isn't Smarter. They're Faster."

- Who is winning in your market
- Why it's not about skill, it's about systems
- The auto-responder advantage
- How to compete without being awake 24/7

### Section 4: The Salty Pretzel (400 words)
**Headline:** "The Narrow Problem vs. The Big Problem"

- Narrow: "I don't know where my leads are leaking"
- BIG: "Even if I knew, I can't respond 24/7"
- Why solving the narrow problem reveals the BIG problem
- The bridge to automation

### Section 5: The Solution (500 words)
**Headline:** "How to Stop the Lead Leak"

- Step 1: Identify the leak (Custom Lead-Leak Report)
- Step 2: Plug the leak (Automated response systems)
- Step 3: Optimize for speed (ReplyzeAI integration)
- The 60-second response rule

### Section 6: The Offer (200 words)
**Headline:** "Get Your Free Lead-Leak Analysis"

- What the report includes
- Why it's free (and why limited)
- How to claim your spot
- Ethical scarcity: "Only 3 reports this week"

### Conclusion (150 words)
- Recap the main points
- The choice: Keep losing or start tracking
- Call to action
- Link to claim report

---

## SEO Elements

### Keywords
- real estate lead response
- lead conversion rate real estate
- missed real estate commission
- automated lead response
- real estate CRM response time

### Internal Links
- Link to ReplyzeAI homepage
- Link to case studies (if available)

### External Links
- Zillow research (391% stat source)
- Real estate industry benchmarks

---

## Technical Requirements

### WordPress REST API
- Endpoint: {WP_URL}/wp-json/wp/v2/posts
- Authentication: Application Password
- Format: JSON

### Post Fields
```json
{
  "title": "Post Title",
  "content": "Full HTML content",
  "status": "draft",
  "categories": [1, 5],
  "tags": ["lead-generation", "real-estate", "automation"],
  "meta": {
    "city": "{CITY}",
    "framework": "{FRAMEWORK}"
  }
}
```

### Featured Image
- Generate or specify placeholder
- Alt text: "Lead leak analysis for {CITY} real estate agents"

---

## Hormozi Guardrails Applied

1. **Proof over promises** - Cite data, use case studies
2. **"How I" not "How To"** - First-person results
3. **The narrow to BIG bridge** - Don't sell in the first post
4. **Single CTA** - Get the report, not multiple actions
5. **Respect the ICP** - Data-driven, sophisticated audience

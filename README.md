# Hermes Agent - Real Estate Content Automation

A dual-agent GitHub Actions system that generates high-conversion content for ReplyzeAI, targeting data-wary real estate agents using Alex Hormozi's marketing frameworks.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent A - Orchestrator                    │
│  • Scheduled (9 AM EST weekdays)                          │
│  • Triggers one task per day                               │
│  • Rotates through task types, cities, frameworks          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ workflow_dispatch
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent B - Executor                        │
│  • Runs Docker container                                   │
│  • One task per trigger                                    │
│  • Query Hormozi guardrails (RAG)                         │
│  • Generate content via Zernio                             │
│  • Sleep (mimic human cadence)                             │
│  • Publish to WordPress/Instagram/Threads                 │
└─────────────────────────────────────────────────────────────┘
```

## Workflows

### Agent A - Orchestrator
- **Trigger**: Scheduled (cron: `0 14 * * 1-5`) or manual
- **Duty**: Determines today's task and triggers Agent B
- **Rotation**: 
  - Monday: Threads thread (Austin, salty_pretzel)
  - Tuesday: IG carousel (Miami, magic_headline)
  - Wednesday: WordPress blog (Denver, big_fast_value)
  - Thursday: Threads thread (Phoenix, salty_pretzel)
  - Friday: IG carousel (Seattle, big_fast_value)

### Agent B - Executor
- **Trigger**: Called by Agent A
- **Duty**: Execute one content generation task
- **Process**:
  1. Query Hormozi guardrails from vector DB
  2. Load prompt template (M.A.G.I.C., Salty Pretzel, or Big Fast Value)
  3. Generate content via Zernio
  4. Sleep (30 minutes default - mimics human review)
  5. Publish to target platform
  6. Exit cleanly

## Content Frameworks

### M.A.G.I.C. Headline
- **M**agnet: "Manual Lead-Flow Audit"
- **A**vatar: "For Top 1% {City} Agents"
- **G**oal: "Capture the $20k Missed Commission"
- **I**nterval: "From the Last 30 Days"

### Salty Pretzel
- Solve narrow problem (identifying leak) → reveal BIG problem (responding 24/7)
- Timeline: 3 AM inquiry → 9 AM "found another agent"

### Big Fast Value
- Over-give before asking
- "How I" vs "How To" framework
- The 391% stat (Zillow research)

## Content Types

| Type | Platform | Key Features |
|------|----------|--------------|
| `wp_blog` | WordPress | 1500-2000 words, SEO optimized, draft for review |
| `ig_carousel` | Instagram | 5-7 slides, 1080x1350, high-contrast design |
| `threads_thread` | Threads | 5-10 posts, text-first, math-focused |

## Setup

### 1. Add Secrets to GitHub

| Secret | Description |
|--------|-------------|
| `PAT_TOKEN` | Fine-grained PAT with workflow permissions |
| `WP_APP_PASSWORD` | WordPress Application Password |
| `ZERNIO_API_KEY` | Zernio API key for content generation |
| `META_ACCESS_TOKEN` | Meta/Facebook API access token |

### 2. Add Hormozi Books (Optional)

Place PDF copies of Alex Hormozi's books in `hormozi_books/`. They will be indexed into a vector database for RAG-based guardrails.

### 3. Configure WordPress

WordPress site must have:
- REST API enabled
- Application Passwords enabled
- User: `hermes_agent` with contributor+ role

### 4. Run Manually

```bash
gh workflow run executor.yml \
  -f task_type="threads_thread" \
  -f framework="salty_pretzel" \
  -f city="Austin" \
  -f target_icp="data_wary_shark"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TASK_TYPE` | threads_thread | Content type |
| `FRAMEWORK` | salty_pretzel | Content framework |
| `CITY` | Austin | Target city |
| `TARGET_ICP` | data_wary_shark | ICP identifier |
| `SLEEP_MINUTES` | 30 | Human cadence delay |
| `SKIP_SLEEP` | false | Skip sleep for testing |
| `WP_URL` | https://replyzeai.com | WordPress site |
| `WP_USER` | hermes_agent | WordPress user |

## Directory Structure

```
├── app/
│   ├── executor.py          # Main agent logic
│   ├── rag_engine.py        # Hormozi RAG queries
│   ├── build_db.py          # Vector DB builder
│   └── clients/
│       ├── zernio_client.py # Zernio API
│       ├── wp_client.py     # WordPress REST API
│       └── meta_client.py   # Instagram/Threads API
├── prompts/
│   ├── magic_headline.md    # M.A.G.I.C. framework
│   ├── salty_pretzel.md     # Salty Pretzel framework
│   ├── big_fast_value.md    # Big Fast Value framework
│   ├── icp_guardrails.md    # ICP-specific rules
│   ├── ig_carousel.md       # IG content template
│   ├── threads_thread.md    # Threads content template
│   └── wp_blog.md           # Blog content template
├── dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
└── .github/workflows/
    ├── orchestrator.yml     # Agent A
    └── executor.yml         # Agent B
```

## The 3% Reply Rate Strategy

Based on Alex Hormozi's principles:

1. **Over-give value first** - 4 value posts per 1 ask (IG), 10:1 ratio (Threads)
2. **Single CTA** - Never ask for multiple actions
3. **Ethical scarcity** - "Only 3 reports this week because tracking is manual"
4. **Rival positioning** - "Your competitor is closing deals you're missing"
5. **Proof over promises** - Use the 391% stat, cite sources
6. **Narrow → BIG bridge** - Don't sell software in first touch

## Target ICP: Data-Wary Real Estate Sharks

- Top 1% real estate agents
- Data-driven decision makers
- Care about ROI, conversion rates, competitor analysis
- Want systems over effort
- Respond to proof, not promises

## License

MIT

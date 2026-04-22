# Search Sources & Queries for Claude Skill Research

Use this reference during Research Mode (Step 2). Run at least 6–8 searches per run, rotating through the queries below. Vary phrasing slightly each run (e.g. swap year, add "new", change order) to avoid getting cached results.

---

## Official / Anthropic Sources

These sources are highest relevance. Always include at least 2–3 official source searches per run.

| Query | Notes |
|---|---|
| `site:docs.anthropic.com skills tutorial` | Official skill documentation |
| `site:docs.anthropic.com claude code skill` | Claude Code skill guides |
| `site:github.com/anthropics claude skill` | Anthropic's own GitHub repos |
| `anthropic claude skill SKILL.md 2025 OR 2026` | Dated official tutorials |
| `anthropic claude agent SDK tool use tutorial` | Agent SDK patterns |
| `site:docs.anthropic.com "tool use" tutorial` | Tool use patterns useful for skills |

---

## GitHub Community Sources

| Query | Notes |
|---|---|
| `"SKILL.md" claude code github` | Community skills shared on GitHub |
| `claude code custom skill github tutorial` | User-written skill tutorials |
| `claude cowork skill example github` | Cowork-specific examples |
| `site:github.com "claude_skill" OR "claude-skill" tutorial` | Skill examples by name |
| `github claude code plugin skill example` | Plugin + skill combos |
| `github "claude code" skill ".md" site:github.com` | Raw skill files |

---

## Community Blogs & Dev Sites

| Query | Notes |
|---|---|
| `how to create claude code skill tutorial 2025 OR 2026` | General tutorials |
| `claude code skills guide walkthrough` | Step-by-step guides |
| `building claude agent skills best practices` | Best practices articles |
| `site:dev.to claude skill OR claude code` | Dev.to articles |
| `site:medium.com claude code skill tutorial` | Medium articles |
| `site:hashnode.com claude skill` | Hashnode posts |
| `site:substack.com claude code skills` | Substack newsletters |

---

## Reddit / Forums

| Query | Notes |
|---|---|
| `site:reddit.com/r/ClaudeAI claude skill tutorial` | Reddit discussions |
| `site:reddit.com claude code skill how to` | How-to threads |
| `site:reddit.com "claude code" "skill" created` | User-shared skills |
| `site:news.ycombinator.com claude code skill` | HN threads |

---

## YouTube / Video Tutorials

| Query | Notes |
|---|---|
| `youtube claude code skill tutorial 2025 OR 2026` | Video tutorials |
| `youtube "claude cowork" skill demo` | Cowork demos |
| `youtube anthropic claude agent skill build` | Build-along videos |

---

## Trusted Domains (prioritize results from these)

When multiple results appear, prioritize in this order:

1. `docs.anthropic.com`
2. `github.com/anthropics`
3. `github.com` (community repos with stars > 50)
4. `dev.to`, `medium.com`, `hashnode.com` (quality dev blogs)
5. `reddit.com/r/ClaudeAI`, `reddit.com/r/ClaudeCode`
6. `youtube.com` (video tutorials — extract transcript if possible)
7. Personal blogs and Substack

---

## Relevance Scoring Guide

Use this when assigning the 1–5 relevance score in the report:

| Score | Meaning |
|---|---|
| 5 | Directly teaches how to create or improve a Claude skill (SKILL.md, skill structure, skill patterns) |
| 4 | Covers Claude Code / Claude Agent SDK patterns that could be wrapped into a skill |
| 3 | Covers tool use, prompt engineering, or MCP concepts useful for skill authors |
| 2 | General Claude tutorial with some actionable patterns |
| 1 | Tangentially related (general AI, general coding) — include only if genuinely novel |

Only include score 1 items if the fetch turns up nothing better. Focus on 4–5 items for the report.

---

## Skill Type Classification

When noting "Skill type potential" in the report, use these categories (can pick multiple):

- **Document generation** — creates docx, PDF, pptx, etc.
- **Data processing** — transforms CSV, Excel, JSON, SQL
- **Web research** — searches and summarizes web content
- **Code generation** — generates code in specific languages or frameworks
- **API integration** — connects to external APIs/services
- **Automation** — repeatable workflows, schedulable tasks
- **Communication** — drafts emails, messages, reports
- **File management** — organizes, renames, converts files
- **AI/agent pattern** — implements an agentic loop or multi-step reasoning pattern
- **Dev tools** — git, CI/CD, code review, testing helpers

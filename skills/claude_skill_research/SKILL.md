---
name: claude_skill_research
description: Automatically research new Claude skill tutorials from the web, save findings, and draft new skills from approved research. Use this skill when the user says "research new Claude skills", "find skill tutorials", "run skill research", "check for new skills", "search for Claude skill ideas", "scan for Claude skill tutorials", or any variation of discovering and preparing new Claude skills. Also trigger when the user approves a research item and wants a draft, e.g. "convert tutorial 2 into a skill", "draft skill from report", "build skill from research", "install draft skill". This skill can also be run on a schedule — trigger when resuming a scheduled skill research run.
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

# Claude Skill Research

A skill for automatically discovering new Claude skill tutorials, saving research reports, avoiding duplicate searches, and drafting new skills from approved research.

## Paths (always use these exact paths)

| Resource | Path |
|---|---|
| Seen log | `claude_cowork/skill_research/seen_log.json` (on user's disk) |
| Research reports | `claude_cowork/skill_research/report_YYYY-MM-DD_N.md` |
| Draft skills staging | `claude_cowork/skill_research/drafts/<skill-name>/SKILL.md` |
| User skills folder | `claude_cowork/skills/<skill-name>/` |
| Search sources ref | (see `references/search_sources.md` in this skill folder) |

When referencing absolute paths in the shell, the workspace mounts at:
`/sessions/tender-sweet-dijkstra/mnt/claude_cowork/`

---

## Two Modes

### Mode 1 — Research Mode (default)
Triggered by: "run skill research", "find new skill tutorials", "search for Claude skills", or a scheduled run.

### Mode 2 — Draft Mode
Triggered by: "convert tutorial N from report X into a draft skill", "draft skill from report", "build skill from research item N".

### Mode 3 — Install Mode
Triggered by: "install draft <skill-name>", "move draft <skill-name> to skills folder".

---

## Mode 1: Research Mode

### Step 1 — Load the Seen Log

Read the file at the absolute path:
`/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/seen_log.json`

If the file does not exist, initialize it as:
```json
{
  "last_run": null,
  "seen_urls": []
}
```
and save it before proceeding.

The seen log format:
```json
{
  "last_run": "2026-04-22T10:00:00",
  "seen_urls": [
    {
      "url": "https://example.com/tutorial",
      "title": "Tutorial title",
      "date_seen": "2026-04-22",
      "report_file": "report_2026-04-22_1.md"
    }
  ]
}
```

Extract the list of already-seen URLs into memory.

### Step 2 — Web Search

Read `references/search_sources.md` (in this skill folder) for the full list of queries and trusted sources. Run at least 6-8 searches, rotating through the queries listed there. Collect all URLs from results.

Vary the queries slightly each run (add the current year, swap phrasing) to surface fresh content.

### Step 3 — Filter Duplicates

Compare every collected URL against the `seen_urls` list. Discard any URL already present.

If ALL collected URLs are already seen, report to the user:
> "No new tutorials found since last run on [last_run date]. Try again later or broaden the search."
Then stop.

### Step 4 — Fetch and Summarize (up to 5 new URLs per run)

For each new URL (cap at 5 to keep reports focused):
- Use WebFetch to retrieve the page
- Extract: title, author/source, publish date, main concepts, code examples, key techniques
- Assess difficulty level: beginner / intermediate / advanced
- Rate relevance to skill creation on 1–5 (5 = directly about building Claude skills)
- Note the skill type it could produce (automation, research, document creation, API integration, etc.)

If WebFetch fails for a URL, note "fetch failed" in the report but still add it to seen_urls so it isn't retried endlessly.

### Step 5 — Save Research Report

Determine the report filename: `report_YYYY-MM-DD_N.md` where N increments if multiple reports exist for the same day. Save to:
`/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/`

Use this exact report template:

```markdown
# Skill Research Report — YYYY-MM-DD (Run N)

**Run date:** [ISO datetime]
**New tutorials found:** [count]
**Skipped (already seen):** [count]
**Sources searched:** [comma-separated list of domains]

---

## Tutorial [N] — [Title]

**URL:** [url]
**Source type:** official / github / reddit / blog / youtube / other
**Difficulty:** beginner / intermediate / advanced
**Relevance score:** [1–5] — [one-line reason]
**Skill type potential:** [e.g. document generation, API integration, automation]

### Summary
[2–4 paragraphs covering what the tutorial teaches, why it's interesting, and what makes it novel or useful]

### Key techniques / patterns
- [technique or pattern 1]
- [technique or pattern 2]
- [technique or pattern 3]

### Skill potential
[Concrete description: what would the resulting skill do? What would trigger it? What would it produce?]

### Notable snippets / quotes
[1–3 key code or text excerpts that capture the tutorial's core contribution]

---

## Tutorial [N+1] — [Title]
[repeat structure above]

---

## ✅ Next Steps

Review this report and tell Claude which tutorial(s) to convert into a draft skill:

> "Convert tutorial [N] from report [filename] into a draft skill"

Or to convert multiple:

> "Convert tutorials 1 and 3 from report [filename] into draft skills"
```

### Step 6 — Update Seen Log

Add ALL URLs fetched in this run (successful or failed) to `seen_urls`. Also add any URLs that were collected but skipped due to the 5-per-run cap — mark them as `"skipped": true` in the entry so they can be prioritized next run.

Update `last_run` to the current ISO datetime. Save the updated `seen_log.json`.

### Step 7 — Report to User

Tell the user:
- How many new tutorials were found and summarized
- How many were skipped (already seen)
- Link to the report file: `computer:///sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/[filename]`
- Remind them to say "Convert tutorial N from report [filename] into a draft skill" to proceed

---

## Mode 2: Draft Mode

Triggered when user says e.g. "convert tutorial 2 from report 2026-04-22_1.md into a draft skill".

### Step 1 — Load the Specified Report

Read the report file from:
`/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/[filename]`

Identify the requested tutorial section (by number or title).

### Step 2 — Propose a Skill Name

Based on what the tutorial teaches, propose a kebab-case skill name (e.g. `api-data-fetcher`, `csv-transformer`, `email-formatter`). Confirm with the user if unsure.

### Step 3 — Draft the SKILL.md

Build a complete draft skill using the standard anatomy:
```
claude_cowork/skill_research/drafts/<skill-name>/
└── SKILL.md
```

The draft SKILL.md must include:
- **name**: the proposed skill name
- **description**: triggering phrases and use-case coverage — make it "pushy" so it triggers reliably
- **Full workflow**: step-by-step instructions based on what the tutorial taught
- **Scripts/references stubs**: if the skill needs helper scripts or reference files, create placeholder files with `# TODO:` comments
- **Comments**: mark any sections needing Pratul's input with `# NEEDS REVIEW:` comments

For your reference, the skill anatomy is:
```
<skill-name>/
├── SKILL.md            ← required, instructions for Claude
├── scripts/            ← optional, Python/JS helpers
├── references/         ← optional, docs loaded on demand
└── assets/             ← optional, templates, fonts, icons
```

### Step 4 — Present the Draft

- Show the full SKILL.md content inline in the conversation
- Provide a link: `computer:///sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/drafts/<skill-name>/SKILL.md`
- Ask: "Does this look good? Say **'install draft <skill-name>'** to move it into your skills folder, or give me feedback to revise it."

---

## Mode 3: Install Mode

Triggered when user says "install draft <skill-name>".

### Step 1 — Verify the Draft Exists

Check that `/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/drafts/<skill-name>/SKILL.md` exists.

### Step 2 — Copy to Skills Folder

```bash
cp -r /sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/drafts/<skill-name> \
      /sessions/tender-sweet-dijkstra/mnt/claude_cowork/skills/<skill-name>
```

### Step 3 — Confirm

Tell the user:
> "✅ Skill **<skill-name>** has been installed to your skills folder. It will be available in your next Cowork session. You can find it at: `computer:///sessions/tender-sweet-dijkstra/mnt/claude_cowork/skills/<skill-name>/SKILL.md`"

---

## Scheduling This Skill

When the user wants to schedule this skill, use the `schedule` skill. The self-contained task prompt to use is:

> Run the claude_skill_research skill in Research Mode:
> 1. Read the seen log from `/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/seen_log.json` (initialize it as `{"last_run": null, "seen_urls": []}` if missing).
> 2. Search the web for new Claude skill tutorials from both official Anthropic sources (docs.anthropic.com, github.com/anthropics) and community sources (GitHub, Reddit, dev blogs, YouTube).
> 3. Filter out any URLs already present in the seen log.
> 4. Fetch and summarize up to 5 new tutorials.
> 5. Save a research report to `/sessions/tender-sweet-dijkstra/mnt/claude_cowork/skill_research/report_YYYY-MM-DD_N.md`.
> 6. Update the seen log with all newly processed URLs and set `last_run` to now.
> 7. Tell the user how many new tutorials were found and link to the report.

Suggested default schedule: **every Monday at 9am** (`0 9 * * 1`).

---

## Error Handling

- **WebFetch fails**: Log the URL in the report as "fetch failed", still add to seen_urls, continue with remaining URLs.
- **No new URLs found**: Report clearly, suggest the user wait before the next run.
- **Seen log is corrupted**: Back up the broken file as `seen_log.json.bak`, reinitialize as empty, log a warning.
- **Draft skill name conflict**: If a draft with the same name already exists, append `_v2`, `_v3`, etc.

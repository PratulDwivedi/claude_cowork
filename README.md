# Cowork Working Folder

Personal workspace managed via Cowork. Contains custom skills and document conversions.

## Structure

```
claude_cowork/
├── skills/                        # Custom Claude skills
│   ├── md_to_pdf/                 # Convert Markdown files → styled PDF
│   │   ├── SKILL.md
│   │   ├── requirements.txt
│   │   ├── scripts/convert.py
│   │   ├── templates/
│   │   │   ├── default.css        # Neutral theme
│   │   │   ├── branded.css        # Customizable branded theme
│   │   │   └── README.md          # Theme customization guide
│   │   └── examples/              # Sample input + rendered PDFs
│   │
│   └── claude_skill_research/     # Research new Claude skill tutorials from the web
│       ├── SKILL.md
│       ├── references/
│       │   └── search_sources.md  # Curated search queries & trusted sources
│       └── scripts/
│           └── manage_seen_log.py # Helper to manage the seen URL log
│
├── skill_research/                # Research outputs (auto-generated)
│   ├── seen_log.json              # Tracks already-processed URLs (no re-fetch)
│   ├── drafts/                    # Draft skills awaiting approval
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   └── report_YYYY-MM-DD_N.md    # Research reports (one per run)
│
└── conversions/                   # Outputs organized per document
    └── <doc-name>/
        ├── source/                # Original markdown (tracked in git)
        └── pdf/                   # Generated PDFs (ignored by git)
```

## Skills

### `md_to_pdf`
Converts Markdown (`.md`) files into styled PDF documents using WeasyPrint. Supports custom CSS themes.  
**Trigger:** "convert md to pdf", "markdown to pdf", "export this md as PDF"  
See `skills/md_to_pdf/templates/README.md` for customizing the branded theme.

### `claude_skill_research`
Automatically searches the web for new Claude skill tutorials (official Anthropic + community sources), saves research reports, avoids re-fetching already-seen URLs, and drafts new skills from approved research.

**Three modes:**
- **Research** — say "run skill research" or "find new Claude skill tutorials" → searches web, saves a report to `skill_research/`
- **Draft** — say "convert tutorial N from report YYYY-MM-DD_N.md into a draft skill" → creates a draft `SKILL.md` in `skill_research/drafts/`
- **Install** — say "install draft \<skill-name\>" → moves approved draft to `skills/` folder

**Schedule:** Available as a scheduled task (`claude-skill-research`) — run manually or set a recurring interval (e.g. every Monday at 9am) from the Cowork Scheduled section.

## Notes

- Generated PDFs are excluded from git — they're regenerable from source.
- Research reports and draft skills are auto-generated and can be regenerated; only approved/installed skills should be tracked.
- Source markdowns and skill code are tracked.

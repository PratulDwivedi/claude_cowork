# Cowork Working Folder

Personal workspace managed via Cowork. Contains custom skills and document conversions.

## Structure

```
claude_cowork/
├── skills/                  # Custom Claude skills
│   └── md_to_pdf/           # Convert Markdown files → styled PDF
│       ├── SKILL.md
│       ├── requirements.txt
│       ├── scripts/convert.py
│       ├── templates/
│       │   ├── default.css  # Neutral theme
│       │   ├── branded.css  # Customizable branded theme
│       │   └── README.md    # Theme customization guide
│       └── examples/        # Sample input + rendered PDFs
│
└── conversions/             # Outputs organized per document
    └── <doc-name>/
        ├── source/          # Original markdown (tracked in git)
        └── pdf/             # Generated PDFs (ignored by git)
```

## Notes

- Generated PDFs are excluded from git — they're regenerable from source.
- Source markdowns and skill code are tracked.
- See `skills/md_to_pdf/templates/README.md` for customizing the branded theme.

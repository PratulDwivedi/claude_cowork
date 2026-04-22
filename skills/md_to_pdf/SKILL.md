---
name: md_to_pdf
description: Convert Markdown (.md) files into styled PDF documents using WeasyPrint. Supports custom CSS themes for branded output. Use this skill when the user says "convert md to pdf", "markdown to pdf", "export this md as PDF", "render markdown as pdf", "generate PDF from markdown", or references a .md file and asks for a PDF version.
allowed-tools: Bash, Read, Write
---

# md_to_pdf

Converts Markdown files into professionally formatted PDF documents. Supports a default clean theme and custom branded CSS templates.

## When to Trigger

Use this skill when the user asks to:

- Convert a `.md` file to `.pdf`
- "Export / render / generate PDF from markdown"
- Produce a branded PDF from a markdown source
- Apply a custom CSS theme to a markdown-derived PDF

## Workflow

Follow these steps in order when invoked:

### 1. Locate the input markdown file

- If the user gave a path, use it.
- If they uploaded a file, check `/sessions/keen-gracious-gauss/mnt/uploads/`.
- If ambiguous, list `.md` files in the working folder and ask.

### 2. Determine the output path

- Default: same folder as input, same basename, `.pdf` extension.
- Save inside `claude_cowork/` so the user can access it.

### 3. Choose a CSS theme

- **Default theme** → `templates/default.css` (clean, neutral, readable)
- **Branded theme** → `templates/branded.css` (user-customizable for corporate/brand use)
- If the user mentions a brand / logo / color → use `branded.css` and ask if they want to edit it first.

### 4. Run the converter

Execute from the sandbox:

```bash
python /sessions/keen-gracious-gauss/mnt/claude_cowork/skills/md_to_pdf/scripts/convert.py \
    --input "<path to .md>" \
    --output "<path to .pdf>" \
    --css "<path to .css>"
```

The script auto-installs dependencies (`markdown`, `weasyprint`, `pygments`) on first run per session.

### 5. Deliver the result

- Share the PDF via a `computer://` link pointing at the file inside `claude_cowork/`.
- Do NOT paste the whole PDF content back; just link and summarize briefly.

## File Layout

```
md_to_pdf/
├── SKILL.md                 ← this file
├── requirements.txt         ← pip dependencies
├── scripts/
│   └── convert.py           ← main converter with auto-install bootstrap
├── templates/
│   ├── default.css          ← neutral clean theme
│   ├── branded.css          ← customizable branded template
│   └── README.md            ← how to customize a template
└── examples/
    └── sample.md            ← test file
```

## Customizing for Branding

Edit `templates/branded.css`. Key variables at the top of the file control:

- Primary brand color
- Heading font
- Body font
- Logo URL (optional)
- Page margins / footer text

See `templates/README.md` for a walkthrough.

## System Dependencies

WeasyPrint needs native libraries. The bootstrap script attempts to install them via `apt-get`. If that fails in a restricted sandbox, the script falls back to the pure-Python renderer (`xhtml2pdf`) which has lower fidelity but no system deps.

## Examples

**User says:** "convert notes.md to pdf"
→ Run with default theme, output `notes.pdf` next to the input.

**User says:** "export report.md as a branded PDF with our company colors"
→ Use `branded.css`. Ask what the primary color and logo should be, edit the template, then render.

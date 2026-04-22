# Customizing a Branded CSS Template

This folder contains the themes used by the `md_to_pdf` skill.

| File | Purpose |
|---|---|
| `default.css` | Neutral, clean theme. Don't edit — use as a starting point. |
| `branded.css` | Your customizable branded theme. Edit this file. |

## Quick customization

Almost everything you'll want to change lives in the `:root { ... }` block at the top of `branded.css`. Change these variables and the rest of the stylesheet follows automatically.

### Brand colors

```css
--brand-primary:      #0B5FFF;   /* main accent color (H1, table headers, links) */
--brand-primary-dark: #062D7A;   /* darker shade for depth */
--brand-accent:       #FF6B35;   /* secondary accent (inline code, blockquote bar) */
```

### Typography

```css
--font-body:    "Helvetica", "Arial", sans-serif;
--font-heading: "Helvetica", "Arial", sans-serif;
--font-mono:    "Consolas", "Menlo", "Monaco", monospace;
```

Want a custom font? Add an `@font-face` block above `:root` pointing at a TTF/OTF file. WeasyPrint loads local fonts.

### Page layout

```css
--page-margin-top:    25mm;
--page-margin-side:   20mm;
--page-margin-bottom: 22mm;
```

### Footer / header text

```css
--footer-text:  "Your Company  ·  Confidential";
--header-text:  "";   /* leave empty to hide header */
```

Page numbers are already wired up (`Page X of Y` in the bottom-right).

## Using it

Just point the `--css` flag at your edited file:

```bash
python scripts/convert.py \
    --input my_doc.md \
    --output my_doc.pdf \
    --css templates/branded.css
```

## Creating multiple brand themes

Duplicate `branded.css` → rename e.g. `acme.css`, `clientx.css`, `dark.css`. Tell the skill which one to use when you run it, or ask me to switch themes.

## Adding a logo in the header

In `branded.css`, change the `@top-left` block:

```css
@top-left {
    content: url("/absolute/path/to/logo.png");
    margin-top: 5mm;
}
```

The path must be absolute inside the sandbox (e.g. `/sessions/keen-gracious-gauss/mnt/claude_cowork/assets/logo.png`).

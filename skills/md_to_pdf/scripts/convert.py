#!/usr/bin/env python3
"""
md_to_pdf — convert a Markdown file into a styled PDF.

Usage:
    python convert.py --input path/to/file.md \
                      --output path/to/file.pdf \
                      [--css path/to/theme.css]

- Auto-installs required Python packages on first run in a fresh sandbox.
- Uses WeasyPrint (preferred) for high-fidelity output.
- Falls back to xhtml2pdf if WeasyPrint cannot load (e.g. missing system libs).
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: install Python deps if missing
# ---------------------------------------------------------------------------

REQUIRED_PKGS = ["markdown", "weasyprint", "pygments", "xhtml2pdf"]


def ensure_python_deps() -> None:
    missing = [p for p in REQUIRED_PKGS if importlib.util.find_spec(p) is None]
    if not missing:
        return
    print(f"[bootstrap] Installing Python packages: {', '.join(missing)}", flush=True)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", *missing]
    )


def try_install_system_deps() -> None:
    """Best-effort install of WeasyPrint's native deps. Ignored on failure."""
    pkgs = [
        "libpango-1.0-0",
        "libpangoft2-1.0-0",
        "libharfbuzz0b",
        "libcairo2",
        "libgdk-pixbuf-2.0-0",
    ]
    try:
        subprocess.run(
            ["apt-get", "install", "-y", "-q", *pkgs],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
        )
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def render_html(md_text: str, css_text: str, title: str) -> str:
    import markdown

    html_body = markdown.markdown(
        md_text,
        extensions=[
            "extra",          # tables, fenced code, attr_list, footnotes, etc.
            "sane_lists",
            "toc",
            "codehilite",
            "admonition",
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "noclasses": False},
        },
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css_text}
</style>
</head>
<body>
<main class="document">
{html_body}
</main>
</body>
</html>
"""


def html_to_pdf_weasyprint(html: str, output_path: Path) -> bool:
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(str(output_path))
        return True
    except Exception as e:
        print(f"[weasyprint] failed: {e}", flush=True)
        return False


def html_to_pdf_xhtml2pdf(html: str, output_path: Path) -> bool:
    try:
        from xhtml2pdf import pisa
        with open(output_path, "wb") as f:
            result = pisa.CreatePDF(src=html, dest=f)
        return not result.err
    except Exception as e:
        print(f"[xhtml2pdf] failed: {e}", flush=True)
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown → PDF")
    parser.add_argument("--input", required=True, help="Path to .md file")
    parser.add_argument("--output", required=True, help="Path to output .pdf")
    parser.add_argument(
        "--css",
        default=None,
        help="Path to CSS file. Defaults to templates/default.css next to this script.",
    )
    args = parser.parse_args()

    ensure_python_deps()
    try_install_system_deps()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2

    # Resolve CSS
    script_dir = Path(__file__).resolve().parent
    default_css = script_dir.parent / "templates" / "default.css"
    css_path = Path(args.css).expanduser().resolve() if args.css else default_css
    if not css_path.exists():
        print(f"ERROR: CSS file not found: {css_path}", file=sys.stderr)
        return 2

    # Read
    md_text = input_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")
    title = input_path.stem

    # Build HTML + render
    html = render_html(md_text, css_text, title)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[convert] {input_path.name} -> {output_path.name} (css: {css_path.name})", flush=True)

    if html_to_pdf_weasyprint(html, output_path):
        print(f"[done] wrote {output_path}  (engine: weasyprint)")
        return 0

    print("[fallback] trying xhtml2pdf ...", flush=True)
    if html_to_pdf_xhtml2pdf(html, output_path):
        print(f"[done] wrote {output_path}  (engine: xhtml2pdf)")
        return 0

    print("ERROR: both PDF engines failed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

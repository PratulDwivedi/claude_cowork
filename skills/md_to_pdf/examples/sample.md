# md_to_pdf — Sample Document

This is a test file used to verify that the `md_to_pdf` skill is rendering correctly.

## Overview

The skill converts Markdown into styled PDFs using **WeasyPrint** (with a fallback to **xhtml2pdf**). You can pick between a neutral default theme and a customizable branded theme.

## Text elements

Paragraphs render with comfortable line height. You can use **bold**, *italic*, and [links](https://example.com) inline. Inline `code snippets` are highlighted.

> Blockquotes get a colored left border and a subtle background tint.

## Lists

Unordered:

- First item
- Second item with a longer piece of text to confirm wrapping behavior across lines
- Third item

Ordered:

1. Step one
2. Step two
3. Step three

## Code block

```python
def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

print(greet("Pratul"))
```

```typescript
interface User {
  id: string;
  name: string;
}

export const getUser = async (id: string): Promise<User> => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
};
```

## Table

| Feature          | Default theme | Branded theme |
|------------------|---------------|---------------|
| Page numbers     | Yes           | Yes           |
| Custom colors    | No            | Yes           |
| Custom footer    | No            | Yes           |
| Logo in header   | No            | Yes (optional)|

## Horizontal rule

---

## Conclusion

If this page renders cleanly, the skill is working. Edit `templates/branded.css` to match your brand.

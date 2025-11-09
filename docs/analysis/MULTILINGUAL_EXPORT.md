# Multilingual Export System

This document explains how to use the multilingual export system for the article.

## Overview

The article uses HTML comment markers to separate English and Italian content:

```markdown
<!-- lang:en -->
English text here
<!-- /lang:en -->

<!-- lang:it -->
Testo italiano qui
<!-- /lang:it -->
```

## Usage

### Export in English only

```bash
make pdf-en
# or
make docx-en
# or
make html-en
```

### Export in Italian only

```bash
make pdf-it
# or
make docx-it
# or
make html-it
```

### Export bilingual (both languages)

```bash
make pdf-both
# or
make docx-both
# or
make html-both
# or simply
make pdf    # defaults to bilingual
make docx   # defaults to bilingual
make html   # defaults to bilingual
```

## How it works

1. The `filters/language_filter.lua` Pandoc filter reads the `lang` metadata variable
2. It filters out content based on the HTML comment markers
3. The Makefile provides convenient targets for each language combination

## Filter Details

The Lua filter:
- Removes `<!-- lang:XX -->` comment markers from the output
- When `lang=en`, only keeps content between `<!-- lang:en -->` markers
- When `lang=it`, only keeps content between `<!-- lang:it -->` markers  
- When `lang=both` (or unspecified), keeps all content

## Adding Language Markers Manually

For new bilingual content, use this pattern:

```markdown
<!-- lang:en -->
Your English paragraph here.
<!-- /lang:en -->

<!-- lang:it -->
Il tuo paragrafo italiano qui.
<!-- /lang:it -->
```

## Automated Marker Addition

Use the script to convert existing bilingual content with italic Italian:

```bash
python scripts/language/add_language_markers.py bridging-the-gap-article-draft.md article_marked.md
```

This converts:
```markdown
English text.

*Testo italiano.*
```

Into:
```markdown
<!-- lang:en -->
English text.
<!-- /lang:en -->

<!-- lang:it -->
Testo italiano.
<!-- /lang:it -->
```

## Testing

Test that the filter works correctly:

```bash
# Test English export
pandoc bridging-the-gap-article-draft.md -L filters/language_filter.lua -M lang=en -t plain | head -50

# Test Italian export  
pandoc bridging-the-gap-article-draft.md -L filters/language_filter.lua -M lang=it -t plain | head -50

# Test bilingual export
pandoc bridging-the-gap-article-draft.md -L filters/language_filter.lua -M lang=both -t plain | head -50
```

## Makefile Targets

The following targets are available:

- `make pdf-en` - English PDF
- `make pdf-it` - Italian PDF
- `make pdf-both` - Bilingual PDF
- `make docx-en` - English DOCX
- `make docx-it` - Italian DOCX
- `make docx-both` - Bilingual DOCX
- `make html-en` - English HTML
- `make html-it` - Italian HTML
- `make html-both` - Bilingual HTML

Default targets (without language suffix) produce bilingual output.

# Article Conversion Documentation

> **Note**: This project now uses a new organized structure. See [../README.md](../README.md) for the complete overview.

## Quick Links

- **[CONVERSION_GUIDE.md](CONVERSION_GUIDE.md)** - Quick start guide for all conversions
- **[README_LATEX.md](README_LATEX.md)** - Complete LaTeX conversion documentation
- **[QUICK_START_LATEX.md](QUICK_START_LATEX.md)** - 3-command quick start

## New Project Structure

The project has been reorganized:

```
articolo/
├── bridging-the-gap-article-draft.md              ← Main article (Markdown)
├── scripts/                      ← Conversion scripts
│   ├── md_to_latex.py           ← Markdown → LaTeX
│   ├── convert_to_pdf.py        ← Legacy PDF converter
│   └── ris_to_bibtex.py         ← RIS → BibTeX
├── templates/                    ← LaTeX templates
│   └── template_latex.tex
├── references/                   ← Bibliography
│   ├── references.bib
│   └── apa.csl
├── assets/figures/published/                ← Images
└── output/                       ← Generated files
    ├── latex/
    ├── pdf/
    └── word/
```

## Conversion Methods

### Recommended: Markdown → LaTeX → PDF

```bash
# 1. Convert to LaTeX with custom template
make latex

# 2. Compile to PDF
cd output/latex
pdflatex article_draft.tex
```

**Advantages**:
- Full control over preambolo
- Custom LaTeX template
- Professional typography
- BibTeX/BibLaTeX support

### Alternative: Direct PDF

```bash
# One-step conversion
make pdf
```

**Advantages**:
- Quick and simple
- Good for previews

### Alternative: Word/HTML

```bash
make docx    # Microsoft Word
make html    # Web HTML
```

## Scripts Location

All conversion scripts are now in `scripts/`:

- **`scripts/conversion/md_to_latex.py`** - Main conversion tool (Markdown → LaTeX)
- **`scripts/legacy/convert_to_pdf.py`** - Legacy direct PDF converter
- **`scripts/legacy/convert_to_pdf.sh`** - Legacy bash script
- **`scripts/conversion/ris_to_bibtex.py`** - Bibliography converter

## File Paths

All paths have been updated:

| Old Path | New Path |
|----------|----------|
| `references.bib` | `references/references.bib` |
| `apa.csl` | `references/apa.csl` |
| `template_latex.tex` | `templates/template_latex.tex` |
| `article_draft.pdf` | `output/pdf/article_draft.pdf` |
| `article_draft.tex` | `output/latex/article_draft.tex` |
| Images | `assets/figures/published/` |

## Prerequisites

Install dependencies:

```bash
# Using Make
make install-deps

# Or manually
sudo apt-get install pandoc texlive-full python3
```

Verify:

```bash
make check-deps
```

## Detailed Documentation

For complete instructions, see:

1. **[CONVERSION_GUIDE.md](CONVERSION_GUIDE.md)** - Quick reference
2. **[README_LATEX.md](README_LATEX.md)** - LaTeX details
3. **[QUICK_START_LATEX.md](QUICK_START_LATEX.md)** - 3-step guide
4. **[../README.md](../README.md)** - Main project README

## Workflow

```bash
# 1. Edit article
nano bridging-the-gap-article-draft.md

# 2. Convert
make latex

# 3. Compile
cd output/latex && pdflatex article_draft.tex

# 4. View
xdg-open article_draft.pdf
```

## Getting Help

```bash
make help                              # Makefile commands
python3 scripts/conversion/md_to_latex.py --help  # Script options
```

---

**Last updated**: 2025-10-18 (Project reorganization v2.0)

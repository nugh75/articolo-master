# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Progetto Articolo: AI in Education** - A scientific article conversion and management system for converting Markdown to LaTeX/PDF with full bibliography support. The article analyzes trust, competence gaps, and ethical tensions in AI integration in education (716-line research paper, 66 KB).

**Version:** 2.0 (Reorganized structure, October 2025)

## Core Architecture

### Three-Tier Conversion Pipeline

1. **Recommended Route (LaTeX + Template)**
   ```
   bridging-the-gap-article-draft.md → md_to_latex.py + template → output/latex/*.tex → pdflatex → PDF
   ```
   - Uses custom `templates/template_latex.tex` with full preambolo control
   - Command: `make latex`
   - Most flexible, best for academic publishing

2. **Direct PDF (Legacy)**
   ```
   bridging-the-gap-article-draft.md → Pandoc direct → output/pdf/*.pdf
   ```
   - Command: `make pdf`
   - Quick previews, less customization

3. **Alternative Formats**
   - HTML: `make html` (MathJax support)
   - DOCX: `make docx` (Word/collaboration)

### Directory Structure (v2.0)

```
/
├── bridging-the-gap-article-draft.md              # PRIMARY SOURCE (edit this!)
├── Makefile                      # Build orchestration (184 lines)
│
├── scripts/                      # Conversion tools
│   ├── md_to_latex.py           # Main converter (268 lines)
│   ├── convert_to_pdf.py        # Legacy direct converter
│   └── ris_to_bibtex.py         # Bibliography converter (224 lines)
│
├── templates/
│   └── template_latex.tex       # Custom LaTeX preambolo (120+ lines)
│
├── references/
│   ├── references.ris           # Zotero export (28 entries)
│   ├── references.bib           # BibTeX (27 entries, auto-generated)
│   └── apa.csl                  # Citation style (83 KB)
│
├── assets/figures/published/               # 38-40 images (auto-discovered)
│
├── sources/                     # Reference materials
│   ├── presentations/           # Original PPTX/PDF
│   ├── notes/                   # Schema & notes (37 KB total)
│   └── extracted/               # PPTX decomposition
│
├── output/                      # Generated files (git-ignored)
│   ├── latex/                   # Generated .tex files
│   ├── pdf/                     # Compiled PDFs
│   └── word/                    # DOCX exports
│
└── docs/                        # 9 documentation files
    ├── README.md                # Documentation index
    ├── QUICK_START_LATEX.md     # 3-step guide
    └── README_LATEX.md          # Complete LaTeX reference
```

## Essential Commands

### Primary Workflow

```bash
# 1. Convert Markdown to LaTeX with template
make latex

# 2. Compile LaTeX to PDF
cd output/latex && pdflatex article_draft.tex

# 3. View result
xdg-open output/latex/article_draft.pdf
```

### Alternative Workflows

```bash
make pdf          # Direct MD→PDF (one-step)
make html         # Generate HTML with MathJax
make docx         # Generate Word document
make bib          # Convert RIS→BibTeX
make clean        # Remove all generated files
make check-deps   # Verify pandoc/pdflatex/python3
make help         # Show all available targets
```

### Script Usage

```bash
# Main converter with options
python3 scripts/conversion/md_to_latex.py bridging-the-gap-article-draft.md \
  -o output/latex/output.tex \
  -t templates/template_latex.tex \
  -b references/references.bib \
  -c references/apa.csl

# Script help
python3 scripts/conversion/md_to_latex.py --help
```

## Critical Implementation Details

### Pandoc Version Handling

The system adapts to Pandoc versions dynamically:

- **Pandoc ≥ 2.11:** Uses `--citeproc` (built-in citation processing)
- **Pandoc < 2.11:** Falls back to `--filter pandoc-citeproc` if available
- **Current system:** 2.5 (old but functional)

Script detection in `md_to_latex.py`:
```python
def check_pandoc():
    # Returns: (available: bool, version: 'new'|'old')
    # Pandoc 2.11+ = 'new', < 2.11 = 'old'
```

### Template System

`templates/template_latex.tex` uses Pandoc variable substitution:

```latex
$if(csl-refs)$
  [Citation formatting setup]
$endif$

$title$, $author$, $date$  # Pandoc variables

\graphicspath{{./assets/figures/published/}{./assets/}{./sources/presentations/}}
# Auto-discovers images in these paths
```

**Key customization points:**
- Line 4: Document class `[12pt,a4paper]`
- Line 23: Margins `[margin=2.5cm]`
- Line 25: Line spacing `\onehalfspacing` (1.5)
- Line 68-70: BibLaTeX section (commented by default)

### Bibliography Workflow

**Input:** Zotero/Mendeley → RIS format (`references/references.ris`)

**Process:**
```bash
make bib  # Runs ris_to_bibtex.py
```

**Output:** `references/references.bib` with auto-generated cite keys

**Key format:** `AuthorYearTitle` (e.g., `Bandura1977Selfefficacy`)

**Type mapping:**
- JOUR → article
- BOOK → book
- CONF → inproceedings
- RPRT → techreport

### Image Path Resolution

Template's `\graphicspath` searches in order:
1. `./assets/figures/published/` (primary)
2. `./assets/`
3. `./sources/presentations/`

**Markdown reference:** `![Caption](image.png)` - no path needed

**Supported formats:** PNG, JPG, PDF

## Build System (Makefile)

### Key Variables

```makefile
INPUT = bridging-the-gap-article-draft.md
OUTPUT_TEX = output/latex/article_draft.tex
BIB_FILE = references/references.bib
TEMPLATE_TEX = templates/template_latex.tex
```

### Standard Pandoc Options

```makefile
PANDOC_OPTS = --number-sections --toc --toc-depth=3 --citeproc
PANDOC_FORMAT = -V documentclass=article -V papersize=a4 \
                -V fontsize=12pt -V geometry:margin=2.5cm \
                -V linestretch=1.5
```

### Dependency Chain

```
make latex → requires:
  - bridging-the-gap-article-draft.md
  - templates/template_latex.tex
  - references/references.bib
  - references/apa.csl

make bib → requires:
  - references/references.ris
  - ris_to_bibtex.py
```

## Script Architecture

### md_to_latex.py (268 lines)

**Core functions:**
1. `check_pandoc()` - Version detection, returns (bool, 'new'|'old')
2. `convert_md_to_latex()` - Main conversion engine
3. `main()` - CLI with argparse

**Default paths:**
- Template: `templates/template_latex.tex`
- Bibliography: `references/references.bib`
- CSL: `references/apa.csl`
- Output: `output/latex/[input_name].tex`

**Output path logic:**
```python
if output_file is None:
    output_file = Path('output/latex') / input_path.with_suffix('.tex').name
    output_file.parent.mkdir(parents=True, exist_ok=True)
```

### ris_to_bibtex.py (224 lines)

**Core functions:**
1. `parse_ris_file()` - RIS parser, groups by TY tags
2. `generate_cite_key()` - Creates `AuthorYearTitle` keys
3. `ris_to_bibtex_entry()` - Single entry converter
4. `clean_string()` - Escapes LaTeX special chars

**Special character handling:**
```python
text.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
```

## Common Modification Patterns

### Add New LaTeX Package

Edit `templates/template_latex.tex`:
```latex
% Add after existing packages (around line 50)
\usepackage{yourpackage}
```

Re-run: `make latex`

### Change Document Margins

Edit `templates/template_latex.tex` line 23:
```latex
\usepackage[margin=3cm]{geometry}  % Changed from 2.5cm
```

### Switch to BibLaTeX

Edit `templates/template_latex.tex` lines 68-70:
```latex
% Uncomment these lines:
\usepackage[style=apa,backend=biber]{biblatex}
\addbibresource{references/references.bib}
```

Then replace end-of-document bibliography:
```latex
% Replace:
\bibliography{references}

% With:
\printbibliography
```

Compile with:
```bash
pdflatex article_draft.tex
biber article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

### Add Image to Article

1. Save to `assets/figures/published/figure_01.png`
2. In `bridging-the-gap-article-draft.md`:
   ```markdown
   ![Figure 1: Description](figure_01.png)
   ```
3. Re-run: `make latex && cd output/latex && pdflatex article_draft.tex`

### Update Bibliography

1. Export from Zotero as RIS to `references/references.ris`
2. Run: `make bib`
3. Verify: `references/references.bib` updated
4. Re-run: `make latex`

## Error Recovery

```bash
# Clean rebuild
make clean && make latex

# Verify environment
make check-deps

# Debug Pandoc command
python3 scripts/conversion/md_to_latex.py bridging-the-gap-article-draft.md --pandoc-opts="--verbose"

# Force bibliography regeneration
rm references/references.bib && make bib
```

## Version Control Practices

**Commit:**
- `bridging-the-gap-article-draft.md` (source)
- `templates/template_latex.tex` (template)
- `references/references.{ris,bib}` (both formats)
- `scripts/*.py` (conversion tools)
- `Makefile` (build system)

**Ignore (.gitignore):**
- `output/` (all generated files)
- `*.aux`, `*.log`, `*.out` (LaTeX artifacts)
- `__pycache__/` (Python cache)

## Dependencies

**Required:**
- Pandoc ≥ 2.5 (2.11+ recommended for `--citeproc`)
- pdflatex (from texlive-full)
- Python 3 (standard library only, no pip packages)

**Optional:**
- biber/bibtex (for manual bibliography compilation)
- entr (for `make watch` file monitoring)

**Check:** `make check-deps`

## Research Context

**Article:** "Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students"

**Key findings:**
- 80% students use AI daily vs. lower teacher adoption
- Competence gap: High practical (4.32/7) vs. low theoretical (3.16/7)
- Training inadequacy: 28% rate it "not adequate"
- ChatGPT dominance (monoculture)

**Structure:** Introduction → Framework → Methods → Results (7 sections) → Discussion (7 points) → Conclusion

## Documentation

All documentation in `docs/`:

- **docs/README.md** - Documentation index
- **docs/guides/QUICK_START_LATEX.md** - 3-step getting started
- **docs/guides/README_LATEX.md** - Complete LaTeX guide (366 lines)
- **docs/guides/CONVERSION_GUIDE.md** - All conversion methods
- **docs/PROJECT_SUMMARY.md** - Research overview + file reference

**Start here:** `docs/README.md` → Task-based navigation

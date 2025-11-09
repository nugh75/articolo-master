# Quick Conversion Guide

## 🚀 Quick Start (3 Steps)

### Method 1: Using Make (Recommended)

```bash
# 1. Install dependencies (one time only)
make install-deps

# 2. Generate LaTeX
make latex

# 3. Compile PDF
cd output/latex
pdflatex article_draft.tex

# Done! Your PDF is ready: output/latex/article_draft.pdf
```

### Method 2: Using Python Script

```bash
# 1. Convert Markdown to LaTeX
python3 scripts/conversion/md_to_latex.py bridging-the-gap-article-draft.md

# 2. Compile LaTeX to PDF
cd output/latex
pdflatex article_draft.tex

# Done! Your PDF is ready: output/latex/article_draft.pdf
```

### Method 3: Direct PDF (Legacy)

```bash
# Generate PDF directly (uses old conversion method)
make pdf

# Done! Your PDF is ready: output/pdf/article_draft.pdf
```

## 📋 What Each Method Does

### Method 1: Make + LaTeX (Recommended)
1. ✓ Uses custom LaTeX template
2. ✓ Full control over preambolo
3. ✓ Manages bibliography with BibTeX/BibLaTeX
4. ✓ Finds images in `assets/figures/published/`
5. ✓ Output in `output/latex/`

### Method 2: Python Script
1. ✓ Flexible conversion options
2. ✓ Works with different Pandoc versions
3. ✓ Custom template support
4. ✓ Automatic path detection

### Method 3: Direct PDF
1. ✓ One-step conversion
2. ✓ Good for quick previews
3. ⚠️  Less customization

## 📂 Files and Directories

After conversion, your structure:

```
articolo/
├── bridging-the-gap-article-draft.md              ← Source file
├── output/
│   ├── latex/
│   │   └── article_draft.tex    ← Generated LaTeX
│   └── pdf/
│       └── article_draft.pdf    ← Generated PDF
├── references/
│   ├── references.bib           ← Bibliography
│   └── apa.csl                  ← Citation style
├── templates/
│   └── template_latex.tex       ← LaTeX template
└── assets/
    └── charts/                  ← Images
```

## 🔧 Available Commands (Using Make)

```bash
make latex        # Create LaTeX with custom template (recommended)
make pdf          # Create PDF directly
make html         # Create HTML version
make docx         # Create Word document
make tex          # Create basic LaTeX (without template)
make clean        # Remove generated files
make check-deps   # Verify dependencies
make help         # Show all commands
```

## 📖 Document Features

The generated LaTeX/PDF includes:

- ✓ Custom template with configurable preambolo
- ✓ Bibliography management (BibTeX or BibLaTeX)
- ✓ Numbered sections
- ✓ A4 paper size, 12pt font
- ✓ 2.5cm margins, 1.5 line spacing
- ✓ Automatic image path detection
- ✓ Clickable links and references

## 🆘 Troubleshooting

### Problem: "make: command not found"

**Solution:** Install make
```bash
sudo apt-get install build-essential
```

### Problem: "pandoc: command not found"

**Solution:** Install pandoc
```bash
sudo apt-get install pandoc
```

### Problem: "pdflatex: command not found"

**Solution:** Install LaTeX
```bash
sudo apt-get install texlive-full
```
Note: This is a large download (~4GB). For minimal installation (~500MB):
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### Problem: "Images not found"

**Solution:** Images should be in `assets/figures/published/`. The template is configured to find them there.

### Problem: "Template not found"

**Solution:** Template should be in `templates/template_latex.tex`. Verify with:
```bash
ls templates/template_latex.tex
```

### Problem: LaTeX compilation errors

**Solution:** Install additional packages
```bash
sudo apt-get install texlive-lang-european texlive-science
```

## 🎯 Quick Checks

Before converting, verify:

```bash
# Check all dependencies
make check-deps

# Or manually:
pandoc --version      # Shows Pandoc version
pdflatex --version    # Shows TeX distribution
python3 --version     # Shows Python version
```

## 📚 File Locations

- **Source article**: `bridging-the-gap-article-draft.md` (root)
- **Template**: `templates/template_latex.tex`
- **Bibliography**: `references/references.bib`
- **Citation style**: `references/apa.csl`
- **Images**: `assets/figures/published/`
- **Scripts**: `scripts/`
- **Output LaTeX**: `output/latex/`
- **Output PDF**: `output/pdf/`
- **Output Word**: `output/word/`

## 💡 Tips

1. **Edit template first** - Customize `templates/template_latex.tex` before converting
2. **Use Make for convenience** - Handles all paths automatically
3. **Check output** - Always verify generated files look correct
4. **Images organized** - Keep all images in `assets/figures/published/`
5. **Version control** - Output files in `output/` are git-ignored

## 🔄 Workflow Example

```bash
# Edit your article
nano bridging-the-gap-article-draft.md

# Convert to LaTeX
make latex

# Review LaTeX file
less output/latex/article_draft.tex

# Edit template if needed
nano templates/template_latex.tex

# Regenerate
make latex

# Compile to PDF
cd output/latex
pdflatex article_draft.tex

# View PDF
xdg-open article_draft.pdf
```

## 📝 Managing Citations

### In Markdown

```markdown
According to research [@Bandura1977], self-efficacy is important.

Multiple sources [@Jenkins2009; @Davis1989; @Venkatesh2000].

With page number [@Munari2024, p. 42].
```

### With BibTeX (manual)

1. Convert as usual: `make latex`
2. In LaTeX file, citations appear as text
3. Manually convert `[@key]` to `\cite{key}` if needed
4. Compile with BibTeX:
```bash
cd output/latex
pdflatex article_draft.tex
bibtex article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

### Citation keys

Find citation keys in `references/references.bib` (look for `@type{KEY,`)

## 🌐 Alternative Outputs

```bash
make html    # For web viewing → output/article_draft.html
make docx    # For Word → output/word/article_draft.docx
make tex     # Basic LaTeX → output/latex/article_draft.tex
make latex   # LaTeX with template → output/latex/article_draft.tex
```

## ✅ Success Indicators

You'll know conversion succeeded when you see:

```
✓ LaTeX generated successfully!
  File: output/latex/article_draft.tex
  Template: templates/template_latex.tex
```

And the file exists:
```bash
ls -lh output/latex/article_draft.tex
```

## 🎓 Customizing Template

Edit `templates/template_latex.tex` to customize:

- **Preambolo**: Add/remove LaTeX packages
- **Margins**: Change geometry settings
- **Fonts**: Modify document class
- **Citations**: Switch between BibTeX/BibLaTeX
- **Image paths**: Adjust `\graphicspath`

See [README_LATEX.md](README_LATEX.md) for details.

---

**Need Help?**
1. Check [README_LATEX.md](README_LATEX.md) for LaTeX-specific help
2. Check [../README.md](../README.md) for project overview
3. Run `make help` for all commands
4. Run `python3 scripts/conversion/md_to_latex.py --help` for script options

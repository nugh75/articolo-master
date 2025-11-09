# Installation & Dependencies

> **Project Version**: 2.0 - Updated paths and structure

## ✅ Quick Check

Verify all dependencies:

```bash
make check-deps
```

## 📦 Required Software

### 1. Pandoc (Document Converter)

**Check if installed:**
```bash
pandoc --version
```

**Install:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install pandoc
```

**Recommended version**: 2.11+ (current system has 2.5 - works but limited features)

### 2. LaTeX (PDF Compilation)

**Check if installed:**
```bash
pdflatex --version
```

**Install:**
```bash
# Full installation (recommended, ~4GB)
sudo apt-get install texlive-full

# Minimal installation (~500MB)
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### 3. Python 3

**Check if installed:**
```bash
python3 --version
```

**Install:**
```bash
sudo apt-get install python3
```

## 🔧 Install All Dependencies

### Method 1: Using Makefile (Recommended)

```bash
make install-deps
```

This will install:
- pandoc
- texlive-full
- python3

### Method 2: Manual Installation

```bash
sudo apt-get update
sudo apt-get install pandoc texlive-full python3
```

## 📁 Current Project Structure

All files are now organized:

```
articolo/
├── bridging-the-gap-article-draft.md              ← Source (root)
├── scripts/                      ← Conversion tools
│   ├── md_to_latex.py           ← Main converter
│   ├── convert_to_pdf.py        ← Legacy PDF
│   ├── convert_to_pdf.sh
│   └── ris_to_bibtex.py
├── templates/                    ← LaTeX templates
│   └── template_latex.tex
├── references/                   ← Bibliography
│   ├── references.bib
│   ├── references.ris
│   └── apa.csl
├── assets/figures/published/                ← Images
└── output/                       ← Generated files
    ├── latex/
    ├── pdf/
    └── word/
```

## ✓ System Status

**Current system has:**
- ✅ pdflatex (LaTeX installed)
- ✅ python3 (Python installed)
- ⚠️  pandoc 2.5 (old version - works but limited)

**Upgrade pandoc (optional):**
```bash
# Download latest version
wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-amd64.deb

# Install
sudo dpkg -i pandoc-3.1.11-1-amd64.deb
```

## 🚀 Quick Start After Installation

### Convert Markdown to LaTeX

```bash
make latex
```

### Compile LaTeX to PDF

```bash
cd output/latex
pdflatex article_draft.tex
```

### All in One (Direct PDF)

```bash
make pdf
```

## 🔍 Verify Installation

```bash
# Check all dependencies
make check-deps

# Manual check
pandoc --version      # Should show 2.5 or higher
pdflatex --version    # Should show TeX distribution
python3 --version     # Should show Python 3.x
```

## ⚙️ Additional LaTeX Packages (Optional)

For advanced features:

```bash
# European languages support
sudo apt-get install texlive-lang-european

# Science/math packages
sudo apt-get install texlive-science

# Additional fonts
sudo apt-get install texlive-fonts-extra
```

## 🌐 Alternative: Install Without Sudo

If you don't have sudo access:

### Pandoc

```bash
# Download binary
cd ~
wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-linux-amd64.tar.gz

# Extract
tar xvzf pandoc-3.1.11-linux-amd64.tar.gz

# Add to PATH
export PATH=$HOME/pandoc-3.1.11/bin:$PATH

# Make permanent
echo 'export PATH=$HOME/pandoc-3.1.11/bin:$PATH' >> ~/.bashrc
```

### LaTeX

Consider using:
- **Overleaf** (online LaTeX editor)
- **Portable TeX** distributions
- Ask system administrator for installation

## 🆘 Troubleshooting

### "pandoc: command not found"

**Solution**: Install pandoc (see above)

### "pdflatex: command not found"

**Solution**: Install LaTeX distribution

### "Package babel Error"

**Solution**:
```bash
sudo apt-get install texlive-lang-european
```

### Pandoc version too old

Current system has 2.5. Some features require 2.11+:
- `--citeproc` flag (citation processing)
- Modern template features

**Workaround**: The system uses fallbacks for older versions

**Upgrade**: Download newer version (see above)

## 📖 What Each Tool Does

| Tool | Purpose | Used For |
|------|---------|----------|
| **pandoc** | Universal document converter | MD → LaTeX, MD → PDF, MD → HTML |
| **pdflatex** | LaTeX compiler | LaTeX → PDF |
| **python3** | Script executor | Running conversion scripts |
| **make** | Build automation | Managing workflows |

## 🎯 Minimum Requirements

To use the basic conversion workflow:

- ✅ pandoc (any version)
- ✅ pdflatex
- ✅ python3

Optional but recommended:
- latexmk (automates multiple pdflatex runs)
- biber or bibtex (for bibliography)

## 📝 Usage Examples

### After Installing Dependencies

```bash
# Convert article to LaTeX
make latex

# View generated LaTeX
less output/latex/article_draft.tex

# Compile to PDF
cd output/latex
pdflatex article_draft.tex

# View PDF
xdg-open article_draft.pdf
```

## 🔗 Resources

- **Pandoc documentation**: https://pandoc.org/
- **Pandoc installation**: https://pandoc.org/installing.html
- **LaTeX documentation**: https://www.latex-project.org/
- **TeX Live**: https://tug.org/texlive/

## ✨ Next Steps

Once dependencies are installed:

1. **Read main README**: [../README.md](../README.md)
2. **Quick start guide**: [QUICK_START_LATEX.md](QUICK_START_LATEX.md)
3. **Conversion guide**: [CONVERSION_GUIDE.md](CONVERSION_GUIDE.md)
4. **Run conversion**: `make latex`

---

**Need Help?**

```bash
make help                              # Show all Makefile commands
python3 scripts/conversion/md_to_latex.py --help  # Show script options
make check-deps                        # Verify installations
```

**Last Updated**: October 18, 2025 (v2.0)

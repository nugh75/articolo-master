#!/bin/bash

# Script to convert article from Markdown to PDF using LaTeX with APA citations
# Requirements: pandoc, texlive-full (or at least texlive-latex-extra, texlive-fonts-recommended)

set -e  # Exit on error

# Configuration
INPUT_FILE="bridging-the-gap-article-draft.md"
OUTPUT_BASE="article_draft"
TIMESTAMP="$(date +%Y-%m-%d_%H-%M)"
BASE_DIR="output"
BUILD_DIR="${BASE_DIR}/build-${TIMESTAMP}"
OUTPUT_PDF="${BUILD_DIR}/${OUTPUT_BASE}.pdf"
OUTPUT_TEX="${BUILD_DIR}/${OUTPUT_BASE}.tex"
BIB_FILE="references/references.bib"
CSL_FILE="references/apa.csl"
LOCAL_PANDOC="tools/bin/pandoc"
if [ -x "$LOCAL_PANDOC" ]; then
    PANDOC_BIN="$LOCAL_PANDOC"
else
    PANDOC_BIN=$(command -v pandoc || true)
fi
PANDOC_BIN=${PANDOC_BIN:-pandoc}
PDF_ENGINE=${PDF_ENGINE:-xelatex}

echo "=========================================="
echo "Converting Markdown to PDF with APA style"
echo "=========================================="
echo ""

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi

# Check if pandoc is installed
if [ -z "$PANDOC_BIN" ] || [ ! -x "$PANDOC_BIN" ]; then
    echo "Error: pandoc is not installed!"
    echo "Install with: sudo apt-get install pandoc"
    exit 1
fi

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex is not installed!"
    echo "Install with: sudo apt-get install texlive-full"
    exit 1
fi

echo "Step 1: Converting RIS to BibTeX..."
# Convert RIS to BibTeX if needed
if [ -f "references/references.ris" ]; then
    if command -v pandoc-citeproc &> /dev/null || "$PANDOC_BIN" --version | grep -q "citeproc"; then
        echo "Converting references/references.ris to $BIB_FILE..."
        # Using pandoc to convert (requires pandoc 2.11+)
        "$PANDOC_BIN" references/references.ris -t biblatex -o "$BIB_FILE" 2>/dev/null || echo "Note: RIS conversion may need manual adjustment"
    else
        echo "Warning: Cannot auto-convert RIS. Please convert references/references.ris to BibTeX manually."
    fi
fi

echo ""
echo "Step 2: Downloading APA CSL style if needed..."
# Download APA 7th edition CSL if not present
if [ ! -f "$CSL_FILE" ]; then
    echo "Downloading APA 7th edition citation style..."
    curl -sL "https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl" -o "$CSL_FILE"
    if [ $? -eq 0 ]; then
        echo "✓ APA style downloaded successfully"
    else
        echo "Warning: Could not download APA style. Using default."
    fi
fi

echo ""
echo "Step 3: Converting Markdown to PDF..."

# Ensure output directories exist
mkdir -p "$BUILD_DIR"

# Determine citeproc options
CITE_OPTS=()
PANDOC_VERSION=$("$PANDOC_BIN" --version | head -1 | awk '{print $2}')
IFS=. read -r PANDOC_MAJOR PANDOC_MINOR _ <<< "$PANDOC_VERSION"
PANDOC_MAJOR=${PANDOC_MAJOR:-0}
PANDOC_MINOR=${PANDOC_MINOR:-0}
if [ "$PANDOC_MAJOR" -gt 2 ] || { [ "$PANDOC_MAJOR" -eq 2 ] && [ "$PANDOC_MINOR" -ge 11 ]; }; then
    CITE_OPTS=(--citeproc)
elif command -v pandoc-citeproc &> /dev/null; then
    CITE_OPTS=(--filter pandoc-citeproc)
else
    echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."
fi

CSL_OPTS=()
if [ ${#CITE_OPTS[@]} -gt 0 ]; then
    CSL_OPTS=(--csl="$CSL_FILE")
else
    echo "ℹ CSL style skipped (citeproc unavailable)."
fi

# Pandoc conversion with comprehensive options
"$PANDOC_BIN" "$INPUT_FILE" \
    -o "$OUTPUT_PDF" \
    --pdf-engine="$PDF_ENGINE" \
    "${CITE_OPTS[@]}" \
    "${CSL_OPTS[@]}" \
    --bibliography="$BIB_FILE" \
    --lua-filter=filters/promote_headings.lua \
    --lua-filter=filters/limit_image_width.lua \
    --lua-filter=filters/language_filter.lua \
    --lua-filter=filters/custom_numbering.lua \
    --toc \
    --toc-depth=3 \
    -V documentclass=article \
    -V papersize=a4 \
    -V fontsize=12pt \
    -V geometry:margin=2.5cm \
    -V linestretch=1.5 \
    -V fontfamily=times \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -V toccolor=black \
    --highlight-style=tango \
    --metadata title="Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students" \
    --metadata author="Daniele Dragoni, Rino Falcone, Elisa Colì, Isabella Poggi, Daniele Caligiore" \
    --metadata date="$(date +%Y)" \
    --verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ PDF created successfully: $OUTPUT_PDF"
    echo "=========================================="
    echo ""
    echo "File details:"
    ls -lh "$OUTPUT_PDF"
else
    echo ""
    echo "=========================================="
    echo "✗ Error creating PDF"
    echo "=========================================="
    exit 1
fi

# Also create standalone LaTeX file for manual editing if needed
echo ""
echo "Step 4: Creating standalone LaTeX file..."
"$PANDOC_BIN" "$INPUT_FILE" \
    -o "$OUTPUT_TEX" \
    --standalone \
    "${CITE_OPTS[@]}" \
    "${CSL_OPTS[@]}" \
    --bibliography="$BIB_FILE" \
    --lua-filter=filters/promote_headings.lua \
    --lua-filter=filters/limit_image_width.lua \
    --lua-filter=filters/language_filter.lua \
    --lua-filter=filters/custom_numbering.lua \
    --toc \
    --toc-depth=3 \
    -V documentclass=article \
    -V papersize=a4 \
    -V fontsize=12pt \
    -V geometry:margin=2.5cm \
    -V linestretch=1.5 \
    -V fontfamily=times \
    --metadata title="Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students" \
    --metadata author="Daniele Dragoni, Rino Falcone, Elisa Colì, Isabella Poggi, Daniele Caligiore"

if [ $? -eq 0 ]; then
    echo "✓ LaTeX file created: $OUTPUT_TEX"
    echo "  (You can edit this manually and compile with: pdflatex -output-directory $BUILD_DIR $OUTPUT_TEX)"
fi

echo ""
echo "Conversion complete!"
echo ""
echo "Generated files:"
echo "  - $OUTPUT_PDF (main output)"
echo "  - $OUTPUT_TEX (editable LaTeX source)"
if [ -f "$CSL_FILE" ]; then
    echo "  - $CSL_FILE (APA citation style)"
fi
if [ -f "$BIB_FILE" ]; then
    echo "  - $BIB_FILE (bibliography)"
fi

echo ""
echo "To view the PDF:"
echo "  xdg-open $OUTPUT_PDF"

# Makefile for converting Markdown article to PDF with APA citations

# Configuration - Paths updated for new structure
ARTICLE_TITLE = Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students
ARTICLE_SLUG = bridging-the-gap
INPUT = bridging-the-gap-article-draft.md
INPUT_BASENAME = $(basename $(notdir $(INPUT)))
RIS_FILE = references/references.ris
BIB_FILE = references/references.bib
CSL_FILE = references/apa.csl
CSL_URL = https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
TEMPLATE_TEX = templates/template_latex.tex
CONVERSION_SCRIPT = scripts/conversion/md_to_latex.py
OUTPUT_BASE_DIR = output
BUILD_ID ?= $(shell date +%Y-%m-%d_%H-%M)
OUTPUT_BASENAME = $(ARTICLE_SLUG)_$(BUILD_ID)
BUILD_DIR = $(OUTPUT_BASE_DIR)/$(OUTPUT_BASENAME)
REFERENCE_DOCX = templates/reference.docx
JOURNAL_GUIDE = Ricerca riviste dove scriverre/GUIDA_COMPLETA_RIVISTE.md
JOURNAL_GUIDE_OUTPUT = $(OUTPUT_BASE_DIR)/journal-guide

export PATH := $(HOME)/bin:$(abspath tools/bin):$(PATH)

PDF_ENGINE ?= xelatex

# Pandoc options
PANDOC_OPTS = --toc --toc-depth=3 \
              --lua-filter=filters/promote_headings.lua \
              --lua-filter=filters/limit_image_width.lua
PANDOC_META =
PANDOC_FORMAT = -V documentclass=article -V papersize=a4 -V fontsize=12pt \
                -V geometry:margin=2.5cm -V linestretch=1.5 \
                -V mainfont="TeX Gyre Termes" \
                -V sansfont="TeX Gyre Heros" \
                -V monofont="TeX Gyre Cursor" \
                -V mathfont="TeX Gyre Termes Math" \
                -V linkcolor=blue -V urlcolor=blue \
                -V indent=true -V parskip=0pt

# Language + numbering filters
LANG_FILTER = filters/language_filter.lua
NUMBERING_FILTER = filters/custom_numbering.lua

# Phony targets
.PHONY: all bundle pdf tex latex html docx audio clean check-deps install-deps bib csl help
.PHONY: pdf-en pdf-it pdf-both html-en html-it html-both docx-en docx-it docx-both
.PHONY: tex-en tex-it tex-both latex-en latex-it latex-both journal-guide journal-guide-docx

# Default target
all: bundle

# Help
help:
	@echo "Makefile for Article Conversion"
	@echo ""
	@echo "Available targets:"
	@echo "  make pdf        - Generate PDF (bilingual)"
	@echo "  make pdf-en     - Generate PDF (English only)"
	@echo "  make pdf-it     - Generate PDF (Italian only)"
	@echo "  make pdf-both   - Generate PDF (bilingual - explicit)"
	@echo "  make tex        - Generate LaTeX file (basic)"
	@echo "  make latex      - Generate LaTeX with custom template (recommended)"
	@echo "  make html       - Generate HTML file (bilingual)"
	@echo "  make html-en    - Generate HTML (English only)"
	@echo "  make html-it    - Generate HTML (Italian only)"
	@echo "  make docx       - Generate Word document (bilingual)"
	@echo "  make docx-en    - Generate Word document (English only)"
	@echo "  make docx-it    - Generate Word document (Italian only)"
	@echo "  make bundle     - Generate PDF, HTML, LaTeX, and DOCX in one folder (default)"
	@echo "  make all        - Same as 'make bundle'"
	@echo "  make journal-guide - Generate PDF of the complete journal submission guide"
	@echo "  make journal-guide-docx - Generate DOCX of the complete journal submission guide"
	@echo "  make bib        - Convert RIS to BibTeX"
	@echo "  make csl        - Download APA citation style"
	@echo "  make clean      - Remove generated files"
	@echo "  make check-deps - Check required dependencies"
	@echo "  make install-deps - Install dependencies (requires sudo)"
	@echo ""
	@echo "Examples:"
	@echo "  make pdf-en                 # Create English-only PDF"
	@echo "  make pdf-it                 # Create Italian-only PDF"
	@echo "  make html-both              # Create bilingual HTML"
	@echo "  make docx-en                # Create English-only Word doc"
	@echo "  make journal-guide          # Create journal submission guide PDF"
	@echo "  make journal-guide-docx     # Create journal submission guide DOCX"
	@echo "  make check-deps             # Verify installation"

# Check dependencies
check-deps:
	@echo "Checking dependencies..."
	@which pandoc > /dev/null || (echo "✗ pandoc not found" && exit 1)
	@echo "✓ pandoc found: $$(pandoc --version | head -1)"
	@which pdflatex > /dev/null || (echo "✗ pdflatex not found (required for PDF)" && exit 1)
	@echo "✓ pdflatex found"
	@which python3 > /dev/null || (echo "✗ python3 not found" && exit 1)
	@echo "✓ python3 found: $$(python3 --version)"
	@echo ""
	@echo "All dependencies satisfied!"

# Install dependencies (Ubuntu/Debian)
install-deps:
	@echo "Installing dependencies..."
	@echo "This requires sudo privileges and may take some time..."
	@sudo apt-get update
	@sudo apt-get install -y pandoc texlive-full python3
	@echo "✓ Dependencies installed!"

# Download APA CSL style
$(CSL_FILE):
	@echo "Downloading APA citation style..."
	@curl -sL "$(CSL_URL)" -o $(CSL_FILE)
	@echo "✓ Downloaded: $(CSL_FILE)"

csl: $(CSL_FILE)

# Convert RIS to BibTeX
$(BIB_FILE): $(RIS_FILE)
	@echo "Converting RIS to BibTeX..."
	@python3 scripts/conversion/ris_to_bibtex.py $(RIS_FILE) $(BIB_FILE)

bib: $(BIB_FILE)

# Generate PDF (bilingual by default)
pdf: pdf-both

# Generate PDF - English only
pdf-en: $(INPUT) $(BIB_FILE) $(CSL_FILE) check-deps
	@mkdir -p "$(BUILD_DIR)"; \
	 output_file="$(BUILD_DIR)/$(OUTPUT_BASENAME)_en.pdf"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating PDF (English only) -> $$output_file"; \
	 if pandoc $(INPUT) -o "$$output_file" \
		--pdf-engine=$(PDF_ENGINE) \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		$(PANDOC_FORMAT) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=en \
		--include-in-header=templates/pandoc_tables.tex \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--verbose; then \
	     echo ""; \
	     echo "✓ PDF (English) created: $$output_file"; \
	     ls -lh "$$output_file"; \
	 else \
	     echo ""; \
	     echo "✗ Error creating PDF"; \
	     exit 1; \
	 fi

# Generate PDF - Italian only
pdf-it: $(INPUT) $(BIB_FILE) $(CSL_FILE) check-deps
	@mkdir -p "$(BUILD_DIR)"; \
	 output_file="$(BUILD_DIR)/$(OUTPUT_BASENAME)_it.pdf"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating PDF (Italian only) -> $$output_file"; \
	 if pandoc $(INPUT) -o "$$output_file" \
		--pdf-engine=$(PDF_ENGINE) \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		$(PANDOC_FORMAT) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=it \
		--include-in-header=templates/pandoc_tables.tex \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--verbose; then \
	     echo ""; \
	     echo "✓ PDF (Italian) created: $$output_file"; \
	     ls -lh "$$output_file"; \
	 else \
	     echo ""; \
	     echo "✗ Error creating PDF"; \
	     exit 1; \
	 fi

# Generate PDF - Bilingual
pdf-both: $(INPUT) $(BIB_FILE) $(CSL_FILE) check-deps
	@mkdir -p "$(BUILD_DIR)"; \
	 output_file="$(BUILD_DIR)/$(OUTPUT_BASENAME)_both.pdf"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating PDF (Bilingual) -> $$output_file"; \
	 if pandoc $(INPUT) -o "$$output_file" \
		--pdf-engine=$(PDF_ENGINE) \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		$(PANDOC_FORMAT) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=both \
		--include-in-header=templates/pandoc_tables.tex \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--verbose; then \
	     echo ""; \
	     echo "✓ PDF (Bilingual) created: $$output_file"; \
	     ls -lh "$$output_file"; \
	 else \
	     echo ""; \
	     echo "✗ Error creating PDF"; \
	     exit 1; \
	 fi

# Generate LaTeX (basic - without template)
tex: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_tex="$(BUILD_DIR)/$(OUTPUT_BASENAME).tex"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating LaTeX (basic) -> $$output_tex"; \
	 pandoc $(INPUT) -o "$$output_tex" \
		--standalone \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		$(PANDOC_FORMAT) \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE); \
	 echo "✓ LaTeX created: $$output_tex"; \
	 echo "  Compile with: pdflatex -output-directory $(BUILD_DIR) $$output_tex"

# Generate LaTeX with custom template (recommended)
latex: $(INPUT) $(BIB_FILE) $(CSL_FILE) $(TEMPLATE_TEX)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_tex="$(BUILD_DIR)/$(OUTPUT_BASENAME).tex"; \
	 echo "========================================================"; \
	 echo "  Generating LaTeX with custom template"; \
	 echo "========================================================"; \
	 python3 $(CONVERSION_SCRIPT) $(INPUT) \
		-o "$$output_tex" \
		-t $(TEMPLATE_TEX) \
		-b $(BIB_FILE) \
		-c $(CSL_FILE); \
	 echo ""; \
	 echo "✓ LaTeX generated successfully!"; \
	 echo "  File: $$output_tex"; \
	 echo "  Template: $(TEMPLATE_TEX)"; \
	 echo ""; \
	 echo "Next steps:"; \
	 echo "  1. Review the LaTeX file: less $$output_tex"; \
	 echo "  2. Compile to PDF: pdflatex -output-directory $(BUILD_DIR) $$output_tex"; \
	 echo "  3. Or use: latexmk -pdf -outdir=$(BUILD_DIR) $$output_tex"; \
	 echo "========================================================"

# Generate HTML (bilingual by default)
html: html-both

# Generate HTML - English only
html-en: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_html="$(BUILD_DIR)/$(OUTPUT_BASENAME)_en.html"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating HTML (English only) -> $$output_html"; \
	 pandoc $(INPUT) -o "$$output_html" \
		--embed-resources \
		--standalone \
		--css=config/html.css \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=en \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--katex; \
	 echo "✓ HTML (English) created: $$output_html"; \
	 echo "  Open with: xdg-open $$output_html"

# Generate HTML - Italian only
html-it: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_html="$(BUILD_DIR)/$(OUTPUT_BASENAME)_it.html"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating HTML (Italian only) -> $$output_html"; \
	 pandoc $(INPUT) -o "$$output_html" \
		--embed-resources \
		--standalone \
		--css=config/html.css \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=it \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--katex; \
	 echo "✓ HTML (Italian) created: $$output_html"; \
	 echo "  Open with: xdg-open $$output_html"

# Generate HTML - Bilingual
html-both: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_html="$(BUILD_DIR)/$(OUTPUT_BASENAME)_both.html"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating HTML (Bilingual) -> $$output_html"; \
	 pandoc $(INPUT) -o "$$output_html" \
		--embed-resources \
		--standalone \
		--css=config/html.css \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=both \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--highlight-style=tango \
		--katex; \
	 echo "✓ HTML (Bilingual) created: $$output_html"; \
	 echo "  Open with: xdg-open $$output_html"

# Generate DOCX (bilingual by default)
docx: docx-both

# Generate DOCX - English only
docx-en: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_docx="$(BUILD_DIR)/$(OUTPUT_BASENAME)_en.docx"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating Word document (English only) -> $$output_docx"; \
	 pandoc $(INPUT) -o "$$output_docx" \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=en \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--reference-doc=$(REFERENCE_DOCX); \
	 python3 scripts/conversion/postprocess_docx_tables.py "$$output_docx"; \
	 echo "✓ DOCX (English) created: $$output_docx"

# Generate DOCX - Italian only
docx-it: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_docx="$(BUILD_DIR)/$(OUTPUT_BASENAME)_it.docx"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating Word document (Italian only) -> $$output_docx"; \
	 pandoc $(INPUT) -o "$$output_docx" \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=it \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--reference-doc=$(REFERENCE_DOCX); \
	 python3 scripts/conversion/postprocess_docx_tables.py "$$output_docx"; \
	 echo "✓ DOCX (Italian) created: $$output_docx"

# Generate DOCX - Bilingual
docx-both: $(INPUT) $(BIB_FILE) $(CSL_FILE)
	@mkdir -p "$(BUILD_DIR)"; \
	 output_docx="$(BUILD_DIR)/$(OUTPUT_BASENAME)_both.docx"; \
	 cite_opts=$$(python3 scripts/conversion/detect_citeproc.py); \
	 if [ -z "$$cite_opts" ]; then \
	     echo "⚠ Warning: citeproc not available - citations will be handled by LaTeX."; \
	     csl_flag=""; \
	 else \
	     csl_flag="--csl=$(CSL_FILE)"; \
	 fi; \
	 echo "Generating Word document (Bilingual) -> $$output_docx"; \
	 pandoc $(INPUT) -o "$$output_docx" \
		$(PANDOC_OPTS) \
		$(PANDOC_META) \
		--lua-filter=$(LANG_FILTER) \
		--lua-filter=$(NUMBERING_FILTER) \
		--metadata lang=both \
		$$cite_opts \
		$$csl_flag \
		--bibliography=$(BIB_FILE) \
		--reference-doc=$(REFERENCE_DOCX); \
	 python3 scripts/conversion/postprocess_docx_tables.py "$$output_docx"; \
	 echo "✓ DOCX (Bilingual) created: $$output_docx"

# Generate full bundle in a shared build directory
bundle: $(INPUT) $(BIB_FILE) $(CSL_FILE) check-deps
	@build_id=$${BUILD_ID:-$$(date +%Y%m%d_%H%M%S)}; \
	 bundle_prefix="$(INPUT_BASENAME)"; \
	 bundle_dir="$(OUTPUT_BASE_DIR)/$${bundle_prefix}-$$build_id"; \
	 echo "========================================================"; \
	 echo "  Bundle build -> $$bundle_dir"; \
	 echo "========================================================"; \
	 $(MAKE) BUILD_ID="$$build_id" BUILD_PREFIX="$$bundle_prefix" pdf; \
	 $(MAKE) BUILD_ID="$$build_id" BUILD_PREFIX="$$bundle_prefix" html; \
	 $(MAKE) BUILD_ID="$$build_id" BUILD_PREFIX="$$bundle_prefix" tex; \
	 $(MAKE) BUILD_ID="$$build_id" BUILD_PREFIX="$$bundle_prefix" docx; \
	 echo "--------------------------------------------------------"; \
	 echo "✓ All artifacts generated in: $$bundle_dir"; \
	 echo "--------------------------------------------------------"

# Generate Journal Guide PDF
journal-guide: check-deps
	@guide_file="$(JOURNAL_GUIDE)"; \
	 if [ ! -f "$$guide_file" ]; then \
	     echo "✗ Error: Journal guide file not found: $$guide_file"; \
	     exit 1; \
	 fi; \
	 mkdir -p "$(JOURNAL_GUIDE_OUTPUT)"; \
	 output_pdf="$(JOURNAL_GUIDE_OUTPUT)/journal-guide.pdf"; \
	 echo "========================================================"; \
	 echo "  Generating Journal Submission Guide PDF"; \
	 echo "========================================================"; \
	 echo "Input: $$guide_file"; \
	 echo "Output: $$output_pdf"; \
	 echo ""; \
	 if pandoc "$$guide_file" -o "$$output_pdf" \
		--pdf-engine=$(PDF_ENGINE) \
		--toc --toc-depth=2 \
		-V documentclass=article \
		-V papersize=a4 \
		-V fontsize=11pt \
		-V geometry:margin=2cm \
		-V linestretch=1.3 \
		-V mainfont="TeX Gyre Termes" \
		-V sansfont="TeX Gyre Heros" \
		-V monofont="TeX Gyre Cursor" \
		-V linkcolor=blue \
		-V urlcolor=blue \
		--highlight-style=tango \
		--verbose; then \
	     echo ""; \
	     echo "✓ Journal guide PDF created: $$output_pdf"; \
	     ls -lh "$$output_pdf"; \
	     echo "  Open with: xdg-open $$output_pdf"; \
	     echo "========================================================"; \
	 else \
	     echo ""; \
	     echo "✗ Error creating journal guide PDF"; \
	     exit 1; \
	 fi

# Generate Journal Guide DOCX
journal-guide-docx: check-deps
	@guide_file="$(JOURNAL_GUIDE)"; \
	 if [ ! -f "$$guide_file" ]; then \
	     echo "✗ Error: Journal guide file not found: $$guide_file"; \
	     exit 1; \
	 fi; \
	 mkdir -p "$(JOURNAL_GUIDE_OUTPUT)"; \
	 output_docx="$(JOURNAL_GUIDE_OUTPUT)/journal-guide.docx"; \
	 echo "========================================================"; \
	 echo "  Generating Journal Submission Guide DOCX"; \
	 echo "========================================================"; \
	 echo "Input: $$guide_file"; \
	 echo "Output: $$output_docx"; \
	 echo ""; \
	 if pandoc "$$guide_file" -o "$$output_docx" \
		--toc --toc-depth=2 \
		--reference-doc=$(REFERENCE_DOCX) \
		--highlight-style=tango; then \
	     echo ""; \
	     echo "✓ Journal guide DOCX created: $$output_docx"; \
	     ls -lh "$$output_docx"; \
	     echo "  Open with: xdg-open $$output_docx"; \
	     echo "========================================================"; \
	 else \
	     echo ""; \
	     echo "✗ Error creating journal guide DOCX"; \
	     exit 1; \
	 fi

# Clean generated files
audio: $(INPUT)
	@echo "Generating audio files (IT/EN) from $(INPUT)"
	@cd scripts/audio && ./play_audio.sh "$(abspath $(INPUT))"

clean:
	@echo "Cleaning generated files..."
	@rm -rf \
		$(OUTPUT_BASE_DIR)/$(BUILD_PREFIX)-* \
		$(OUTPUT_BASE_DIR)/$(INPUT_BASENAME)-* \
		$(OUTPUT_BASE_DIR)/$(BUILD_PREFIX)_* \
		$(OUTPUT_BASE_DIR)/$(INPUT_BASENAME)_*
	@rm -rf $(OUTPUT_BASE_DIR)/latex $(OUTPUT_BASE_DIR)/pdf $(OUTPUT_BASE_DIR)/word $(JOURNAL_GUIDE_OUTPUT)
	@echo "✓ Clean complete"

# Watch for changes (requires entr)
watch:
	@which entr > /dev/null || (echo "Install entr: sudo apt-get install entr" && exit 1)
	@echo "Watching $(INPUT) for changes..."
	@echo "Press Ctrl+C to stop"
	@echo $(INPUT) | entr make pdf

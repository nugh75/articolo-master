# Project Summary: AI in Education Article

> **Project Version**: 2.0 (Reorganized structure - October 2025)

## 📄 Article Information

**Title:** Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students

**Alternate Title:** Balancing Trust and Uncertainty: Human Factors in the Adoption of AI in Education

**Authors:**
- Daniele Dragoni
- Rino Falcone
- Elisa Colì
- Isabella Poggi
- Daniele Caligiore

**Source:** Conference presentation at Palermo, October 10-11, 2025

## 📊 Research Overview

### Key Findings

- **80% of students** use AI daily vs. significantly lower teacher adoption
- **Competence paradox**: High practical skills (4.32/7) but low theoretical understanding (3.16/7)
- **Training inadequacy**: Students rate training at 3.3/7, teachers at 2.93/7 (28% say "not adequate at all")
- **Trust asymmetry**: Students more confident (4.47) than teachers (4.12) in AI integration
- **Teacher concerns**: 4.71/7 concern about students' responsible use (60% high values)
- **Third-person bias**: Teachers predict AI will change teaching (5.45) but less their own teaching (4.68)

### Research Approach

- **Mixed-methods** investigation (quantitative data presented, qualitative ongoing)
- **Participants**: Students (n=269), Current Teachers (n=308), Future Teachers (n=100)
- **Tool**: Mirror questionnaires for students and teachers
- **Innovation**: "Vibe-research" approach with AI-assisted dashboard

## 📁 New Project Structure (v2.0)

```
articolo/
├── bridging-the-gap-article-draft.md              ⭐ Main article (Markdown)
├── README.md                     📖 Project documentation
├── Makefile                      🔧 Build system
│
├── sources/                      📚 Source materials
│   ├── presentations/           # PowerPoint & PDF
│   ├── notes/                   # Schema & discorso
│   └── extracted/               # PPTX data
│
├── references/                   📖 Bibliography
│   ├── references.bib           # 27 references (BibTeX)
│   ├── references.ris           # 28 references (RIS)
│   ├── apa.csl                  # Citation style
│   └── references_summary.md
│
├── assets/                       🖼️ Media assets
│   └── figures/
│       ├── published/          # Figure pronte per l'articolo
│       └── manifest.csv
│
├── templates/                    📄 LaTeX templates
│   └── template_latex.tex
│
├── scripts/                      🔧 Script e tool
│   ├── conversion/             # md_to_latex, detect_citeproc, ris_to_bibtex, ecc.
│   ├── analysis/               # publish_figures, chart helpers
│   ├── language/               # marcatori bilingue
│   ├── audio/                  # Edge TTS
│   └── legacy/                 # convert_to_pdf.*, strumenti storici
│
├── output/                       📦 Generated files
│   ├── latex/                  # LaTeX output
│   ├── pdf/                    # PDF output
│   └── word/                   # Word output
│
└── docs/                         📚 Documentation
    ├── guides/ (conversione, LaTeX, installazione)
    ├── analysis/ (report e output)
    ├── workflows/ (notebook, testing, word styles)
    ├── reference/ (Zotero, Better BibTeX)
    └── PROJECT_SUMMARY.md (this file)
```

## 📂 Core Files

### Article Files

| File | Location | Description | Size |
|------|----------|-------------|------|
| bridging-the-gap-article-draft.md | `/` (root) | **Main article** in Markdown | 66 KB |
| schema_articolo.md | `sources/notes/` | Article structure template | 10 KB |
| discorso_palermo.md | `sources/notes/` | Original Italian presentation | 27 KB |

### Reference Files

| File | Location | Description | Count |
|------|----------|-------------|-------|
| references.bib | `references/` | BibTeX bibliography | 27 refs |
| references.ris | `references/` | RIS format (Zotero) | 28 refs |
| apa.csl | `references/` | APA 7th citation style | - |
| references_summary.md | `references/` | Reference summary | - |

### Source Materials

| Type | Location | Files |
|------|----------|-------|
| Presentations | `sources/presentations/` | PPTX + PDF |
| Notes | `sources/notes/` | 2 Markdown files |
| Extracted data | `sources/extracted/` | pptx_extract/ |
| Images | `assets/figures/published/` | 38 images |

### Conversion Tools

| Tool | Location | Type | Purpose |
|------|----------|------|---------|
| md_to_latex.py | `scripts/conversion/` | Python | **Main converter** MD → LaTeX |
| detect_citeproc.py | `scripts/conversion/` | Python | Autodetect citeproc support (build targets) |
| postprocess_docx_tables.py | `scripts/conversion/` | Python | Fixes DOCX tables after export |
| ris_to_bibtex.py | `scripts/conversion/` | Python | RIS → BibTeX |
| publish_figures.py | `scripts/analysis/` | Python | Copia gli export in `assets/figures/published/` |
| makefile | `/` (root) | Make | Build automation (`make latex`, `make pdf`, ecc.) |
| convert_to_pdf.py / .sh | `scripts/legacy/` | Python / Bash | Converter storici (non più usati) |

### Templates

| File | Location | Purpose |
|------|----------|---------|
| template_latex.tex | `templates/` | Custom LaTeX template with preambolo |

### Documentation

| File | Purpose |
|------|---------|
| README.md (root) | **Main project documentation** |
| CONVERSION_GUIDE.md | Quick conversion reference |
| README_LATEX.md | Complete LaTeX guide |
| QUICK_START_LATEX.md | 3-step quick start |
| README_CONVERSION.md | Overview of conversion methods |
| INSTALLATION_NEEDED.md | Dependencies |
| PROJECT_SUMMARY.md | This file |
| REORGANIZATION_SUMMARY.md | v2.0 reorganization details |

## 🎯 Article Structure

### 1. Introduction
- Paradox: 80% students use AI, but inadequate training
- GenAI as revolutionary technology (Munari's creativity framework)
- Jenkins' participatory culture and informal learning
- EU AI Act: education as high-risk domain

### 2. Theoretical Framework
- Mixed-methods convergent parallel design
- Model of mind and social behavior (Castelfranchi et al.)
- Trust in educational AI integration (Castelfranchi & Falcone)

### 3. Materials and Methods
- Mixed-methods design with "vibe-research"
- Questionnaire domains: demographics, perceptions, usage, qualitative
- Participants from Italian education
- AI-assisted research methodology

### 4. Results
- **3.1** Participant demographics (3 groups, female majority)
- **3.2** AI usage patterns (80% students vs. lower teachers, ChatGPT dominance)
- **3.3** Perceived competence (practical-theoretical gap)
- **3.4** Training adequacy (widespread dissatisfaction)
- **3.5** Perceived impact (third-person bias)
- **3.6** Trust and concerns (asymmetry, paradox)
- **3.7** Student-specific perceptions

### 5. Discussion
- **4.1** Massive adoption without institutional engagement
- **4.2** Competence paradox: knowing how without understanding why
- **4.3** Institutional training void
- **4.4** Third-person bias and resistance
- **4.5** Trust paradox
- **4.6** Educational theory implications
- **4.7** Urgency of systematic intervention

### 6. Conclusion
- Current state challenges
- Risks of inaction vs. opportunities
- Path forward: building pedagogy of AI
- Call to action for all stakeholders

## 🚀 Quick Start

### Convert to LaTeX

```bash
make latex
```

### Compile to PDF

```bash
cd output/latex
pdflatex article_draft.tex
```

### Full Workflow

```bash
# Edit article
nano bridging-the-gap-article-draft.md

# Convert
make latex

# Compile
cd output/latex && pdflatex article_draft.tex

# View
xdg-open article_draft.pdf
```

## 📖 Key References

### Theoretical Frameworks

- **Bandura (1977, 1986)** - Social cognitive theory, self-efficacy
- **Castelfranchi & Falcone (2010, 2017)** - Trust theory
- **Jenkins et al. (2006, 2009, 2015)** - Participatory culture
- **Munari (2024)** - Creativity and recombination

### Technology Acceptance

- **Davis (1989)** - Technology Acceptance Model (TAM)
- **Venkatesh & Davis (2000, 2003)** - TAM extensions, UTAUT

### Current Research

- **Freeman (2025)** - 92% UK students using GenAI
- **Pew Research (2025)** - Teen ChatGPT usage doubled
- **Schwartz et al. (2024)** - US teacher/principal AI adoption
- **European Union (2024)** - AI Act, education as high-risk

## 📊 Project Statistics

- **Total files**: 71
- **Source documents**: 2 MD files (article + notes)
- **Source materials**: 4 files (presentations + notes)
- **Images**: 38 files
- **Bibliography**: 27 BibTeX entries
- **Scripts**: 4 tools
- **Documentation**: 7 MD files
- **Output files**: 7 (LaTeX + Word)

## 🔄 Version History

- **v2.0** (Oct 2025) - Complete reorganization with granular structure
- **v1.x** (Oct 2025) - Initial article development
- **v1.0** - Conference presentation (Palermo)

## 📝 Citation Recommendations

When citing this research:

> Dragoni, D., Falcone, R., Colì, E., Poggi, I., & Caligiore, D. (2025). Bridging the Gap: Trust, Competence, and Concern in the Integration of AI among Teachers and Students. Presented at [Conference Name], Palermo, Italy.

## 🔗 Related Documentation

- [README.md](../README.md) - Main project README
- [CONVERSION_GUIDE.md](CONVERSION_GUIDE.md) - Conversion quick reference
- [README_LATEX.md](README_LATEX.md) - LaTeX documentation
- [REORGANIZATION_SUMMARY.md](../REORGANIZATION_SUMMARY.md) - v2.0 changes

---

**Last Updated**: October 18, 2025
**Project Status**: Active development
**Structure Version**: 2.0

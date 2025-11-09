# Documentation Index

> **Project**: AI in Education Article
> **Version**: 2.0 (Reorganized structure)
> **Last Updated**: October 18, 2025

## 📚 Documentation Overview

This folder contains all project documentation. Start here to find what you need.

## 🚀 Getting Started

**Need guidance?** Start here:

1. **[../README.md](../README.md)** – Project overview (big picture + workflow)
2. **[docs/guides/QUICK_START_LATEX.md](guides/QUICK_START_LATEX.md)** – 3-command quick start
3. **[docs/guides/INSTALLATION_NEEDED.md](guides/INSTALLATION_NEEDED.md)** – Software dependencies checklist

## 📁 Documentation Structure

| Section | Contents | Key Files |
| --- | --- | --- |
| **Guides** | Conversion, LaTeX, installation walkthroughs | `docs/guides/README_CONVERSION.md`, `CONVERSION_GUIDE.md`, `README_LATEX.md`, `QUICK_START_LATEX.md`, `INSTALLATION_NEEDED.md` |
| **Analysis** | Statistical summaries and output logs | `docs/analysis/AI_USAGE_ANALYSIS_SUMMARY.md`, `LIKERT_DIMENSIONS_ANALYSIS.md`, `USAGE_PATTERNS_OUTPUTS.md`, `MULTILINGUAL_*` |
| **Workflows** | Notebook, testing, documentation maintenance, Word styles | `docs/workflows/NOTEBOOK_CELLS_GUIDE.md`, `LANGUAGE_MARKING_PROGRESS.md`, `TESTING_SUMMARY.md`, `word_styles.md`, `DOCUMENTATION_UPDATE_SUMMARY.md` |
| **Reference & bibliography** | Zotero, Better BibTeX guidance | `docs/reference/ZOTERO_GUIDE.md`, `ZOTERO_CHEATSHEET.md`, `BETTER_BIBTEX_SETUP.md` |
| **Summaries** | Executive/organizational history | `docs/PROJECT_SUMMARY.md`, `docs/REORGANIZATION_SUMMARY.md` |

## 📘 Guides (conversion + templates)

- **[docs/guides/CONVERSION_GUIDE.md](guides/CONVERSION_GUIDE.md)** – Full conversion cookbook (make, pandoc, pdf, html, docx).
- **[docs/guides/README_CONVERSION.md](guides/README_CONVERSION.md)** – High-level conversion index with migration table.
- **[docs/guides/README_LATEX.md](guides/README_LATEX.md)** – Deep dive on template customizations, citations, multi-language export.
- **[docs/guides/QUICK_START_LATEX.md](guides/QUICK_START_LATEX.md)** – Three-command quick start and cheatsheet for common options.
- **[docs/guides/INSTALLATION_NEEDED.md](guides/INSTALLATION_NEEDED.md)** – Software prerequisites, tips, environment checks.

## 📈 Analysis & Outputs

- **[docs/analysis/AI_USAGE_ANALYSIS_SUMMARY.md](analysis/AI_USAGE_ANALYSIS_SUMMARY.md)** – Executive summary of survey-based use patterns.
- **[docs/analysis/LIKERT_DIMENSIONS_ANALYSIS.md](analysis/LIKERT_DIMENSIONS_ANALYSIS.md)** – Interpretation of Likert dimensions, correlations, and significance.
- **[docs/analysis/USAGE_PATTERNS_OUTPUTS.md](analysis/USAGE_PATTERNS_OUTPUTS.md)** – Raw outputs, CSV references, statistical tables.
- **[docs/analysis/MULTILINGUAL_EXPORT.md](analysis/MULTILINGUAL_EXPORT.md)** – How multilingual export works.
- **[docs/analysis/MULTILINGUAL_SYSTEM_SUMMARY.md](analysis/MULTILINGUAL_SYSTEM_SUMMARY.md)** – Status report for the multilingual pipeline.

## ⚙️ Workflows & Maintenance

- **[docs/workflows/NOTEBOOK_CELLS_GUIDE.md](workflows/NOTEBOOK_CELLS_GUIDE.md)** – Cell-by-cell walkthrough of `notebooks/analisi_dati.ipynb`.
- **[docs/workflows/LANGUAGE_MARKING_PROGRESS.md](workflows/LANGUAGE_MARKING_PROGRESS.md)** – Tracking multilingual markup and updates.
- **[docs/workflows/word_styles.md](workflows/word_styles.md)** – Pandoc reference DOCX and styling workflow for Word exports.
- **[docs/workflows/TESTING_SUMMARY.md](workflows/TESTING_SUMMARY.md)** – End-to-end testing report.
- **[docs/workflows/DOCUMENTATION_UPDATE_SUMMARY.md](workflows/DOCUMENTATION_UPDATE_SUMMARY.md)** – Notes on the v2.0 documentation update process and verification.

## 📚 Reference & Bibliography

- **[docs/reference/ZOTERO_GUIDE.md](reference/ZOTERO_GUIDE.md)** – Zotero workflow for the project.
- **[docs/reference/ZOTERO_CHEATSHEET.md](reference/ZOTERO_CHEATSHEET.md)** – Quick Zotero cheatsheet.
- **[docs/reference/BETTER_BIBTEX_SETUP.md](reference/BETTER_BIBTEX_SETUP.md)** – Better BibTeX sync notes.

## 🏁 Summaries & History

- **[docs/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** – Project goals, structure, and research context.
- **[docs/REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md)** – Timeline and results of the v2.0 reorganization.

## 🎯 Common Tasks

**Convert Markdown to LaTeX** → Start with [docs/guides/QUICK_START_LATEX.md](guides/QUICK_START_LATEX.md) and refer to [docs/guides/CONVERSION_GUIDE.md](guides/CONVERSION_GUIDE.md) for all options.

**Customize the template** → See [docs/guides/README_LATEX.md](guides/README_LATEX.md).

**Install dependencies** → Follow [docs/guides/INSTALLATION_NEEDED.md](guides/INSTALLATION_NEEDED.md).

**Understand the project** → Read [docs/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) and keep `assets/figures/README.md`/`analysis/README.md` on hand.

**Manage references** → Use [docs/reference/ZOTERO_GUIDE.md](reference/ZOTERO_GUIDE.md) plus [docs/reference/BETTER_BIBTEX_SETUP.md](reference/BETTER_BIBTEX_SETUP.md).

**Run the notebook** → Use [docs/workflows/NOTEBOOK_CELLS_GUIDE.md](workflows/NOTEBOOK_CELLS_GUIDE.md), then publish graphs following `scripts/analysis/publish_figures.py`.

## 🔧 Quick Commands

```bash
make latex
make pdf
make html
make docx
make clean
make help
make check-deps
```

## 📝 Additional Notes

- All documentation is now grouped by function to make it easier to maintain.
- Files in `docs/guides/` describe user-facing workflows; the rest are supporting analysis, operations, or reference docs.
- If you add a new doc, pick the correct directory and update this index.

## 📌 Recent Updates

- Reorganized docs into `analysis/`, `guides/`, `workflows/`, and `reference/`.
- Updated all paths to the new `assets/figures/published/` + `scripts/` layout.
- Added this index to explain the new structure.

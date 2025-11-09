# References Workflow

Contain every bibliography-related asset here so the conversion scripts can find them automatically:

- `references.ris` → import/export file from your reference manager
- `references.bib` → BibTeX file consumed by Pandoc/LaTeX
- `apa.csl` → default citation style (feel free to replace it with any other CSL file)

Run `make bib` whenever you update the RIS file to refresh `references.bib`. The make target calls `scripts/conversion/ris_to_bibtex.py` for you.

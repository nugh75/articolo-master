# DOCX Collaboration Dropzone

Use this folder to temporarily store documents exported from Google Docs, Word Online or any other collaborative editor before importing them back into Markdown.

## Suggested workflow

1. Download the DOCX you want to merge and place it here (e.g. `collab/review-round-01.docx`).
2. Import it into your source file:
   ```bash
   python scripts/analysis/docx_sync.py collab/review-round-01.docx \
     --target article-template.md
   ```
3. The script keeps the original front matter, overwrites the body with the Pandoc conversion, and automatically creates a timestamped backup.
4. Remove obsolete DOCX files periodically to keep the folder tidy.

You can version-control this folder or add selective `.gitignore` rules if your documents are large.

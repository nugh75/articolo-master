# Figure Management

Use this folder to track the evolution of visual assets referenced by your articles.

- `assets/figures/published/` contains only the figures that are already referenced in Markdown. Keep the folder clean by promoting assets here only when they are final.
- Store work-in-progress charts, screenshots or design files anywhere else (e.g. inside `analysis/exports` or an untracked `assets/figures/drafts/`).
- `scripts/analysis/publish_figures.py` expects to find source files with the same relative path under your analysis exports and will regenerate `assets/figures/manifest.csv` for you.

Feel free to add more subfolders (per section, per figure type, per language) as long as the Markdown paths keep starting with `assets/figures/published/`.

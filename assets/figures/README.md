# Figures

Questa sezione contiene le immagini pronte per la pubblicazione utilizzate in `bridging-the-gap-article-draft.md`.

```
assets/figures/
├── published/        # Copie curate dei grafici referenziati nell'articolo
└── manifest.csv      # Mappa figure_id → file pubblicato + origine export
```

- I file in `published/` sono organizzati seguendo la stessa gerarchia dell'export (`analysis/exports/latest`) ma includono solo i grafici effettivamente citati.
- `manifest.csv` tiene traccia dell'associazione fra ID della figura (es. `#fig:age-violin-it`), percorso pubblicato e sorgente originale, semplificando refresh e audit.

## Aggiornare le figure
1. Eseguire il notebook per rigenerare i grafici desiderati (`analysis/exports/latest/...`).
2. Lanciare `python scripts/analysis/publish_figures.py --article <file.md> [--article <altro.md>]` per copiare i file aggiornati in `assets/figures/published/` e rigenerare il manifesto. Se non passi alcun file, lo script usa `bridging-the-gap-article-draft.md` di default.
   ```bash
   python scripts/analysis/publish_figures.py \
     --article bridging-the-gap-article-draft.md \
     --article nuovo-articolo.md
   ```
3. Verificare che l'articolo compili e che le immagini puntino al percorso pubblicato (prefisso `assets/figures/published/`).

> Nota: non modificare manualmente i file in `published/`; usare sempre lo script per garantire coerenza con il manifesto.

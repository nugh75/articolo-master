# Analysis Exports

La cartella `analysis/exports/` contiene tutti i file generati automaticamente dal notebook `notebooks/analisi_dati.ipynb` e da eventuali script statistici.

```
analysis/exports/
├── run-2025-11-08/   # Snapshot dell'ultima esecuzione completa
└── latest -> run-2025-11-08
```

- **Snapshots (`run-YYYY-MM-DD`):** copie datate degli output (PNG, SVG, CSV) utili per tracciare cosa è stato pubblicato in una determinata versione dell'articolo.
- **`latest` (symlink):** puntatore aggiornato all'export valido che gli script usano di default. Il notebook scrive sempre qui, quindi è sufficiente cambiare il collegamento simbolico per congelare un risultato e iniziare un nuovo ciclo.

## Workflow suggerito
1. Eseguire il notebook con le modifiche desiderate: gli artefatti finiscono in `analysis/exports/latest`.
2. Quando i risultati sono approvati, rinominare `analysis/exports/latest` in `analysis/exports/run-YYYY-MM-DD` e creare un nuovo symlink `latest` che punti allo snapshot definitivo.
3. Eseguire `scripts/analysis/publish_figures.py` (o il comando documentato nel README) per aggiornare `assets/figures/published` e il relativo manifesto.

I path sono definiti in `config/paths.json`, quindi eventuali modifiche future (es. spostare gli export fuori dal repository) richiedono una sola modifica di configurazione.

# Data Directory

Questa cartella raccoglie tutte le fonti di dati utilizzate per l'analisi descritta nell'articolo.

```
data/
├── raw/          # Dati originali non modificati
│   └── surveys/  # Questionari CNR (studenti / insegnanti)
├── interim/      # Estratti e dataset intermedi generati dai notebook
└── processed/    # Output consolidati pronti per la pubblicazione (placeholder)
```

## raw/surveys
- `Insegnati - Questionario - CNR-solo chiuse.xlsx`
- `Studenti - Questionario -CNR - solo chiuse.xlsx`

Questi file vengono letti da `notebooks/analisi_dati.ipynb`. Non vanno modificati direttamente; se arrivano nuove versioni, conservarle qui mantenendo la nomenclatura o documentando la variazione in questo README.

## interim
Destinato a CSV/JSON intermedi (es. `combined_insegnanti_studenti.csv`, estratti delle domande). Il notebook e gli script possono salvare qui gli output condivisi che devono essere riutilizzati senza ricreare i grafici.

## processed
Slot per dataset finali da pubblicare (ad es. tabelle pulite che accompagnano l'articolo). Al momento è vuoto; riempirlo solo con file revisionati.

> Nota: i percorsi vengono centralizzati in `config/paths.json` e letti dai notebook, così eventuali modifiche future richiedono l'aggiornamento di un unico file di configurazione.

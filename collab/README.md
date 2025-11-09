# Cartella Collaborazione DOCX

Usa questa cartella per salvare i DOCX esportati da Google Docs (o altri editor condivisi) prima di importarli nel Markdown sorgente.

## Workflow suggerito

1. Scarica da Google Drive il file aggiornato e salvalo qui, es. `collab/versione_google_2025-11-09.docx`.
2. Importa le modifiche nel Markdown eseguendo:
   ```bash
   python scripts/analysis/docx_sync.py collab/versione_google_2025-11-09.docx \
     --target bridging-the-gap-article-draft.md
   ```
3. Lo script creerà un backup del Markdown originale (`*.backup.<timestamp>`) e sovrascriverà il corpo con la conversione Pandoc.
4. Dopo aver verificato le differenze, elimina eventuali DOCX obsoleti da questa cartella per evitare confusione.

> Nota: la cartella è versionata per tracciare quali documenti sono stati importati. Se i file diventano voluminosi, puoi aggiungere regole mirate al `.gitignore` o mantenere solo l'ultima versione utile.

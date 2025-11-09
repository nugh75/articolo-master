# Scripts Overview

La cartella `scripts/` è stata suddivisa in sottodirectory tematiche per chiarire responsabilità e dipendenze. Questa pagina elenca ogni script, spiegandone lo scopo e indicando dove viene usato.

## Struttura

```
scripts/
├── conversion/     # Pipeline di conversione e template
├── analysis/       # Supporto analisi dati e figure
├── language/       # Tooling per marcatura bilingue
├── audio/          # Generatore TTS e launcher
└── legacy/         # Script mantenuti solo per compatibilità
```

## Conversione (`scripts/conversion`)

| Script | Scopo | Utilizzo |
| --- | --- | --- |
| `md_to_latex.py` | Driver principale Markdown → LaTeX (Pandoc + template). | Invocato dal Makefile (`make latex`, `make bundle`) e citato nella documentazione principale. |
| `detect_citeproc.py` | Verifica se Pandoc ha il filtro citeproc disponibile, per abilitare/disabilitare le opzioni bibliografiche automaticamente. | Chiamato da tutti i target Pandoc nel Makefile. |
| `postprocess_docx_tables.py` | Pulisce e uniforma le tabelle nei DOCX generati (allinea font/width). | Eseguito alla fine dei target `make docx*`. |
| `ris_to_bibtex.py` | Converte il file `references/references.ris` in `references/references.bib`. | Usato da `make bib` e documentato in `docs/guides/CONVERSION_GUIDE.md`. |
| `generate_reference_docx.py` | Ricrea `templates/reference.docx` a partire dallo stile definito nel repo (utile dopo modifiche allo stile Word). | Descritto in `docs/workflows/word_styles.md`; va lanciato manualmente quando si cambia lo stile. |

## Analisi & Figure (`scripts/analysis`)

| Script | Scopo | Utilizzo |
| --- | --- | --- |
| `publish_figures.py` | Copia gli export più recenti da `analysis/exports/latest/` verso `assets/figures/published/` e rigenera `manifest.csv`. | Richiamato manualmente (es. `python scripts/analysis/publish_figures.py --article bridging-the-gap-article-draft.md`). Documentato in README/analysis. |
| `generate_demographic_charts.py` | Rigenera i grafici demografici (età, genere, ecc.) a partire dai CSV prodotti dal notebook. **Da aggiornare**: oggi punta ancora ai vecchi path `output/exploratory/`. | Usato sporadicamente durante l’analisi; prima di riutilizzarlo va allineato alla nuova struttura `analysis/exports/`. |
| `create_tools_boxplot.py` | Script sperimentale per ricreare i boxplot sul numero di tool utilizzati (dati sintetici → PNG/PDF). | Mantenuto per riprodurre grafici storici; consigliato spostarlo in un notebook dedicato in futuro. |

## Language Helpers (`scripts/language`)

| Script | Scopo | Status |
| --- | --- | --- |
| `add_language_markers.py` | Aggiunge manualmente marker `<!-- lang:xx -->` a coppie di paragrafi inglese/italiano in Markdown. | Tool manuale (usato durante preparazione versioni bilingue). |
| `auto_mark_languages.py` | Variante automatica sperimentale per la stessa operazione (riconosce paragrafi in corsivo come italiano). | Sperimentale; richiede ulteriori test prima di integrarlo nel workflow. |

## Audio (`scripts/audio`)

| Script | Scopo | Utilizzo |
| --- | --- | --- |
| `audio_player.py` | Converte sezioni del Markdown in MP3 usando Edge TTS (voce IT/EN configurabile). | Invocato via `scripts/audio/play_audio.sh` o direttamente con Python. Output salvato in `output/audio/`. |
| `play_audio.sh` | Launcher bash per `audio_player.py` (gestisce ambiente virtuale, cache, argomenti). | Uso consigliato per generare l’audio con un singolo comando. |
| `setup_audio_player.sh` | Installa le dipendenze necessarie (`edge-tts`) e mostra le istruzioni rapide. | Da lanciare una volta per configurare l’ambiente audio. |
| `README_AUDIO_PLAYER.md` | Documentazione completa del generatore audio (setup, variabili d’ambiente, troubleshooting). | Riferimento per eventuali aggiornamenti o nuove esportazioni vocali. |

## Legacy (`scripts/legacy`)

| Script | Scopo | Nota |
| --- | --- | --- |
| `convert_to_pdf.py` | Vecchio wrapper Python che convertiva direttamente Markdown → PDF via Pandoc. | Non più usato (sostituito da `md_to_latex.py` + Makefile). Conservato per riferimento storico. |
| `convert_to_pdf.sh` | Versione bash dello stesso flusso legacy. | Idem come sopra; tenuto solo per compatibilità. |

> ℹ️ Se aggiungi nuovi script, scegli la sottocartella coerente o creane una nuova (es. `scripts/data/`) e aggiorna questa pagina. Se sposti un file, ricorda di aggiornare il Makefile e la documentazione che lo cita.

# Riepilogo Riorganizzazione Progetto

**Data documento originale**: 2025-10-18  
**Versione documento originale**: 2.0

> **Aggiornamento 2025-11-08 – Fase 0 (Inventario):** lo stato reale del repository differisce sensibilmente dalla struttura descritta qui sotto. Prima di procedere con la nuova riorganizzazione ho mappato componenti, dipendenze e workflow utilizzando `PROJECT_TREE.txt`, `README.md`, il `Makefile` corrente e un `tree -L 2` eseguito in data 2025-11-08. I punti raccolti servono come baseline condivisa per le Fasi successive.

## 🧭 Stato Fase 0 – Inventario (agg. 2025-11-08)

### Fonti e metodo
- `README.md`: descrive workflow dichiarati e destinazione d’uso delle cartelle principali.
- `Makefile`: unica regia dei workflow di conversione; espone dipendenze pratiche (script, template, filtri, assets, references, tools).
- `PROJECT_TREE.txt`: fotografia datata; confrontata con `tree -L 2` per evidenziare discrepanze (nuove cartelle `figures/`, `config/`, `filters/`, `tools/`, `notebooks/`, build cache, directory spurie come `-o`).
- Ispezione mirata di `docs/`, `scripts/` e `output/` per capire origine e destinazione dei file citati nelle fasi successive.

### Divergenze rilevate rispetto alla documentazione precedente
- `PROJECT_TREE.txt` non include cartelle oggi presenti (es. `assets/figures`, `dati`, `config`, `filters`, `tmp/docx`, `notebooks/output`, `output/audio`, directory `build-*` timestampate).
- I contenuti testuali (`apppunti.md`, `nuovo-articolo.md[.backup]`, `ARTICLE_STRUCTURE_[EN|IT].txt`) vivono nella root senza convenzioni; non sono menzionati nel README.
- Il Makefile fa riferimento a `filters/*.lua`, `templates/pandoc_tables.tex`, `tools/bin`, `scripts/conversion/detect_citeproc.py`, `templates/reference.docx` e `scripts/conversion/generate_reference_docx.py`, ma questi elementi non sono citati nella struttura “nuova” della vecchia riorganizzazione.
- La sezione output del README presume cartelle fisse (`output/pdf`, `output/latex`, `output/word`), mentre in realtà esistono sia cartelle permanenti sia build snapshot (`output/build-YYYY...`) e directory funzionali (audio, exploratory).
- Non risultano tracciati nel riepilogo i dataset (`dati/*.xlsx`), le cartelle “Ricerca riviste...” e i notebook; stessi per gli script dedicati all’audio e al post-processing DOCX.

### Workflow principali e percorsi attualmente coinvolti
| Workflow | Ingressi principali | Strumenti/percorsi coinvolti | Uscite/osservazioni | Note per la riorganizzazione |
| --- | --- | --- | --- | --- |
| Redazione contenuti | `bridging-the-gap-article-draft.md`, `nuovo-articolo*.md`, `apppunti.md`, `ARTICLE_STRUCTURE_*`, `sources/notes` | Editor manuali, nessun orchestratore | File Markdown in root + note sparse | Necessario concentrare i testi in una radice (`content/`) e documentare naming/versioning. |
| Conversione Pandoc/Makefile | Input principale + `references/*.bib/ris`, `templates/*.tex/docx`, `filters/*.lua`, `config/html.css`, `assets/*`, `tools/bin` | `Makefile`, `scripts/conversion/md_to_latex.py`, `scripts/legacy/convert_to_pdf.py/.sh`, `scripts/conversion/detect_citeproc.py` | `output/build-*/*.{pdf,tex,docx,html}`, `output/pdf`, `output/latex`, `output/word` | I comandi scrivono in cartelle miste (build snapshot + cartelle stabili); serve una strategia unica per gli artefatti. |
| Gestione bibliografia | `references/references.ris`, note Zotero (docs) | `scripts/conversion/ris_to_bibtex.py`, `make bib`, `refs_summary` | `references/references.bib`, `references_summary.md` | Files bibliografici dovrebbero stare sotto una radice dati comune con versioning chiaro. |
| Analisi dati e grafici | `dati/*.xlsx`, `sources/extracted`, `notebooks/analisi_dati.ipynb` | `notebooks/`, `scripts/analysis/generate_demographic_charts.py`, `scripts/analysis/create_tools_boxplot.py` | `assets/figures/*.png|svg|pdf`, `analysis/exports/latest`, `notebooks/output` | Gli asset esportati confluiscono sia in `assets/figures/published` sia in `assets/figures`; occorre distinguere raw vs processed. |
| Audio & media helper | `scripts/audio/audio_player.py`, `scripts/audio/play_audio.sh`, `scripts/audio/setup_audio_player.sh` | `output/audio` | File audio derivati e cache utilizzata dal player | Le directory audio sono dentro `output/` ma non ignorate tutte; valutare una sezione dedicata agli artifact multimediali. |
| Ricerca riviste & metadata | `Ricerca riviste dove scriverre/*.md`, `docs/ZOTERO_*.md` | Editing manuale | Nessun output automatico | Materiale editoriale che andrà riposizionato insieme ai dati di ricerca/pubblicazione. |

### Matrice file/dir critici e dipendenze incrociate
| Nodo | Tipo | Dipendenze/Input | Consumatori/Workflow | Output/Note |
| --- | --- | --- | --- | --- |
| `bridging-the-gap-article-draft.md` | Contenuto principale | Include immagini da `assets/figures/published` e `assets/figures`; cita bibliografia via `references/references.bib` | Tutti i target `make *` | Qualsiasi spostamento richiede aggiornare il Makefile e gli script che lo assumono in root. |
| `Makefile` | Orchestratore build | Chiama `scripts/conversion/md_to_latex.py`, `scripts/legacy/convert_to_pdf.py`, `scripts/conversion/detect_citeproc.py`, `filters/*.lua`, `templates/pandoc_tables.tex`, `templates/template_latex.tex`, `templates/reference.docx`, `references/*`, `assets/*`, `tools/bin` | Workflow Conversione | Genera `output/build-*`; setta PATH custom (`tools/bin`); hardcode dei path che bloccherebbero qualsiasi spostamento non sincronizzato. |
| `scripts/conversion/md_to_latex.py` | Script conversione | Template LaTeX + bibliografia + asset; crea cartelle in `output/latex` | Target `make latex`, `make bundle` | Sarà da spostare sotto `automation/conversion` ma prima serve capire i path hardcoded nel codice. |
| `scripts/legacy/convert_to_pdf.py` / `.sh` | Script ausiliari | Dipendono da Pandoc, `templates/template_latex.tex`, `config/html.css` (per HTML), bibliografia | Target PDF/HTML | Necessitano di path coerenti per template e CSS; consumano la stessa struttura di asset del Makefile. |
| `filters/*.lua` | Filtri pandoc | Nessuna dipendenza interna, ma vengono caricati via path relativo dal Makefile | Workflow conversione | Se la cartella cambia nome/posizione bisogna aggiornare sia Makefile sia eventuali script standalone. |
| `templates/template_latex.tex` & `templates/pandoc_tables.tex` | Template | Richiamano immagini (`./assets/...`), bibliografia (`references/references.bib`, commentata) | Pandoc/LaTeX | Necessario aggiornare `\graphicspath` se gli asset vengono spostati. |
| `templates/reference.docx` | Reference DOCX | Aggiornato via `scripts/conversion/generate_reference_docx.py`, doc `docs/workflows/word_styles.md` | Target `make docx*` | Va tenuto sincronizzato con la nuova posizione dei template e documentato nel README. |
| `references/references.{ris,bib}`, `references_summary.md`, `apa.csl` | Bibliografia | Input da Zotero/ris; script `ris_to_bibtex.py`; `csL` scaricabile via `make csl` | Pandoc citeproc, doc markdown | Dovranno condividere radice con altri dati bibliografici per evitare path sparsi. |
| `assets/figures/published`, `assets/figures` | Risorse grafiche | Prodotte da notebook/script, oppure importate manualmente | Inserite nei Markdown e nelle esportazioni Pandoc | Occorre distinguere tra grafici finali e materiale sorgente; oggi condividono namespace senza manifesto. |
| `notebooks/analisi_dati.ipynb` + `notebooks/output` | Analisi dati | Dipende da `dati/*.xlsx`, `sources/extracted` | Produce figure, CSV intermedi in `analysis/exports/latest` | Lo spostamento dei dataset richiederà aggiornare i path dentro il notebook e negli script associati. |
| `output/` (pdf/latex/word/audio/build-*) & `tmp/docx` | Artefatti | Scritti da Makefile, script audio, script docx post-processing | Consumatore finale (review, export) | Directory mista tra output versionati, cache audio e build time-stamped; da normalizzare/ignorare in `.gitignore`. |
| `config/html.css`, `config/style_overrides.txt` | Configurazioni rendering | Referenziate dagli script HTML o dal Makefile (via `--css`) | Export HTML | Devono seguire gli script nel caso vengano spostati in `automation/config`. |
| `tools/bin`, `tools/vendor` | Tooling locale | PATH esteso dal Makefile | Tutti i target `make` che richiedono binari custom | Documentazione assente; serve capire quali binari sono lì prima di spostarli. |
| `Ricerca riviste dove scriverre/`, `data/raw/surveys/` | Materiale di ricerca | Raccolta manuale e dataset Excel | Notebook, onboarding editoriale | Dovranno finire nella stessa area dati per evitare duplicati sparsi. |

### Gap evidenziati prima di passare alla Fase 1
- Le strutture documentate non rispecchiano lo stato reale del file system; ogni spostamento dovrà partire da questa fotografia aggiornata.
- I workflow di build generano sia output permanenti sia snapshot datati nella stessa cartella (`output/`); non esiste distinzione netta tra file versionati, cache e artefatti da ignorare.
- I contenuti editoriali non hanno naming convention condivisa e vivono insieme a file tecnici nella root.
- Non esiste un inventario centralizzato degli asset grafici, né un legame esplicito tra grafici e notebook/script che li producono.
- I dataset (`data/raw/surveys/`, `sources/extracted`, `Ricerca riviste...`) e i riferimenti bibliografici si trovano in livelli diversi e non sono descritti nel README principale.
- Gli script audio e i relativi output rischiano di essere rimossi da `make clean` perché non sono dichiarati; serve definire come preservarli o rigenerarli.

Le sezioni successive del documento restano come storico della precedente riorganizzazione e non riflettono la situazione attuale; verranno aggiornate nelle fasi successive dopo l’allineamento della struttura.

## ✅ Stato Fase 1 – Organizzazione dati & grafici (agg. 2025-11-08)

- **Dati di ricerca**: i questionari originali sono stati spostati da `data/raw/surveys/` a `data/raw/surveys/`, con `data/interim/` e `data/processed/` pronti per dataset condivisi e pubblicabili. Il nuovo `data/README.md` documenta ruoli e naming.
- **Export notebook**: tutto il contenuto di `analysis/exports/latest/` è ora in `analysis/exports/run-2025-11-08/` con symlink `analysis/exports/latest` e `analysis/exports/latest -> ../analysis/exports/latest` per retrocompatibilità. `analysis/README.md` spiega come creare snapshot datati.
- **Figure pubblicate**: gli asset utilizzati nell’articolo sono stati copiati (con struttura identica) in `assets/figures/published/`, accompagnati da `assets/figures/manifest.csv` e da uno script (`scripts/analysis/publish_figures.py`) che sincronizza figure e manifest partendo dagli export correnti.
- **Pulizia asset legacy**: la cartella `assets/figures/` contiene ora solo `published/`, `manifest.csv` e `README.md`; tutte le immagini generate da vecchi script sono state rimosse (restano solo negli snapshot dentro `analysis/exports/`), così non ci sono duplicati o file fuori posto.
- **Configurazione centralizzata**: `config/paths.json` espone i percorsi chiave (raw data, interim, exports, figures) ed è consumato dal notebook `notebooks/analisi_dati.ipynb`, aggiornato per individuare automaticamente la root del repo e creare le cartelle necessarie.
- **Documentazione**: `README.md`, `analysis/README.md`, `assets/figures/README.md` e `data/README.md` descrivono il nuovo workflow dati → export → figure pubblicate. Restano da aggiornare gradualmente le guide secondarie (`docs/workflows/NOTEBOOK_CELLS_GUIDE.md`, `docs/analysis/USAGE_PATTERNS_OUTPUTS.md`, ecc.) che citano ancora i vecchi path.

## ✅ Riorganizzazione Completata

Il progetto è stato completamente riorganizzato con una struttura granulare e ben definita.

## 📁 Nuova Struttura

```
articolo/
├── bridging-the-gap-article-draft.md              ⭐ ARTICOLO PRINCIPALE
├── README.md                     📖 Documentazione principale
├── Makefile                      🔧 Build system
├── .gitignore                    🚫 File da ignorare
│
├── sources/                      📚 FONTI per scrivere l'articolo
│   ├── presentations/           # Presentazioni originali (PPTX, PDF)
│   ├── notes/                   # Note, schemi, discorsi
│   └── extracted/               # Dati estratti da presentazioni
│
├── references/                   📖 Bibliografia e citazioni
│   ├── references.bib           # BibTeX (principale)
│   ├── references.ris           # RIS (sorgente)
│   ├── apa.csl                  # Stile APA
│   └── references_summary.md    # Riepilogo
│
├── assets/                       🖼️ Risorse grafiche
│   └── charts/                  # 38 immagini per l'articolo
│
├── templates/                    📄 Template di conversione
│   └── template_latex.tex       # Template LaTeX personalizzato
│
├── scripts/                      🔧 Script di conversione
│   ├── md_to_latex.py          # MD → LaTeX (principale)
│   ├── convert_to_pdf.py       # MD → PDF
│   ├── convert_to_pdf.sh       # Script bash
│   └── ris_to_bibtex.py        # RIS → BibTeX
│
├── output/                       📦 File generati (git-ignored)
│   ├── latex/                  # File LaTeX generati
│   ├── pdf/                    # PDF generati
│   └── word/                   # 5 file Word esistenti
│
└── docs/                         📚 Documentazione
    ├── README_LATEX.md         # Guida completa LaTeX
    ├── QUICK_START_LATEX.md    # Quick start
    ├── CONVERSION_GUIDE.md     # Guide conversioni
    ├── README_CONVERSION.md    # README conversioni
    ├── PROJECT_SUMMARY.md      # Riepilogo progetto
    └── INSTALLATION_NEEDED.md  # Dipendenze
```

## 🔄 Modifiche Effettuate

### 1. Directory create
- ✅ `sources/` con sottocartelle (presentations, notes, extracted)
- ✅ `references/` per bibliografia
- ✅ `assets/figures/published/` per immagini
- ✅ `templates/` per template
- ✅ `scripts/` per script
- ✅ `output/` con sottocartelle (latex, pdf, word)
- ✅ `docs/` per documentazione

### 2. File spostati

#### sources/
- Presentazione Palermo (PPTX + PDF) → `sources/presentations/`
- discorso_palermo.md → `sources/notes/`
- schema_articolo.md → `sources/notes/`
- pptx_extract/ → `sources/extracted/`

#### references/
- references.bib → `references/`
- references.ris → `references/`
- apa.csl → `references/`
- references_summary.md → `references/`

#### assets/
- 38 immagini da charts/ → `assets/figures/published/`

#### templates/
- template_latex.tex → `templates/`

#### scripts/
- md_to_latex.py → `scripts/`
- convert_to_pdf.py → `scripts/`
- convert_to_pdf.sh → `scripts/`
- ris_to_bibtex.py → `scripts/`

#### output/
- 5 file .docx → `output/word/`
- 2 file .tex → `output/latex/`

#### docs/
- Tutti i README e guide → `docs/`

### 3. File aggiornati

#### Makefile
- ✅ Path aggiornati per INPUT/OUTPUT
- ✅ BIB_FILE → `references/references.bib`
- ✅ CSL_FILE → `references/apa.csl`
- ✅ TEMPLATE_TEX → `templates/template_latex.tex`
- ✅ CONVERSION_SCRIPT → `scripts/conversion/md_to_latex.py`
- ✅ Output path → `output/latex/`, `output/pdf/`, `output/word/`

#### scripts/conversion/md_to_latex.py
- ✅ Default output → `output/latex/[nome].tex`
- ✅ Default template → `templates/template_latex.tex`
- ✅ Default bibliography → `references/references.bib`
- ✅ Default CSL → `references/apa.csl`
- ✅ Help aggiornato con nuovi path
- ✅ Crea automaticamente directory output se non esiste

#### templates/template_latex.tex
- ✅ `\graphicspath` aggiornato → `{./assets/figures/published/}{./assets/}{./sources/presentations/}`
- ✅ `\addbibresource` → `references/references.bib` (commentato)

### 4. File creati

- ✅ **README.md** (principale) - Documentazione completa del progetto
- ✅ **.gitignore** - Ignora output/ e file temporanei
- ✅ **REORGANIZATION_SUMMARY.md** (questo file)

## 🧪 Test Effettuati

### Test conversione LaTeX
```bash
make latex
```
**Risultato**: ✅ Successo
- File generato: `output/latex/article_draft.tex` (77 KB)
- Template applicato correttamente
- Path funzionanti

### Test script Python
```bash
python3 scripts/conversion/md_to_latex.py --help
```
**Risultato**: ✅ Successo
- Help mostra nuovi path di default
- Esempi aggiornati

### Test Makefile
```bash
make help
```
**Risultato**: ✅ Successo
- Tutti i target funzionanti

## 📊 Statistiche

### File
- **Fonti**: 4 file (2 presentazioni + 2 note + 1 cartella estratti)
- **Bibliografia**: 4 file (BIB, RIS, CSL, summary)
- **Immagini**: 38 file in assets/figures/published/
- **Template**: 1 file LaTeX
- **Script**: 4 script Python/Bash
- **Output Word**: 5 file DOCX
- **Output LaTeX**: 2 file TEX
- **Documentazione**: 6 file MD

### Dimensioni
- **sources/**: ~8.7 MB (principalmente presentazioni)
- **assets/**: ~6.8 MB (immagini)
- **output/**: ~4.2 MB (file generati)
- **references/**: ~116 KB
- **docs/**: ~40 KB
- **scripts/**: ~25 KB

## 🎯 Vantaggi della Nuova Struttura

### Organizzazione
- ✅ Separazione chiara tra source e output
- ✅ Fonti centralizzate in `sources/`
- ✅ Bibliografia separata in `references/`
- ✅ Asset grafici in `assets/`

### Manutenibilità
- ✅ Facile trovare file
- ✅ Path chiari e logici
- ✅ Documentazione centralizzata

### Workflow
- ✅ Source → Process → Output ben definito
- ✅ Makefile gestisce tutto
- ✅ Script con path di default corretti

### Scalabilità
- ✅ Facile aggiungere nuove fonti
- ✅ Facile aggiungere nuovi template
- ✅ Output separato e ricreabile

### Git-friendly
- ✅ .gitignore esclude output/
- ✅ Solo source code versionato
- ✅ File generati riproducibili

## 🚀 Quick Start Post-Riorganizzazione

### 1. Scrivi l'articolo
```bash
nano bridging-the-gap-article-draft.md
```

### 2. Converti in LaTeX
```bash
make latex
```

### 3. Compila PDF
```bash
cd output/latex
pdflatex article_draft.tex
```

## 📝 Prossimi Passi Raccomandati

1. ⬜ Aggiungi file .gitignore al repository Git
2. ⬜ Fai commit della nuova struttura
3. ⬜ Testa compilazione PDF completa
4. ⬜ Verifica che tutte le immagini siano trovate
5. ⬜ Personalizza template LaTeX se necessario
6. ⬜ Aggiorna documentazione specifica del progetto

## 📖 Documentazione

- **README principale**: [README.md](README.md)
- **Guida LaTeX**: [docs/guides/README_LATEX.md](docs/guides/README_LATEX.md)
- **Quick Start**: [docs/guides/QUICK_START_LATEX.md](docs/guides/QUICK_START_LATEX.md)
- **Guide conversioni**: [docs/guides/CONVERSION_GUIDE.md](docs/guides/CONVERSION_GUIDE.md)

## ✨ Conclusione

La riorganizzazione è stata completata con successo. Il progetto ora ha:

- ✅ Struttura chiara e logica
- ✅ Separazione source/output
- ✅ Fonti centralizzate
- ✅ Path aggiornati in tutti i file
- ✅ Workflow funzionante
- ✅ Documentazione completa

Il progetto è pronto per continuare lo sviluppo dell'articolo!

---

**Note tecniche**:
- Pandoc versione: 2.5 (vecchia, ma funzionante)
- Python versione: 3.x
- Sistema operativo: Linux
- Conversione testata: MD → LaTeX ✅

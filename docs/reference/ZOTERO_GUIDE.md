# Guida Zotero per il Progetto Articolo

Guida completa per gestire le referenze bibliografiche usando Zotero in questo progetto.

---

## 🎯 Quick Start

### ⭐ Workflow Consigliato (Better BibTeX - Auto-Sync)

**Setup una volta sola** (vedi `docs/reference/BETTER_BIBTEX_SETUP.md`):
1. Installa Better BibTeX plugin
2. Configura auto-export della collezione Zotero

**Uso quotidiano:**
```bash
# 1. Modifica/aggiungi referenze in Zotero
#    → Sincronizzazione automatica! ✨

# 2. Genera documento
make bundle INPUT=nuovo-articolo.md OUTPUT_BASENAME=nuovo-articolo
```

### Workflow Alternativo (RIS → BibTeX Manuale)

```bash
# 1. Esporta da Zotero
#    File → Export Library/Collection
#    Format: RIS
#    Save: references/references.ris

# 2. Converti in BibTeX
make bib

# 3. Genera bundle con citazioni
make bundle INPUT=nuovo-articolo.md OUTPUT_BASENAME=nuovo-articolo
```

---

## 📚 Due Approcci Disponibili

### Approccio A: RIS + Script Python (Attuale)

**Pro:**
- ✅ Già configurato e funzionante
- ✅ Non richiede plugin Zotero
- ✅ Semplice e diretto

**Contro:**
- ❌ Manuale: devi riesportare ogni volta
- ❌ Citation keys potrebbero cambiare

**Workflow:**
1. Gestisci referenze in Zotero normalmente
2. Export → RIS format → `references/references.ris`
3. `make bib` converte in BibTeX con citation keys automatici
4. Usa nel documento markdown

### Approccio B: Better BibTeX (Consigliato per Ricerca Seria)

**Pro:**
- ✅ Auto-sync: modifiche in Zotero → aggiornamento automatico .bib
- ✅ Citation keys stabili e personalizzabili
- ✅ Workflow più professionale

**Contro:**
- ❌ Richiede installazione plugin
- ❌ Setup iniziale più complesso

**Setup:**

1. **Installa Better BibTeX:**
   - Download: https://retorque.re/zotero-better-bibtex/installation/
   - In Zotero: Tools → Add-ons → Install Add-on From File
   - Riavvia Zotero

2. **Configura Citation Key Format:**
   - Edit → Preferences → Better BibTeX → Citation keys
   - Formula: `[auth:capitalize][year][shorttitle3_3:capitalize]`
   - Esempi output:
     - Bandura1977Selfefficacy
     - Castelfranchi2017Rischio
     - Jenkins2009Confronting

3. **Setup Auto-Export:**
   - Crea collezione "AI in Education" in Zotero
   - Right-click → Export Collection
   - Format: **Better BibTeX**
   - ✅ **Keep updated** (importante!)
   - Save to: `/percorso/progetto/references/references.bib`

4. **Verifica:**
   ```bash
   # Ogni modifica in Zotero ora aggiorna automaticamente il .bib
   cat references/references.bib | grep "^@" | wc -l
   ```

---

## ➕ Aggiungere Referenze

### Da Browser (Zotero Connector - Più Veloce)

1. **Installa:** https://www.zotero.org/download/connectors
2. **Uso:**
   - Visita un articolo (es. PubMed, arXiv, journal)
   - Click icona Zotero in browser
   - Seleziona collezione "AI in Education"
   - ✅ Automaticamente aggiunto e sincronizzato!

### Da Identificatore (DOI/ISBN/PMID/arXiv)

In Zotero:
1. Click bacchetta magica (Add Item by Identifier)
2. Inserisci identificatore:
   ```
   10.1037/0033-295X.84.2.191        # DOI - Bandura 1977
   2301.04655                        # arXiv ID
   PMID:12345678                     # PubMed ID
   978-88-15-25234-5                 # ISBN
   ```
3. Enter → metadata automatici!

**Esempi Referenze del Progetto:**
```
Bandura 1977:         10.1037/0033-295X.84.2.191
Davis 1989:           10.2307/249008
Bandura 1986:         ISBN 0-13-815614-X
```

### Da Google Scholar

1. Cerca articolo
2. Click "Cite" sotto il risultato
3. Click "BibTeX" in fondo
4. Copia il testo
5. In Zotero: File → Import from Clipboard

### Manualmente

File → New Item → [Tipo documento]

**Campi principali:**
- Author (cognome, nome)
- Title
- Publication (journal/book)
- Year
- Volume/Issue/Pages
- DOI (se disponibile)

---

## 📖 Citare nel Markdown

### Sintassi Pandoc

```markdown
# Citazione singola
La teoria dell'autoefficacia [@Bandura1977Selfefficacy] fornisce...

# Citazioni multiple
Studi recenti [@Bandura1977Selfefficacy; @Davis1989Perceived; @Jenkins2009Confronting]
mostrano che...

# Con pagina/capitolo
Come discusso in [@Poggi2022Psicologia, pp. 45-67], la comunicazione...

# Citazione nel testo (nome visibile)
@Bandura1977Selfefficacy dimostra che l'autoefficacia influenza...

# Solo anno tra parentesi
Bandura [-@Bandura1977Selfefficacy] ha proposto...
```

### Output Generato (APA Style)

**Nel testo:**
- `[@Author2024]` → (Author, 2024)
- `[@Author2024; @Other2023]` → (Author, 2024; Other, 2023)
- `@Author2024` → Author (2024)

**Bibliografia finale:**
Generata automaticamente, ordinata alfabeticamente secondo APA.

---

## 🔧 Citation Keys Attuali

Referenze già disponibili nel progetto:

```
@techreport{Schwartz2024UnevenAdop}      # RAND - AI adoption study
@article{Davis1989PerceivedU}             # TAM - Technology Acceptance
@techreport{Jenkins2009ParticipatoryReport} # Participatory culture
@techreport{Carretero2017DigComp21}      # Digital competence framework
@techreport{Freeman2025StudentGen}        # Student AI survey
```

Visualizza tutte:
```bash
grep "^@" references/references.bib
```

---

## 🛠️ Comandi Makefile

```bash
# Converte RIS → BibTeX (solo se usi Approccio A)
make bib

# Genera PDF con citazioni
make pdf INPUT=nuovo-articolo.md

# Genera tutti i formati (PDF, HTML, DOCX, LaTeX)
make bundle INPUT=nuovo-articolo.md OUTPUT_BASENAME=nuovo-articolo

# Pulisci output precedenti
make clean
```

---

## 🎨 Personalizzare Citation Keys (Better BibTeX)

### Formula Attuale
```
[auth:capitalize][year][shorttitle3_3:capitalize]
```

### Altre Formule Utili

```
# Solo autore e anno (più corto)
[auth:lower][year]
→ bandura1977

# Primo autore + et al per multi-autore
[auth:capitalize][year][authEtAl:capitalize]
→ Schwartz2024Etal

# Con prima parola del titolo
[auth:capitalize][year][veryshorttitle:capitalize]
→ Bandura1977Self
```

**Cambiare formula:**
Edit → Preferences → Better BibTeX → Citation keys → Formato

---

## 📊 Stili di Citazione

Il progetto usa **APA 7th Edition** (`references/apa.csl`).

### Cambiare Stile

1. **Scarica stile:** https://www.zotero.org/styles
2. **Salva in:** `references/[nome_stile].csl`
3. **Modifica Makefile:**
   ```makefile
   CSL_FILE = references/chicago.csl  # invece di apa.csl
   ```

**Stili popolari:**
- APA (attuale)
- Chicago
- MLA
- Vancouver
- Nature
- IEEE

---

## ✅ Best Practices

### 1. Organizzazione in Zotero
- Crea collezione dedicata "AI in Education"
- Usa sotto-collezioni: "Theory", "Empirical Studies", "Methods"
- Aggiungi tags: "competence", "trust", "gender-gap"

### 2. Metadata Completi
Assicurati che ogni voce abbia:
- ✅ Autori completi (nome e cognome)
- ✅ Anno di pubblicazione
- ✅ DOI (se disponibile)
- ✅ Abstract (aiuta a ricordare il contenuto)

### 3. Citazioni nel Testo
```markdown
❌ Come dice lo studio di Smith del 2024...
✅ Come dimostrato [@Smith2024Evidence], gli studenti...
```

### 4. Backup
```bash
# Backup periodico del .bib
cp references/references.bib references/references.bib.backup-$(date +%Y%m%d)
```

---

## 🐛 Troubleshooting

### Problema: Citation key non trovato

**Errore:** `[WARNING] Citeproc: citation Bandura1977 not found`

**Soluzione:**
```bash
# 1. Verifica che esista nel .bib
grep "Bandura1977" references/references.bib

# 2. Controlla sintassi nel markdown
#    Deve essere: [@Bandura1977...] non [Bandura1977...]

# 3. Rigenera .bib se usi RIS
make bib
```

### Problema: Bibliografia non appare

**Verifica:**
1. File .bib esiste: `ls -lh references/references.bib`
2. Pandoc trova CSL: `ls -lh references/apa.csl`
3. Markdown ha citazioni: `grep "@" nuovo-articolo.md`

### Problema: Caratteri speciali (à, é, ñ)

Nel .bib usa:
```bibtex
author = {Mart{\'i}nez, Jos{\'e}}
title = {Educaci{\'o}n y tecnolog{\'i}a}
```

O in Zotero: Better BibTeX gestisce automaticamente!

---

## 📚 Risorse

- **Zotero:** https://www.zotero.org/
- **Better BibTeX:** https://retorque.re/zotero-better-bibtex/
- **Pandoc Citations:** https://pandoc.org/MANUAL.html#citations
- **CSL Styles:** https://www.zotero.org/styles
- **Citation Style Language:** https://citationstyles.org/

---

## 🆘 Supporto

Problemi o domande:
1. Consulta questa guida
2. Vedi `docs/README.md` per documentazione generale
3. Controlla `CLAUDE.md` per architettura progetto

---

*Ultima modifica: 2 novembre 2025*

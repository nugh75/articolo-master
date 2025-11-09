# Guida Setup Better BibTeX

Guida completa per passare dall'approccio RIS manuale a Better BibTeX con sincronizzazione automatica.

---

## 🎯 Obiettivo

Configurare **Better BibTeX** per Zotero in modo che:
- ✅ Le modifiche in Zotero si sincronizzino automaticamente con `references/references.bib`
- ✅ I citation keys siano stabili e consistenti
- ✅ Non sia più necessario esportare manualmente il file RIS
- ✅ Il workflow di compilazione rimanga invariato

---

## 📋 Prerequisiti

- [x] Zotero installato (https://www.zotero.org/download/)
- [ ] Better BibTeX plugin da installare
- [ ] Collezione Zotero con le referenze del progetto

---

## 🔧 Installazione Better BibTeX

### Passo 1: Download del Plugin

1. Visita: https://retorque.re/zotero-better-bibtex/installation/
2. Scarica l'ultima versione del file `.xpi` (es. `zotero-better-bibtex-6.x.x.xpi`)
3. **NON** aprire il file, solo scaricarlo

### Passo 2: Installazione in Zotero

1. Apri Zotero
2. Menu: **Tools** → **Add-ons**
3. Click sull'icona ingranaggio ⚙️ in alto a destra
4. Seleziona **Install Add-on From File...**
5. Trova e seleziona il file `.xpi` scaricato
6. Click **Install Now**
7. **Riavvia Zotero**

### Passo 3: Verifica Installazione

Dopo il riavvio, verifica che Better BibTeX sia attivo:
- Menu: **Edit** → **Preferences** 
- Dovrebbe apparire una nuova scheda **Better BibTeX** nella finestra delle preferenze

✅ Se vedi la scheda, l'installazione è riuscita!

---

## ⚙️ Configurazione Citation Keys

### Passo 1: Imposta Formula Citation Key

1. **Edit** → **Preferences** → **Better BibTeX** → **Citation keys**
2. Nel campo **Citation key formula**, inserisci:
   ```
   [auth:capitalize][year][shorttitle3_3:capitalize]
   ```
3. Click **OK**

**Questa formula genera citation keys tipo:**
- `Bandura1977Selfefficacy`
- `Castelfranchi2017Rischio`
- `Jenkins2009Confronting`

### Passo 2: Rigenera Citation Keys Esistenti

Se hai già referenze in Zotero:
1. Seleziona tutte le referenze nella tua collezione
2. Right-click → **Better BibTeX** → **Refresh BibTeX key**
3. I citation keys verranno aggiornati secondo la nuova formula

---

## 📁 Configurazione Auto-Export

### Passo 1: Identifica Path Assoluto del Progetto

Nel terminale del progetto, esegui:

```bash
cd /mnt/git/articolo
pwd  # Copia il percorso che appare
```

Il percorso sarà qualcosa tipo: `/mnt/git/articolo`

### Passo 2: Setup Export Automatico

1. In Zotero, vai alla tua collezione (o crea "AI in Education")
2. **Right-click sulla collezione** → **Export Collection...**
3. **Format**: Seleziona **Better BibTeX** (NON "BibTeX")
4. ✅ **IMPORTANTE**: Spunta **Keep updated**
5. **Save to**: Naviga e seleziona:
   ```
   /mnt/git/articolo/references/references.bib
   ```
6. Click **Save**

### Passo 3: Verifica Auto-Export Attivo

1. **Edit** → **Preferences** → **Better BibTeX** → **Automatic Export**
2. Dovresti vedere la tua collezione elencata con:
   - Status: ✓ (checkmark verde)
   - Path: `/mnt/git/articolo/references/references.bib`
   - Format: Better BibTeX

✅ Se vedi questi dettagli, l'auto-export è configurato!

---

## 🧪 Test del Sistema

### Test 1: Modifica Esistente

1. In Zotero, seleziona una referenza esistente
2. Modifica un campo (es. aggiungi una parola nel titolo)
3. Attendi 2-3 secondi
4. Nel terminale:
   ```bash
   cd /mnt/git/articolo
   tail -20 references/references.bib
   ```
5. Verifica che la modifica sia presente

### Test 2: Nuova Referenza

1. In Zotero, aggiungi una nuova referenza alla collezione
2. Esempio usando DOI: Click bacchetta magica, inserisci:
   ```
   10.1037/0033-295X.84.2.191
   ```
3. Attendi sincronizzazione (2-3 secondi)
4. Nel terminale:
   ```bash
   grep "Bandura1977" references/references.bib
   ```
5. Dovresti vedere la nuova entry

### Test 3: Compilazione Documento

```bash
make bundle INPUT=bridging-the-gap-article-draft.md OUTPUT_BASENAME=article_draft
```

Verifica che:
- ✅ Le citazioni vengano risolte correttamente
- ✅ La bibliografia sia generata
- ✅ Nessun warning su citation keys mancanti

---

## 🔄 Workflow Post-Setup

### Prima (Approccio RIS)
```bash
# 1. Modifiche in Zotero
# 2. Export manuale → RIS
# 3. make bib          # Converte RIS → BibTeX
# 4. make bundle       # Compila documento
```

### Dopo (Better BibTeX)
```bash
# 1. Modifiche in Zotero → Auto-sync automatico! 🎉
# 2. make bundle       # Compila documento
```

**Non serve più `make bib`!** Il file `.bib` è sempre aggiornato.

---

## 📝 Aggiungere Nuove Referenze

### Metodo 1: Browser (Più Veloce)

1. Installa Zotero Connector: https://www.zotero.org/download/connectors
2. Visita la pagina di un articolo (PubMed, arXiv, journal)
3. Click icona Zotero nel browser
4. Seleziona collezione "AI in Education"
5. ✅ Aggiunto automaticamente e sincronizzato!

### Metodo 2: DOI/ISBN/PMID

In Zotero:
1. Click bacchetta magica (Add Item by Identifier)
2. Inserisci identificatore:
   ```
   10.1037/0033-295X.84.2.191  # DOI
   2301.04655                   # arXiv
   PMID:12345678               # PubMed
   ```
3. ✅ Metadata scaricati automaticamente!

### Metodo 3: Google Scholar

1. Cerca articolo su Google Scholar
2. Click **"Cite"**
3. Click **"BibTeX"**
4. Copia tutto il testo
5. In Zotero: **File** → **Import from Clipboard**

---

## 🎨 Personalizzazione Citation Keys (Opzionale)

Se vuoi cambiare il formato dei citation keys:

### Formato Attuale
```
[auth:capitalize][year][shorttitle3_3:capitalize]
→ Bandura1977Selfefficacy
```

### Alternative Popolari

**Solo autore + anno (più corto):**
```
[auth:lower][year]
→ bandura1977
```

**Con et al per multi-autore:**
```
[auth:capitalize][year][authEtAl:capitalize]
→ Schwartz2024Etal
```

**Primo autore + prima parola titolo:**
```
[auth:capitalize][year][veryshorttitle:capitalize]
→ Bandura1977Self
```

Per cambiare:
1. **Edit** → **Preferences** → **Better BibTeX** → **Citation keys**
2. Modifica formula
3. Rigenera tutti i keys: seleziona collezione → **Refresh BibTeX key**

---

## 🔧 Modifica al Makefile (Opzionale)

Better BibTeX rende obsoleto il target `bib`. Puoi aggiornare il Makefile:

### Rimuovi dipendenza da RIS

Cambia questa riga nel Makefile:
```makefile
# Prima
$(BIB_FILE): $(RIS_FILE)
	@echo "Converting RIS to BibTeX..."
	@python3 scripts/conversion/ris_to_bibtex.py $(RIS_FILE) $(BIB_FILE)

# Dopo (commenta o rimuovi)
# $(BIB_FILE): $(RIS_FILE)
# 	@echo "Nota: BibTeX è gestito da Better BibTeX (auto-sync)"
```

### Aggiorna Help

```makefile
help:
	@echo "  make bib        - [DEPRECATO] Ora usa Better BibTeX auto-sync"
```

---

## 🐛 Troubleshooting

### Problema: Auto-export non funziona

**Sintomi:** Modifiche in Zotero non appaiono nel `.bib`

**Soluzioni:**
1. Verifica export attivo:
   - **Edit** → **Preferences** → **Better BibTeX** → **Automatic Export**
   - Deve esserci la tua collezione con status ✓
   
2. Forza manuale:
   - Right-click collezione → **Export Collection**
   - Seleziona lo stesso path → sostituisci file
   - ✅ Ri-spunta **Keep updated**

3. Riavvia Zotero

### Problema: Citation key duplicati

**Sintomi:** Warning tipo `Bandura1977Selfefficacy already exists`

**Soluzioni:**
1. Seleziona referenze duplicate
2. **Better BibTeX** → **Refresh BibTeX key**
3. Better BibTeX aggiungerà suffisso automatico (es. `Bandura1977Selfefficacya`)

### Problema: Caratteri speciali (é, à, ñ)

**Soluzione:** Better BibTeX gestisce automaticamente!

Gli autori con accenti vengono convertiti correttamente:
- `Martínez` → `author = {Mart{\'i}nez}`
- Nessuna azione richiesta da parte tua

### Problema: Citation key non appare in Zotero

**Sintomi:** La colonna "Citation Key" è vuota

**Soluzione:**
1. Right-click sulla barra delle colonne
2. Spunta **Citation Key**
3. La colonna appare con i keys generati

---

## ✅ Checklist Post-Setup

- [ ] Better BibTeX installato e attivo
- [ ] Formula citation key configurata
- [ ] Auto-export attivo e funzionante
- [ ] Test con modifica referenza esistente → sync OK
- [ ] Test con nuova referenza → sync OK
- [ ] Compilazione documento → no errori
- [ ] Zotero Connector installato nel browser
- [ ] Backup del vecchio file RIS (opzionale)

---

## 📚 Vantaggi del Nuovo Sistema

| Aspetto | Prima (RIS) | Dopo (Better BibTeX) |
|---------|-------------|---------------------|
| Sync | ❌ Manuale | ✅ Automatico |
| Citation Keys | ⚠️ Variabili | ✅ Stabili |
| Workflow | 4 passi | 2 passi |
| Errori export | ⚠️ Possibili | ✅ Minimizzati |
| Pin specifico | ❌ No | ✅ Sì (pin key manuale) |

---

## 📖 Risorse

- **Better BibTeX Home**: https://retorque.re/zotero-better-bibtex/
- **Documentation**: https://retorque.re/zotero-better-bibtex/citing/
- **Citation Key Format**: https://retorque.re/zotero-better-bibtex/citing/customized-keys/
- **Zotero Forums**: https://forums.zotero.org/

---

## 🆘 Supporto

Problemi o domande:
1. Consulta la sezione Troubleshooting sopra
2. Vedi documentazione Better BibTeX
3. Controlla forum Zotero
4. Vedi `docs/reference/ZOTERO_GUIDE.md` per workflow generale

---

*Creato: 4 novembre 2025*
*Progetto: CNR-articolo-quantitativo*

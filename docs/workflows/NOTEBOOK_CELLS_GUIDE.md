# Guida alle celle del notebook analisi_dati.ipynb

Questo documento fornisce una panoramica completa di tutte le celle del notebook `notebooks/analisi_dati.ipynb`, organizzate per sezione tematica.

## Sezione 1: Setup e Configurazione Iniziale

### Cella 1 (Markdown)
**Tipo:** Markdown  
**Contenuto:** Intestazione principale e descrizione del notebook  
**Scopo:** Descrive l'obiettivo dell'analisi esplorativa e le funzionalità principali

### Cella 2 (Python) - INSTALLAZIONE DIPENDENZE
**Linee:** 12-25  
**Scopo:** Verifica e installa automaticamente le librerie Python necessarie (pandas, numpy, matplotlib, seaborn, openpyxl)  
**Output:** Messaggio di conferma installazione dipendenze

### Cella 3 (Python) - IMPORT E CONFIGURAZIONE
**Linee:** 28-41  
**Scopo:** Importa librerie principali e configura opzioni di visualizzazione  
**Configurazioni:**
- Mostra fino a 100 righe/colonne
- Tema grafico 'whitegrid' di seaborn
- Stampa versioni librerie

### Cella 4 (Python) - DEFINIZIONE PERCORSI
**Linee:** 44-51  
**Scopo:** Definisce percorsi cartelle dati e output  
**Variabili create:**
- `ROOT`: directory corrente
- `DATA_DIR`: cartella dati di input
- `OUTPUT_DIR`: cartella output esplorativo

### Cella 5 (Python) - LISTA FILE DISPONIBILI
**Linee:** 54-62  
**Scopo:** Cerca ed elenca tutti i file dati disponibili (CSV, TSV, Excel, JSON)  
**Output:** Elenco numerato file trovati

### Cella 6 (Python) - IDENTIFICAZIONE FILE PRINCIPALI
**Linee:** 65-97  
**Scopo:** Identifica automaticamente file Excel di insegnanti e studenti  
**Metodo:** Pattern matching su nomi file con fallback alfabetico

### Cella 7 (Python) - CARICAMENTO DATI
**Linee:** 100-178  
**Scopo:** Carica dati da Excel, gestisce intestazioni duplicate, unifica strutture  
**Output:**
- Dataframe `_df_ins` (insegnanti)
- Dataframe `_df_stu` (studenti)
- Lista `q_insegnanti`, `q_studenti` (domande)

### Cella 8 (Python) - CONCATENAZIONE DATASET
**Linee:** 181-195  
**Scopo:** Concatena insegnanti e studenti in dataframe unico  
**Variabile creata:** `DF` (dataset completo)  
**Output:** CSV combinato salvato

### Cella 9 (Python) - ESTRAZIONE LISTA DOMANDE
**Linee:** 198-294  
**Scopo:** Estrae e salva lista completa delle domande del questionario  
**Output:** CSV con domande numerate

### Cella 10 (Python) - CLASSIFICAZIONE 4 GRUPPI
**Linee:** 297-323  
**Scopo:** Classifica partecipanti in 4 categorie dettagliate:
- studenti - secondaria
- studenti - universitari
- insegnanti - non in servizio
- insegnanti - in servizio  
**Variabile creata:** `DF_plot` con colonna `GruppoDettaglio`

### Cella 11 (Python) - VERIFICA CLASSIFICAZIONE
**Linee:** 326-432  
**Scopo:** Verifica correttezza classificazione con crosstab  
**Output:** CSV con crosstab gruppo vs stato insegnamento

## Sezione 2: Analisi Demografica - Età

### Cella 12 (Python) - VIOLIN PLOT ETÀ
**Linee:** 435-499  
**Scopo:** Crea violin plot distribuzione età per i 4 gruppi  
**Esclusioni:** Studenti primaria, docenti universitari  
**Palette:** rosso=secondaria, verde=universitari, giallo=non servizio, blu=in servizio  
**Output:** `violin_eta.png`, CSV dati e summary

### Cella 13 (Python) - BOX PLOT ETÀ CON OUTLIER
**Linee:** 502-621  
**Scopo:** Box plot età mostrando outlier  
**Output:** `box_eta.png`, tabella statistiche descrittive

### Cella 14-22 (Python)
**Scopo:** Varianti grafici età (box plot con outlier colorati, versioni inglesi, grafici Plotly interattivi)

## Sezione 3: Analisi Demografica - Genere e Area Disciplinare

### Cella 23 (Python) - GRAFICI GENERE E AREA
**Linee:** 1109-1282  
**Scopo:** Genera grafici a barre distribuzione genere e area disciplinare  
**Output:**
- Grafici PNG alta risoluzione (IT + EN)
- CSV con conteggi per gruppo
- Grafici separati per genere e area

### Cella 24 (Python) - AREA DISCIPLINARE (AGGIORNATA)
**Linee:** 1285-1376  
**Scopo:** Versione migliorata grafici area disciplinare  
**Categorie:** Umanistica, Scientifica, Non risponde

### Cella 25 (Python) - BOX PLOT ORE SETTIMANALI
**Linee:** 1379-1482  
**Scopo:** Box plot ore settimanali uso IA con outlier  
**Output:** Grafici PNG/SVG, statistiche descrittive

### Cella 26 (Python) - VIOLIN PLOT TRIMMED
**Linee:** 1485-1576  
**Scopo:** Violin plot senza outlier (solo inliers per leggibilità)  
**Metodo:** Rimozione outlier tramite IQR  
**Output:** Versioni IT + EN

## Sezione 4: Uso Quotidiano dell'IA

### Cella 27 (Python) - USO QUOTIDIANO IA (SÌ/NO)
**Linee:** 1492-1576  
**Scopo:** Grafici a barre uso quotidiano IA  
**Domanda:** "Utilizzi l'intelligenza artificiale nella tua vita quotidiana?"  
**Layout:** Griglia 4 pannelli + grafico unico  
**Output:** PNG/SVG in IT + EN

### Cella 28 (Python) - USO IA PER STUDIO E INSEGNAMENTO
**Linee:** 1579-1687  
**Scopo:** Grafici uso IA per studio (studenti) e insegnamento (insegnanti)  
**Output:** Pannelli separati + grafici combinati in IT + EN

### Cella 29 (Python) - VERSIONE COMBINATA 4 GRUPPI
**Linee:** 1690-1964  
**Scopo:** Grafici combinati uso IA studio/insegnamento  
**Output:** CSV conteggi + PNG/SVG grafici

## Sezione 5: Competenze Percepite

### Cella 30 (Python) - COMPETENZE PRATICA VS TEORICA
**Linee:** 1967-2131  
**Scopo:** Analisi competenza percepita pratica vs teorica  
**Metodo:** Distribuzione risposte scala Likert con calcolo medie  
**Output:** Grafici comparativi per gruppo

### Cella 31 (Python) - GRAFICI COMPETENZE PUBBLICAZIONE
**Linee:** 2134-2224  
**Scopo:** Versione ottimizzata grafici competenze per pubblicazione  
**Colori:** Blu=pratica, Arancione=teorica  
**Output:** Layout pannelli con distribuzioni complete Likert 1-5

### Cella 32 (Python) - NUMERO STRUMENTI IA
**Linee:** 2232-2274  
**Scopo:** Box plot numero strumenti IA utilizzati  
**Risultato tipico:** 1-2 strumenti (prevalenza ChatGPT)

## Sezione 6: Analisi Scala Likert

### Cella 33 (Python) - ESTRAZIONE DOMANDE LIKERT
**Linee:** 2277-2324  
**Scopo:** Identifica domande scala Likert (1-5)  
**Metodo:** Filtra colonne con risposte numeriche 1-5

### Cella 34 (Python) - STATISTICHE LIKERT PER GRUPPO
**Linee:** 2327-2390  
**Scopo:** Calcola statistiche descrittive domande Likert  
**Output:** CSV con media, mediana, SD, conteggi per gruppo

### Celle 35-40 (Python)
**Scopo:** Grafici heatmap, radar chart e analisi multidimensionali domande Likert

## Sezione 7: Analisi Avanzate

### Celle 41-50 (Python)
**Scopo:** 
- Analisi fattoriale domande Likert
- Grafici per singole dimensioni
- Confronti tra gruppi
- Versioni inglesi dei grafici

### Celle 51-60 (Python)
**Scopo:**
- Analisi correlazioni
- Test statistici (Kruskal-Wallis, Mann-Whitney)
- Grafici distribuzioni specifiche
- Export dati per analisi R/SPSS

## Sezione 8: Grafici Specializzati

### Celle 61-70 (Python)
**Scopo:**
- Grafici interattivi Plotly
- Analisi temporali
- Confronti incrociati
- Dashboard riepilogativi

### Celle 71-80 (Python)
**Scopo:**
- Grafici pubblicazione finale
- Versioni alta risoluzione
- Export multipli formati (PNG, SVG, PDF)
- Tabelle riepilogative

## Sezione 9: Analisi Testuali e Qualitative

### Celle 81-90 (Python)
**Scopo:**
- Analisi risposte aperte
- Word clouds
- Categorizzazione tematiche
- Frequenze parole chiave

## Sezione 10: Export e Finalizzazione

### Celle 91-98 (Python)
**Scopo:**
- Export finali tutti i dati
- Creazione report HTML
- Salvataggio workspace
- Pulizia file temporanei

## Palette Colori Standard

**4 Gruppi:**
- Studenti - secondaria: `red`
- Studenti - universitari: `forestgreen`  
- Insegnanti - in servizio: `royalblue`
- Insegnanti - non in servizio: `gold`

**Competenze:**
- Pratica: `blue` / `steelblue`
- Teorica: `orange` / `darkorange`

**Grafici Sì/No:**
- Sì: `darkgray`
- No: `lightgray`

## Convenzioni File Output

**Grafici:**
- `*_it.png` / `*_it.svg`: Versione italiana
- `*_en.png` / `*_en.svg`: Versione inglese
- DPI: 150 (visualizzazione), 300 (pubblicazione)

**Dati:**
- `*.csv`: Tabelle e conteggi
- `*_summary.csv`: Statistiche descrittive
- `*_data.csv`: Dati grezzi per grafici

**Cartelle Output:**
- `analysis/exports/latest/demographics/`: Grafici demografici
- `analysis/exports/latest/usage/`: Grafici uso IA
- `analysis/exports/latest/competence/`: Grafici competenze
- `analysis/exports/latest/likert/`: Analisi Likert
- `analysis/exports/latest/classificazione/`: File verifica classificazione

## Note Importanti

1. **Ordine esecuzione:** Le celle devono essere eseguite in sequenza per garantire la disponibilità delle variabili necessarie

2. **Filtri applicati:** Studenti primaria e docenti universitari sono esclusi dalla maggior parte delle analisi (n insufficiente)

3. **Gestione outlier:** Per le ore settimanali, vengono create versioni sia con outlier visibili che "trimmed" (solo inliers)

4. **Bilingue:** Tutte le visualizzazioni principali hanno versione italiana e inglese

5. **Riproducibilità:** Tutti i grafici salvano anche i dati sorgente in CSV per permettere riproducibilità e verifiche

## Aggiornamenti

- **7 novembre 2025:** Aggiunte celle esplicative markdown per facilitare comprensione struttura notebook
- Le celle di codice mantengono commenti inline per dettagli implementativi

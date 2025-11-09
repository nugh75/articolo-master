# Conversione Markdown → LaTeX

Sistema completo per convertire file Markdown in LaTeX con gestione di:
- ✅ Preambolo personalizzabile
- ✅ Citazioni bibliografiche (BibTeX/BibLaTeX)
- ✅ Grafica e immagini
- ✅ Template LaTeX custom
- ✅ Stili CSL

## File creati

- **`template_latex.tex`**: Template LaTeX con preambolo personalizzabile
- **`md_to_latex.py`**: Script Python per conversione automatica
- **`Makefile`**: Target `latex` per workflow automatizzato

## Uso rapido

### Opzione 1: Make (consigliato)

```bash
make latex
```

Questo genera `article_draft.tex` usando il template personalizzato.

### Opzione 2: Script Python diretto

```bash
# Conversione base
python3 md_to_latex.py bridging-the-gap-article-draft.md

# Con tutti i parametri
python3 md_to_latex.py bridging-the-gap-article-draft.md \
  -o output.tex \
  -t template_latex.tex \
  -b references.bib \
  -c apa.csl
```

### Opzione 3: Help completo

```bash
python3 md_to_latex.py --help
```

## Personalizzare il preambolo

Modifica `template_latex.tex` per personalizzare:

### 1. Pacchetti LaTeX

```latex
% Aggiungi pacchetti nella sezione PREAMBOLO
\usepackage{miopacchetto}
```

### 2. Stile documento

```latex
\documentclass[12pt,a4paper]{article}  % Modifica qui
```

### 3. Margini e layout

```latex
\usepackage[margin=2.5cm]{geometry}    % Cambia margini
\onehalfspacing                        % Interlinea 1.5
```

### 4. Grafica

```latex
% Path per le immagini (già configurato)
\graphicspath{{./}{./charts/}{./images/}{./figures/}}
```

### 5. Comandi personalizzati

```latex
% Nella sezione COMANDI PERSONALIZZATI
\newcommand{\miocmd}[1]{\textbf{#1}}
```

## Gestione citazioni

### Metodo 1: Pandoc + CSL (Pandoc >= 2.11)

Se hai Pandoc recente, le citazioni vengono processate automaticamente:

```bash
python3 md_to_latex.py article.md -b references.bib -c apa.csl
```

### Metodo 2: BibTeX tradizionale (Pandoc < 2.11)

Se hai Pandoc vecchio (come nel tuo caso), le citazioni vengono gestite da LaTeX:

1. **Nel Markdown**, scrivi citazioni come:
   ```markdown
   Secondo Smith (2020) [@Smith2020], ...
   ```

2. **Pandoc converte** in LaTeX come testo normale (non processa citazioni)

3. **Per usare BibTeX**, modifica il LaTeX generato:
   - Sostituisci `[@Smith2020]` con `\cite{Smith2020}`
   - Oppure usa uno script di post-processing

4. **Compila con BibTeX**:
   ```bash
   pdflatex article_draft.tex
   bibtex article_draft
   pdflatex article_draft.tex
   pdflatex article_draft.tex
   ```

### Metodo 3: BibLaTeX (consigliato per controllo avanzato)

Modifica `template_latex.tex`, decommenta:

```latex
\usepackage[style=apa,backend=biber]{biblatex}
\addbibresource{references.bib}
```

E alla fine del template, sostituisci la sezione bibliografia con:

```latex
\printbibliography
```

Compila con:

```bash
pdflatex article_draft.tex
biber article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

## Gestione immagini

### Path automatici

Il template è già configurato per cercare immagini in:
- `./` (directory corrente)
- `./charts/`
- `./images/`
- `./figures/`

### Nel Markdown

```markdown
![Didascalia](image.png)
```

Viene convertito in:

```latex
\begin{figure}
\centering
\includegraphics{image.png}
\caption{Didascalia}
\end{figure}
```

### Opzioni avanzate

Per controllare dimensioni nel LaTeX generato:

```latex
\includegraphics[width=0.8\textwidth]{image.png}
```

## Compilazione LaTeX → PDF

### Metodo 1: pdflatex semplice

```bash
pdflatex article_draft.tex
```

### Metodo 2: Con BibTeX

```bash
pdflatex article_draft.tex
bibtex article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

### Metodo 3: Con BibLaTeX/Biber

```bash
pdflatex article_draft.tex
biber article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

### Metodo 4: latexmk (automatico)

```bash
latexmk -pdf article_draft.tex
```

Questo esegue automaticamente tutti i passaggi necessari.

## Workflow completo

### 1. Scrivi in Markdown

Crea o modifica `bridging-the-gap-article-draft.md` con:
- Testo in Markdown
- Citazioni come `[@key]` o testo normale
- Immagini come `![caption](file.png)`

### 2. Converti in LaTeX

```bash
make latex
# oppure
python3 md_to_latex.py bridging-the-gap-article-draft.md
```

### 3. Personalizza (opzionale)

- Modifica `template_latex.tex` per il preambolo
- Modifica `article_draft.tex` per aggiustamenti specifici

### 4. Gestisci citazioni (se necessario)

Se usi BibTeX/BibLaTeX manualmente:
- Converti citazioni da `[@key]` a `\cite{key}`
- Oppure inserisci citazioni direttamente nel .tex

### 5. Compila

```bash
latexmk -pdf article_draft.tex
```

### 6. Verifica PDF

```bash
xdg-open article_draft.pdf
```

## Opzioni avanzate

### Metadata YAML nel Markdown

Aggiungi all'inizio del file .md:

```yaml
---
title: "Titolo dell'articolo"
author: "Nome Autore"
date: "2025-10-18"
abstract: "Breve abstract..."
toc: true
---
```

### Opzioni pandoc personalizzate

```bash
python3 md_to_latex.py article.md --pandoc-opts "--toc --toc-depth=3"
```

### Disabilitare template/bibliografia

```bash
python3 md_to_latex.py article.md --no-template --no-bib
```

## Troubleshooting

### Problema: Citazioni non funzionano

**Soluzione**: Con Pandoc < 2.11, gestisci citazioni in LaTeX:
1. Converti manualmente `[@key]` in `\cite{key}`
2. Oppure usa BibLaTeX nel template

### Problema: Immagini non trovate

**Soluzione**:
- Verifica path in `\graphicspath{}`
- Usa path assoluti o relativi corretti
- Assicurati che le immagini siano in formato supportato (PNG, JPG, PDF)

### Problema: Errori di compilazione LaTeX

**Soluzione**:
1. Controlla log: `less article_draft.log`
2. Verifica pacchetti mancanti
3. Installa pacchetti: `sudo apt-get install texlive-full`

### Problema: Template non applicato

**Soluzione**: Verifica che il path sia corretto:
```bash
python3 md_to_latex.py article.md -t template_latex.tex
```

## Esempi

### Esempio 1: Conversione base

```bash
python3 md_to_latex.py mio_articolo.md
pdflatex mio_articolo.tex
```

### Esempio 2: Con template e bibliografia

```bash
python3 md_to_latex.py mio_articolo.md \
  -t template_latex.tex \
  -b references.bib \
  -c apa.csl

latexmk -pdf mio_articolo.tex
```

### Esempio 3: Workflow completo

```bash
# 1. Converti
make latex

# 2. Compila con BibTeX
pdflatex article_draft.tex
bibtex article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex

# 3. Visualizza
xdg-open article_draft.pdf
```

## Risorse

- **Pandoc manual**: https://pandoc.org/MANUAL.html
- **LaTeX documentation**: https://www.latex-project.org/help/documentation/
- **BibLaTeX manual**: https://ctan.org/pkg/biblatex
- **Citation styles (CSL)**: https://github.com/citation-style-language/styles

## Note sulla versione Pandoc

Il tuo sistema ha **Pandoc 2.5** (vecchio). Limitazioni:
- ❌ Non supporta `--citeproc` (citazioni processate da Pandoc)
- ✅ Supporta template LaTeX
- ✅ Supporta conversione Markdown → LaTeX
- ⚠️  Per citazioni, usa BibTeX/BibLaTeX in LaTeX

Per aggiornare Pandoc (opzionale):
```bash
# Scarica ultima versione da https://github.com/jgm/pandoc/releases
wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-amd64.deb
sudo dpkg -i pandoc-3.1.11-1-amd64.deb
```

## Licenza

Questi script sono forniti come-sono per uso personale. Modifica e personalizza liberamente.

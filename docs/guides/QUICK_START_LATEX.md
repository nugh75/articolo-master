# Quick Start: Markdown → LaTeX

## 🚀 Conversione in 3 comandi

```bash
# 1. Converti MD → LaTeX con template personalizzato
make latex

# 2. Compila LaTeX → PDF
pdflatex article_draft.tex

# 3. Visualizza PDF
xdg-open article_draft.pdf
```

## 📝 Personalizzazione

### Modifica il preambolo LaTeX
```bash
nano template_latex.tex
```

Esempi di modifiche comuni:
- **Margini**: Cambia `\usepackage[margin=2.5cm]{geometry}`
- **Font**: Cambia `\documentclass[12pt,a4paper]{article}`
- **Pacchetti**: Aggiungi `\usepackage{tuopacchetto}`

### Converti altri file MD
```bash
python3 md_to_latex.py mio_file.md
```

## 📚 Gestione citazioni

### Con BibTeX (semplice)
```bash
pdflatex article_draft.tex
bibtex article_draft
pdflatex article_draft.tex
pdflatex article_draft.tex
```

### Con BibLaTeX (avanzato)
1. Modifica `template_latex.tex`, decommenta:
   ```latex
   \usepackage[style=apa,backend=biber]{biblatex}
   \addbibresource{references.bib}
   ```

2. Compila:
   ```bash
   pdflatex article_draft.tex
   biber article_draft
   pdflatex article_draft.tex
   ```

## 🖼️ Immagini

Le immagini vengono cercate automaticamente in:
- `./` (directory corrente)
- `./charts/`
- `./images/`

Nel Markdown:
```markdown
![Didascalia dell'immagine](image.png)
```

## 🔧 Opzioni avanzate

```bash
# Help completo
python3 md_to_latex.py --help

# Senza template
python3 md_to_latex.py file.md --no-template

# Con opzioni pandoc custom
python3 md_to_latex.py file.md --pandoc-opts "--toc --toc-depth=2"
```

## 📖 Documentazione completa

Vedi `README_LATEX.md` per la guida completa.

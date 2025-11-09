# Word style reference

Questo repository utilizza un file di riferimento (`templates/reference.docx`) per controllare l'aspetto dei documenti Word generati da pandoc. Tutti i font e gli stili principali vengono letti da quel file quando lanci `make docx` oppure `make bundle`.

## Dove intervenire

- Apri `templates/reference.docx` con Word o LibreOffice.
- Nel documento troverai blocchi delimitati da righe come `=== BLOCCO NORMAL: INIZIO ===`. Ogni blocco mostra lo stile applicato al testo subito sopra o sotto.
- Modifica il testo all'interno dei blocchi (font, dimensione, colore, spaziatura) per aggiornare lo stile corrispondente:
  - **Normal**: corpo del testo (attualmente Times New Roman, 12pt, nero, giustificato).
  - **Heading 1/2/3**: titoli con font Times New Roman nero.
  - **Title/Subtitle**: intestazione principale del documento di riferimento.

> Suggerimento: per cambiare rapidamente un attributo, evidenzia il testo dentro il blocco e modifica lo stile mediante il riquadro "Stili" di Word, quindi fai `Aggiorna [Nome stile] in base alla selezione`.

## Configurazione rapida tramite file di override

- Modifica `config/style_overrides.txt` per impostare font globale, giustificazione e distanza tra titolo e corpo.
- Attiva una riga togliendo il `#` iniziale; disattivala rimettendo il commento.
- Esempio di opzioni disponibili:
  - `font.family = Times New Roman`
  - `body.justify = true`
  - `title.spacing_after_pt = 18`
- Dopo ogni modifica lancia `python3 scripts/conversion/generate_reference_docx.py` per aggiornare il template.

## Rigenerare il file di riferimento

Se vuoi ripartire da zero o vuoi applicare modifiche tramite script, puoi rigenerare il file con:

```bash
python3 scripts/conversion/generate_reference_docx.py
```

Il comando ricrea `templates/reference.docx` applicando:

- Corpo del testo in Times New Roman 12pt nero.
- Titoli neri (Heading 1-3) in Times New Roman con dimensioni scalate (18/16/14pt).
- Blocchi etichettati per identificare facilmente cosa modificare.

## Utilizzare varianti di stile

Per mantenere varianti con font differenti:

1. Duplica `templates/reference.docx` (es. `templates/reference-serif.docx`).
2. Personalizza la copia con i nuovi stili.
3. Lancia pandoc specificando il file duplicato, ad esempio:

   ```bash
   make docx REFERENCE_DOCX=templates/reference-serif.docx
   ```

Oppure esporta direttamente:

```bash
REFERENCE_DOCX=templates/reference-serif.docx make bundle
```

In questo modo puoi passare rapidamente da un set di stili all'altro senza sovrascrivere il file predefinito.

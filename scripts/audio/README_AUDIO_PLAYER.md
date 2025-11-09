# 🎵 Audio Player per Articoli Markdown

Builder automatico che converte articoli Markdown in MP3 con generazione asincrona intelligente.

## ✨ Caratteristiche

- 🎤 **Text-to-Speech di alta qualità** con Microsoft Edge TTS
- 🌍 **Supporto bilingue** automatico (Italiano/Inglese, voce Isabella per l'italiano)
- ⚡ **Generazione asincrona** - divide il testo in parti e le genera in parallelo
- 💾 **MP3 per paragrafo** – ogni sezione produce un unico file nominato con lo slug del titolo
- 🧹 **Pulizia Markdown avanzata** – rimuove marcatori, liste, heading e footnote
- 🎯 **Smart chunking** - spezza il testo su frasi complete per evitare tagli bruschi
- 📡 **Invio opzionale via SSH** - trasferisce automaticamente i file generati tramite `scp`
- 🔎 **Filtri per sezione** - converti solo i paragrafi che ti servono (`--section`)
- 🗂️ **Filtri lingua** - decidi se generare solo sezioni italiane, inglesi o una combinazione (`--language`)
- 🧭 **Menu interattivo** (launcher) - scegli con un wizard lingue, sezioni e voci prima di generare l'audio

## 📦 Installazione

```bash
# Installa le dipendenze
pip install edge-tts

# Rendi eseguibile lo script (Linux/Mac)
chmod +x scripts/audio/audio_player.py
```

## 🚀 Utilizzo

### Menu interattivo (default)
```bash
scripts/audio/play_audio.sh
```
Il launcher avvia un piccolo wizard che ti guida in tre passaggi:

1. **Lingue** – scegli se convertire l'articolo in italiano, inglese o entrambi.
2. **Sezioni** – seleziona rapidamente i paragrafi (es. Introduzione, Metodi, Discussione).
3. **Voci** – imposta la voce TTS preferita per ogni lingua (o inseriscine una personalizzata).

Se premi `Invio` a ogni passaggio verranno convertite tutte le sezioni in entrambe le lingue con le voci predefinite (Isabella/Guy). Il menu si disattiva automaticamente quando lo script è avviato in modalità non interattiva (pipe/CI) o quando passi già argomenti espliciti.

Per saltare il wizard, imposta `AUDIO_PLAYER_SKIP_MENU=1` oppure passa le opzioni manualmente (`--section`, `--language`). Per forzarlo anche quando fornisci argomenti, usa `AUDIO_PLAYER_FORCE_MENU=1`.

### Generazione completa (senza menu)
```bash
scripts/audio/play_audio.sh
```

### Specifica un file Markdown
```bash
scripts/audio/play_audio.sh /percorso/articolo.md
```

### Usa direttamente Python
```bash
python scripts/audio/audio_player.py /percorso/articolo.md
```

### Converti solo una lingua
```bash
# Solo le sezioni italiane
scripts/audio/play_audio.sh --language it

# Solo le sezioni inglesi
python scripts/audio/audio_player.py bridging-the-gap-article-draft.md --language en

# Specifica più lingue (ripetibile)
scripts/audio/play_audio.sh --language it --language en
```

### Converti solo determinate sezioni
```bash
scripts/audio/play_audio.sh --section "Introduzione" --section "Appendix"
# oppure
python scripts/audio/audio_player.py bridging-the-gap-article-draft.md \
  --section "Introduzione" --section "Appendix"
```
Puoi combinare `--language` e `--section` per restringere ulteriormente la selezione.
Il menu interattivo usa internamente le stesse flag, così puoi replicare facilmente le scelte anche in modalità non interattiva.

## 🧠 Come funziona

1. **Estrazione sezioni**: Analizza il file Markdown e identifica tutte le sezioni (`##`)
2. **Rilevamento lingua**: Usa marker `<!-- lang:it/en -->` per identificare italiano/inglese
3. **Smart chunking**: Divide testi lunghi in parti di ~3000 caratteri (30-45s audio)
4. **Generazione parallela**: Genera fino a 3 chunk alla volta in modo asincrono
5. **Merge trasparente**: Unisce i chunk in un unico MP3 nominato con lo slug della sezione
6. **Export finale**: Salva l'MP3 e, se richiesto, lo invia via SSH (nessuna riproduzione locale)

## 🎤 Voci utilizzate

- **Italiano**: Isabella (F) - Voce femminile naturale (richiesta)
- **Inglese**: Guy (M) - Voce maschile americana

## 📁 File generati

- **Output finale**: `output/audio/<titolo-sezione>.mp3`
- **Chunk temporanei**: `output/audio/_chunks/chunk_XXX.mp3` (rimossi automaticamente)

I file finali restano disponibili finché non cancelli manualmente la cartella o disattivi `MD_AUDIO_KEEP_FILES`.

## ⚙️ Configurazione avanzata

Puoi modificare queste costanti nello script:

```python
CHUNK_SIZE = 3000  # caratteri per chunk
VOICES = {
    'it': 'it-IT-DiegoNeural',
    'en': 'en-US-GuyNeural'
}
```

### Voci alternative disponibili

**Italiano:**
- `it-IT-IsabellaNeural` (F, default)
- `it-IT-DiegoNeural` (M)
- `it-IT-ElsaNeural` (F)

**Inglese:**
- `en-US-GuyNeural` (M)
- `en-GB-RyanNeural` (M, UK)
- `en-GB-SoniaNeural` (F, UK)

### Override rapido delle voci
Puoi cambiare al volo le voci predefinite impostando queste variabili (le stesse utilizzate dal menu):

```bash
export MD_AUDIO_VOICE_IT="it-IT-ElsaNeural"
export MD_AUDIO_VOICE_EN="en-GB-SoniaNeural"
```

Il wizard aggiorna automaticamente `MD_AUDIO_VOICE_IT/EN` per la sessione corrente, quindi puoi lanciare lo script in modo non interattivo subito dopo mantenendo le stesse voci.

## 📡 Invio automatico via SSH

Per trasferire ogni MP3 generato verso un altro host con `scp`:

```bash
export AUDIO_PLAYER_SSH_TARGET="utente@host:/percorso/destinazione/"
scripts/audio/play_audio.sh
```

Flag aggiuntivi (porta, chiavi dedicate, ecc.) possono essere passati con:

```bash
export AUDIO_PLAYER_SSH_OPTIONS="-P 2222 -i ~/.ssh/id_ed25519"
```

Quando configurato, il launcher mostra `📡 Invio SSH attivo` e spedisce automaticamente ogni file finale.
> Se esegui direttamente `python scripts/audio/audio_player.py`, usa le variabili `MD_AUDIO_SSH_TARGET` e `MD_AUDIO_SSH_OPTIONS`.

## 🔇 Modalità headless (default)

Il tool genera esclusivamente file MP3: non tenta di riprodurre l’audio in locale. È quindi ideale da eseguire via SSH. Usa le variabili `AUDIO_PLAYER_SSH_TARGET`/`MD_AUDIO_SSH_TARGET` per trasferire automaticamente i file se ti serve ascoltarli su un’altra macchina.

## 🐛 Troubleshooting

### "edge_tts non trovato"
```bash
pip install edge-tts
```

### "Errore trasferimento SSH"
- Verifica di poter eseguire manualmente `scp file utente@host:/percorso/`
- Aggiungi eventuali flag necessari con `AUDIO_PLAYER_SSH_OPTIONS`

### "⚠️ Nessuna sezione corrisponde ai filtri forniti"
- Controlla che `--section` combaci con il titolo (match parziale, case insensitive)
- Verifica di non aver escluso tutte le lingue con l'opzione `--language`
- Rimuovi i filtri per convertire tutto l'articolo

### "Lo script resta in attesa di input"
- Il launcher avvia un menu quando eseguito da terminale senza argomenti.
- Per saltarlo, usa `AUDIO_PLAYER_SKIP_MENU=1 scripts/audio/play_audio.sh` oppure passa direttamente le opzioni (`--language`, `--section`...).
- In ambienti headless/CI il menu viene disabilitato automaticamente.

### File generati ma non conservati
- Di default il launcher mantiene gli MP3 in `output/audio`
- Se esegui manualmente lo script imposta `MD_AUDIO_KEEP_FILES=1` per evitarne la rimozione

## 📊 Esempio output

```
🎵 Generatore Audio per Articoli Markdown
======================================
🐍 Interpreter: /usr/bin/python3

🔍 Verifica dipendenze...
✅ edge-tts già installato

💾 Gli MP3 verranno salvati in: /mnt/git/articolo/output/audio
▶️  Avvio generazione...
📄 Sezioni trovate: 15

============================================================
🎵 Introduction: GenAI as Cultural Mediator in Education
============================================================
📄 Lingua: EN
📏 Lunghezza: 3815 caratteri (~640 parole)

📦 Diviso in 3 parti
🎤 Voce: en-US-GuyNeural
✅ Generazione completata!
💾 File MP3 creato: introduction-genai-as-cultural-mediator-in-education.mp3
📁 Percorso: /mnt/git/articolo/output/audio/introduction-genai-as-cultural-mediator-in-education.mp3

...

======================================
✅ Conversione completata
 - introduction-genai-as-cultural-mediator-in-education.mp3
 - introduzione-la-genai-come-mediatore-culturale-nell-istruzione.mp3
 - ...
======================================
```

## 🔧 Requisiti di sistema

- Python 3.7+
- Connessione internet (per edge-tts API)
- ~10MB spazio disco per file temporanei

## 📝 Note

- La velocità di generazione dipende dalla connessione internet
- Ogni chunk richiede ~2-5 secondi per essere generato
- Il playback inizia non appena il primo chunk è pronto
- La generazione asincrona mantiene sempre 1-2 chunk di vantaggio

## 🤝 Contributi

Per migliorare lo script:
1. Modifica `scripts/audio/audio_player.py`
2. Testa con diversi file Markdown
3. Documenta modifiche in questo README

## 📜 Licenza

Stesso del progetto principale.

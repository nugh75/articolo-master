#!/bin/bash
# Setup script per Generatore Audio

echo "🔧 Setup Generatore Audio per Articoli Markdown"
echo "============================================"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✓ Python3 trovato: $(python3 --version)"
echo ""

# Installa dipendenze
echo "📦 Installazione dipendenze..."
pip install edge-tts

echo ""
echo "============================================"
echo "✅ Setup completato!"
echo ""
echo "🚀 Per generare gli MP3:"
echo "   cd /mnt/git/articolo"
echo "   scripts/audio/play_audio.sh"
echo ""
echo "📖 Documentazione completa:"
echo "   cat scripts/audio/README_AUDIO_PLAYER.md"
echo "============================================"

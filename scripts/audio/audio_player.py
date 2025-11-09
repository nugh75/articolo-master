#!/usr/bin/env python3
"""
Generatore di audio da articoli Markdown.
Legge le sezioni del file, pulisce il Markdown e crea un MP3 per ciascun paragrafo.
"""

import argparse
import asyncio
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

try:
    import edge_tts  # type: ignore
except ImportError:  # pragma: no cover - gestito in main
    edge_tts = None

# Configurazione voci (Italiano usa Isabella come richiesto)
VOICES = {
    "it": "it-IT-IsabellaNeural",
    "en": "en-US-GuyNeural",
    "en_f": "en-GB-SoniaNeural",
}

CHUNK_SIZE = 3000  # caratteri per chunk (circa 30-45 secondi)


class MarkdownAudioBuilder:
    """Converte le sezioni Markdown in file MP3"""

    def __init__(self, markdown_file: Path):
        if edge_tts is None:
            raise RuntimeError("edge-tts non installato. Esegui: pip install edge-tts")

        self.markdown_file = Path(markdown_file)
        if not self.markdown_file.exists():
            raise FileNotFoundError(self.markdown_file)

        cache_dir = os.environ.get("MD_AUDIO_CACHE_DIR")
        if cache_dir:
            self.output_dir = Path(cache_dir).expanduser()
        else:
            self.output_dir = (
                Path(__file__).resolve().parent.parent / "output" / "audio"
            )
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.chunk_dir = self.output_dir / "_chunks"
        self.chunk_dir.mkdir(parents=True, exist_ok=True)

        flag_values = {"1", "true", "yes", "on"}
        self.keep_files = os.environ.get("MD_AUDIO_KEEP_FILES", "").strip().lower() in flag_values

        ssh_target = os.environ.get("MD_AUDIO_SSH_TARGET", "").strip()
        self.ssh_target = ssh_target or None
        ssh_opts = os.environ.get("MD_AUDIO_SSH_OPTIONS", "")
        self.ssh_options = shlex.split(ssh_opts) if ssh_opts else []

        self.sections = self._extract_sections()
        self.voice_env_prefix = "MD_AUDIO_VOICE_"

    # ------------------------------------------------------------------ Parsing
    def _extract_sections(self):
        content = self.markdown_file.read_text(encoding="utf-8")
        section_pattern = r"^##\s+(.+?)$"
        matches = list(re.finditer(section_pattern, content, re.MULTILINE))

        lang_pattern = r"<!--\s*lang:(en|it)\s*-->"
        current_lang = "it"

        sections = []
        for idx, match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
            raw_section = content[start:end].strip()

            pre_section = content[max(0, match.start() - 200):match.start()]
            lang_match = re.findall(lang_pattern, pre_section)
            if lang_match:
                current_lang = lang_match[-1]

            cleaned = self._clean_markdown(raw_section)
            if cleaned and len(cleaned) > 50:
                sections.append(
                    {
                        "title": title,
                        "content": cleaned,
                        "language": current_lang,
                    }
                )
        return sections

    def _clean_markdown(self, text: str) -> str:
        """Rimuove la maggior parte dei marcatori Markdown lasciando solo il testo."""
        text = re.sub(r"\r\n?", "\n", text)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)  # commenti
        text = re.sub(r"```[\s\S]*?```", "", text)  # blocchi di codice
        text = re.sub(r"`([^`]+)`", r"\1", text)  # codice inline
        text = re.sub(r"!\[[^\]]*\]\([^\)]+\)", "", text)  # immagini
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # link
        text = re.sub(r"^\s*\[[^\]]+\]:\s+.*$", "", text, flags=re.MULTILINE)  # ref link
        text = re.sub(r"\[\^[^\]]+\]", "", text)  # footnote refs
        text = re.sub(r"^\[\^[^\]]+\]:\s+.*$", "", text, flags=re.MULTILINE)  # footnote def
        text = re.sub(r"<[^>]+>", " ", text)  # HTML
        text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)  # heading
        text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)  # blockquote
        text = re.sub(r"^(\s*)([-*+]|(\d+\.))\s+", r"\1", text, flags=re.MULTILINE)  # liste
        text = re.sub(r"__|\*\*|[_*]", "", text)  # bold/italic residui
        text = re.sub(r"\[@[^\]]+\]", "", text)  # citazioni zotero
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()

    # ------------------------------------------------------------------ Utility
    def _split_into_chunks(self, text, chunk_size=CHUNK_SIZE):
        chunks = []
        current = ""
        sentences = re.split(r"([.!?]\s+|\n\n)", text)

        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            separator = sentences[i + 1] if i + 1 < len(sentences) else ""
            if len(current) + len(sentence) + len(separator) <= chunk_size:
                current += sentence + separator
            else:
                if current:
                    chunks.append(current.strip())
                current = sentence + separator

        if current:
            chunks.append(current.strip())
        return chunks

    def _slugify(self, text):
        normalized = unicodedata.normalize("NFKD", text)
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        ascii_text = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower()).strip("-")
        slug = ascii_text or "sezione"
        return slug[:80]

    def _build_output_path(self, slug):
        base = slug or "sezione"
        candidate = base
        counter = 1
        output = self.output_dir / f"{candidate}.mp3"
        while output.exists():
            candidate = f"{base}-{counter}"
            output = self.output_dir / f"{candidate}.mp3"
            counter += 1
        return output

    def _clear_chunk_files(self):
        if not self.chunk_dir.exists():
            return
        for chunk in self.chunk_dir.glob("*.mp3"):
            try:
                chunk.unlink()
            except OSError:
                pass

    async def _generate_chunk_audio(self, text, voice, chunk_idx, total_chunks):
        output_file = self.chunk_dir / f"chunk_{chunk_idx:03d}.mp3"
        print(f"   Generando chunk {chunk_idx + 1}/{total_chunks}...", end="\r")
        communicate = edge_tts.Communicate(text, voice, rate="+0%", volume="+0%")
        await communicate.save(str(output_file))
        return output_file

    async def _generate_all_chunks(self, text, language):
        chunks = self._split_into_chunks(text)
        voice = self._resolve_voice(language)
        print(f"\n📦 Diviso in {len(chunks)} parti")
        print(f"🎤 Voce: {voice}")

        tasks = [
            self._generate_chunk_audio(chunk, voice, i, len(chunks))
            for i, chunk in enumerate(chunks)
        ]

        chunk_files = []
        for i in range(0, len(tasks), 3):
            batch = tasks[i : i + 3]
            results = await asyncio.gather(*batch)
            chunk_files.extend(results)

        print("✅ Generazione completata!")
        return chunk_files

    def _resolve_voice(self, language):
        env_key = f"{self.voice_env_prefix}{language.upper()}"
        env_voice = os.environ.get(env_key, "").strip()
        if env_voice:
            return env_voice
        return VOICES.get(language, VOICES["it"])

    def _merge_chunks(self, title, chunk_files):
        if not chunk_files:
            return None
        slug = self._slugify(title)
        output_path = self._build_output_path(slug)
        with open(output_path, "wb") as merged:
            for chunk in chunk_files:
                with open(chunk, "rb") as piece:
                    shutil.copyfileobj(piece, merged)
        print(f"💾 File MP3 creato: {output_path.name}")
        print(f"📁 Percorso: {output_path}")
        return output_path

    def _send_via_ssh(self, audio_file):
        if not self.ssh_target or not audio_file:
            return
        cmd = ["scp", *self.ssh_options, str(audio_file), self.ssh_target]
        print(f"📡 Invio via SSH → {self.ssh_target}")
        try:
            subprocess.run(cmd, check=True)
            print("✅ Trasferimento completato")
        except FileNotFoundError:
            print("❌ 'scp' non disponibile. Installa openssh-client per usare l'invio automatico.")
        except subprocess.CalledProcessError as exc:
            print(f"❌ Errore trasferimento SSH (codice {exc.returncode})")

    # ------------------------------------------------------------------ Public API
    def build_section(self, section):
        title = section["title"]
        text = section["content"]
        language = section["language"]

        print("\n" + "=" * 60)
        print(f"🎵 {title}")
        print("=" * 60)
        print(f"📄 Lingua: {language.upper()}")
        print(f"📏 Lunghezza: {len(text)} caratteri (~{len(text.split())} parole)")

        self._clear_chunk_files()

        try:
            chunk_files = asyncio.run(self._generate_all_chunks(text, language))
        except Exception as exc:
            print(f"❌ Errore generazione audio: {exc}")
            return None

        if not chunk_files:
            print("❌ Nessun audio generato")
            return None

        merged_file = self._merge_chunks(title, chunk_files)
        self._send_via_ssh(merged_file)
        self._clear_chunk_files()
        return merged_file

    def build_all_sections(self, filters=None, languages=None):
        produced = []
        targets = self.sections

        if languages:
            lang_set = {lang.lower() for lang in languages}
            targets = [s for s in targets if s["language"].lower() in lang_set]
            if not targets:
                print("⚠️  Nessuna sezione appartiene alle lingue selezionate.")
                return produced

        if filters:
            filters_lower = [f.lower() for f in filters]

            def match(section_title):
                title_lower = section_title.lower()
                return any(fragment in title_lower for fragment in filters_lower)

            targets = [s for s in targets if match(s["title"])]
            if not targets:
                print("⚠️  Nessuna sezione corrisponde ai filtri forniti.")
                return produced

        for section in targets:
            audio_file = self.build_section(section)
            if audio_file:
                produced.append(audio_file)

        return produced

    def cleanup(self):
        self._clear_chunk_files()
        try:
            self.chunk_dir.rmdir()
        except OSError:
            pass

        if self.keep_files:
            saved = list(self.output_dir.glob("*.mp3"))
            if saved:
                print(f"\n💾 Audio salvati in: {self.output_dir}")
            else:
                print("\nℹ️  Nessun file audio generato.")
            return

        for audio_file in self.output_dir.glob("*.mp3"):
            try:
                audio_file.unlink()
            except OSError:
                pass
        try:
            self.output_dir.rmdir()
        except OSError:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="Genera MP3 da un articolo Markdown.")
    parser.add_argument(
        "markdown",
        nargs="?",
        help="File Markdown da convertire (default: bridging-the-gap-article-draft.md)",
    )
    parser.add_argument(
        "--section",
        action="append",
        help="Filtra le sezioni da convertire (match parziale, ripetibile).",
    )
    parser.add_argument(
        "--language",
        action="append",
        choices=("it", "en"),
        help="Converte solo le sezioni della lingua indicata (ripetibile).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    default_file = Path(__file__).parent.parent / "bridging-the-gap-article-draft.md"

    if args.markdown:
        md_file = Path(args.markdown)
    elif default_file.exists():
        md_file = default_file
    else:
        print("❌ Specifica il file Markdown da convertire.")
        print(f"   python {Path(__file__).name} <file.md>")
        sys.exit(1)

    if not md_file.exists():
        print(f"❌ File non trovato: {md_file}")
        sys.exit(1)

    print("🔍 Verifica dipendenze...")
    if edge_tts is None:
        print("❌ edge-tts non installato. Esegui: pip install edge-tts")
        sys.exit(1)

    builder = None
    produced = []
    try:
        builder = MarkdownAudioBuilder(md_file)
        print(f"📄 Sezioni trovate: {len(builder.sections)}")
        produced = builder.build_all_sections(filters=args.section, languages=args.language)
    except KeyboardInterrupt:
        print("\n\n👋 Interruzione utente")
    except Exception as exc:
        print(f"\n❌ Errore: {exc}")
        import traceback

        traceback.print_exc()
    finally:
        if builder:
            builder.cleanup()

    if produced:
        print("\n======================================")
        print("✅ Conversione completata")
        for file_path in produced:
            print(f" - {file_path.name}")
        print("======================================")
    else:
        print("\n⚠️  Nessun file audio generato.")


if __name__ == "__main__":
    main()

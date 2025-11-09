#!/usr/bin/env python3
"""
Sincronizza modifiche provenienti da un DOCX esterno (es. Google Docs)
con il file Markdown sorgente.

Workflow tipico:
1. Scarica il DOCX collaborativo da Google Drive.
2. Esegui:
     python scripts/analysis/docx_sync.py path/al/file.docx \
            --target bridging-the-gap-article-draft.md
3. Lo script conserva il front matter del Markdown (title, author, ecc.),
   sostituisce il corpo con il contenuto convertito via Pandoc e crea
   automaticamente un backup del file originale.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def check_pandoc() -> None:
    """Ensure pandoc is available."""
    result = shutil.which("pandoc")
    if result is None:
        sys.stderr.write("Errore: 'pandoc' non trovato nel PATH. Installalo prima di procedere.\n")
        sys.exit(1)


def convert_docx_to_markdown(docx_path: Path) -> str:
    """Use pandoc to convert a DOCX file to GitHub-flavored Markdown."""
    cmd = [
        "pandoc",
        str(docx_path),
        "-f",
        "docx",
        "-t",
        "gfm",
        "--wrap=none",
    ]
    try:
        completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr)
        raise SystemExit(f"Errore durante la conversione pandoc ({exc.returncode}).") from exc
    return completed.stdout


def split_front_matter(content: str) -> tuple[str, str]:
    """
    Return (front_matter, body).
    Front matter must be fenced by lines containing only '---'.
    """
    lines = content.splitlines()
    if not lines:
        return "", ""
    if lines[0].strip() != "---":
        return "", content
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            front = "\n".join(lines[: idx + 1]) + "\n"
            body = "\n".join(lines[idx + 1 :]).lstrip("\n")
            return front, body
    # Malformed front matter; treat whole content as body
    return "", content


def backup_target(target: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = target.with_suffix(target.suffix + f".backup.{timestamp}")
    shutil.copy2(target, backup_path)
    return backup_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa modifiche da un DOCX collaborativo nel Markdown sorgente."
    )
    parser.add_argument("docx", type=Path, help="File DOCX da importare")
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("bridging-the-gap-article-draft.md"),
        help="File Markdown da aggiornare (default: bridging-the-gap-article-draft.md)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Non creare un backup automatico del file target",
    )
    args = parser.parse_args()

    if not args.docx.exists():
        raise SystemExit(f"File DOCX non trovato: {args.docx}")

    if not args.target.exists():
        raise SystemExit(f"File target non trovato: {args.target}")

    check_pandoc()

    converted_body = convert_docx_to_markdown(args.docx).strip("\n") + "\n"

    target_text = args.target.read_text()
    front, _ = split_front_matter(target_text)

    if not args.no_backup:
        backup_path = backup_target(args.target)
        print(f"✓ Backup creato: {backup_path}")

    new_content = []
    if front:
        new_content.append(front.rstrip("\n"))
        new_content.append("")  # blank line between front matter and body
    new_content.append(converted_body.rstrip("\n"))
    new_content.append("")
    args.target.write_text("\n".join(new_content))
    print(f"✓ Aggiornato: {args.target}")
    print("Nota: verifica manualmente le differenze prima di committare.")


if __name__ == "__main__":
    main()

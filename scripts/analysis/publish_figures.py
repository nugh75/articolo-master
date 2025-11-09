#!/usr/bin/env python3
"""
Sincronizza le figure pubblicate copiandole dagli export correnti
(`analysis/exports/latest`) verso `assets/figures/published` e rigenera
`assets/figures/manifest.csv`.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
from typing import Iterable

FIG_PATTERN = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)(?P<attrs>\{[^}]*\})?", re.MULTILINE
)
PUBLISHED_PREFIX = "assets/figures/published/"


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Impossibile trovare la root del repository")


def load_paths(repo_root: Path) -> dict:
    config_path = repo_root / "config" / "paths.json"
    with config_path.open() as fp:
        return json.load(fp)


def parse_figures(markdown: Path, repo_root: Path) -> list[dict]:
    text = markdown.read_text()
    figures: list[dict] = []

    for match in FIG_PATTERN.finditer(text):
        path = match.group("path")
        if PUBLISHED_PREFIX not in path:
            continue
        attrs = match.group("attrs") or ""
        fig_id = ""
        if "#fig:" in attrs:
            remainder = attrs.split("#fig:", 1)[1]
            fig_id = remainder.split()[0].rstrip("}")
        line_number = text.count("\n", 0, match.start()) + 1
        try:
            document = str(markdown.relative_to(repo_root))
        except ValueError:
            document = str(markdown.resolve())
        figures.append(
            {
                "document": document,
                "line": line_number,
                "alt_text": match.group("alt"),
                "article_path": path,
                "figure_id": fig_id,
            }
        )
    return figures


def ensure_sources(figures: Iterable[dict], source_root: Path, dest_root: Path, repo_root: Path) -> list[dict]:
    dest_root.mkdir(parents=True, exist_ok=True)
    copied: set[Path] = set()
    processed: list[dict] = []

    for fig in figures:
        if PUBLISHED_PREFIX not in fig["article_path"]:
            continue
        rel = Path(fig["article_path"].split(PUBLISHED_PREFIX, 1)[1])
        source = source_root / rel
        dest = dest_root / rel
        if not source.exists():
            raise FileNotFoundError(
                f"File sorgente mancante per {fig['figure_id'] or rel} "
                f"(documento: {fig['document']}, linea {fig['line']}): {source}"
            )
        if rel not in copied:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            copied.add(rel)
        fig = fig.copy()
        fig["published_path"] = str(dest.relative_to(repo_root))
        fig["source_export"] = str(source.relative_to(repo_root))
        processed.append(fig)
    return processed


def write_manifest(manifest: Path, rows: Iterable[dict]) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "document",
        "line",
        "figure_id",
        "alt_text",
        "article_path",
        "published_path",
        "source_export",
    ]
    with manifest.open("w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pubblica i grafici dai Markdown indicati.")
    parser.add_argument(
        "--article",
        action="append",
        dest="articles",
        type=Path,
        help="File Markdown da analizzare (ripetere l'opzione per più documenti).",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Cartella contenente gli export dell'analisi (default: analysis/exports/latest).",
    )
    parser.add_argument(
        "--dest-root",
        type=Path,
        help="Cartella di destinazione per le figure pubblicate (default: assets/figures/published).",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Percorso del file manifest da rigenerare (default: assets/figures/manifest.csv).",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    paths = load_paths(repo_root)

    source_root = (repo_root / paths["analysis"]["exports_latest_dir"]).resolve()
    dest_root = (repo_root / paths["figures"]["published_dir"]).resolve()
    manifest_path = (repo_root / paths["figures"]["manifest"]).resolve()

    if args.source_root:
        source_root = args.source_root.resolve()
    if args.dest_root:
        dest_root = args.dest_root.resolve()
    if args.manifest:
        manifest_path = args.manifest.resolve()

    articles = args.articles or [Path("master.md")]
    all_figures: list[dict] = []
    for article in articles:
        md_path = (repo_root / article).resolve()
        all_figures.extend(parse_figures(md_path, repo_root))

    if not all_figures:
        raise RuntimeError(
            "Nessuna immagine con prefisso 'assets/figures/published/' trovata nei file indicati."
        )

    processed = ensure_sources(
        figures=all_figures,
        source_root=source_root,
        dest_root=dest_root,
        repo_root=repo_root,
    )
    write_manifest(manifest_path, processed)

    print(f"Copiate {len({row['published_path'] for row in processed})} figure in {dest_root}")
    print(f"Manifest aggiornato: {manifest_path} ({len(processed)} riferimenti)")


if __name__ == "__main__":
    main()

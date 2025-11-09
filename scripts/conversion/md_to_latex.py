#!/usr/bin/env python3
"""
Script per convertire file Markdown in LaTeX usando Pandoc
Gestisce preambolo personalizzato, citazioni e grafica
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LOCAL_PANDOC = Path('tools/bin/pandoc')
PANDOC_BIN = str(LOCAL_PANDOC) if LOCAL_PANDOC.exists() else 'pandoc'


def check_pandoc():
    """Verifica che pandoc sia installato e ritorna la versione"""
    try:
        result = subprocess.run([PANDOC_BIN, '--version'],
                              capture_output=True,
                              text=True,
                              check=True)
        version_str = result.stdout.split()[1]
        version_parts = version_str.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0

        print(f"✓ Pandoc trovato: {version_str}")

        # Versione 2.11+ supporta --citeproc
        # Versioni precedenti usano pandoc-citeproc come filtro
        if major > 2 or (major == 2 and minor >= 11):
            return (True, 'new')
        else:
            return (True, 'old')

    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Errore: Pandoc non trovato. Installalo con: sudo apt-get install pandoc")
        return (False, None)


def convert_md_to_latex(input_file, output_file=None, template=None,
                       bibliography=None, csl=None, options=None, pandoc_version='new'):
    """
    Converte un file Markdown in LaTeX usando Pandoc

    Args:
        input_file: Path del file .md di input
        output_file: Path del file .tex di output (opzionale)
        template: Path del template LaTeX (opzionale)
        bibliography: Path del file .bib per citazioni (opzionale)
        csl: Path del file .csl per stile citazioni (opzionale)
        options: Lista di opzioni aggiuntive per pandoc
        pandoc_version: 'new' per pandoc 2.11+, 'old' per versioni precedenti
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"✗ Errore: File {input_file} non trovato")
        return False, None

    # Determina output file
    if output_file is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        build_dir = Path('output') / f"build-{timestamp}"
        build_dir.mkdir(parents=True, exist_ok=True)
        output_path = build_dir / input_path.with_suffix('.tex').name
    else:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # Costruisci comando pandoc
    cmd = [
        PANDOC_BIN,
        str(input_path),
        '-o', str(output_path),
        '--from=markdown',
        '--to=latex',
        '--standalone',
        '--toc',
        '--toc-depth=3',
        '--lua-filter=filters/promote_headings.lua',
        '--lua-filter=filters/limit_image_width.lua',
        '--lua-filter=filters/language_filter.lua',
        '--lua-filter=filters/custom_numbering.lua',
    ]

    # Gestione citazioni basata sulla versione di pandoc
    if pandoc_version == 'new':
        cmd.append('--citeproc')  # Pandoc 2.11+
    elif pandoc_version == 'old':
        # Pandoc < 2.11: verifica se pandoc-citeproc è disponibile
        try:
            subprocess.run(['pandoc-citeproc', '--version'],
                         capture_output=True, check=True)
            cmd.extend(['--filter', 'pandoc-citeproc'])
            print("✓ Usando pandoc-citeproc per citazioni")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠ pandoc-citeproc non trovato - citazioni non processate")
            print("  Le citazioni verranno gestite da BibTeX/BibLaTeX in LaTeX")

    # Template personalizzato
    if template:
        template_path = Path(template)
        if template_path.exists():
            cmd.extend(['--template', str(template_path)])
            print(f"✓ Usando template: {template}")
        else:
            print(f"⚠ Warning: Template {template} non trovato, uso default")

    # Bibliografia (solo se pandoc può gestirla o se abbiamo il filtro)
    can_process_citations = (pandoc_version == 'new')
    if pandoc_version == 'old':
        try:
            subprocess.run(['pandoc-citeproc', '--version'],
                         capture_output=True, check=True)
            can_process_citations = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            can_process_citations = False

    if bibliography and can_process_citations:
        bib_path = Path(bibliography)
        if bib_path.exists():
            cmd.extend(['--bibliography', str(bib_path)])
            print(f"✓ Bibliografia: {bibliography}")
        else:
            print(f"⚠ Warning: File bibliografia {bibliography} non trovato")
    elif bibliography and not can_process_citations:
        print(f"ℹ Bibliografia: {bibliography} (sarà gestita da LaTeX, non da Pandoc)")

    # Stile citazioni CSL (solo se pandoc può gestirlo)
    if csl and can_process_citations:
        csl_path = Path(csl)
        if csl_path.exists():
            cmd.extend(['--csl', str(csl_path)])
            print(f"✓ Stile citazioni: {csl}")
        else:
            print(f"⚠ Warning: File CSL {csl} non trovato")
    elif csl and not can_process_citations:
        print(f"ℹ Stile CSL ignorato (pandoc troppo vecchio, usa BibTeX in LaTeX)")

    # Opzioni aggiuntive
    if options:
        cmd.extend(options)

    # Esegui conversione
    print(f"\n→ Conversione in corso: {input_file} → {output_file}")
    print(f"  Comando: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              check=True)

        print(f"✓ Conversione completata con successo!")
        print(f"✓ File LaTeX creato: {output_path}")

        # Mostra warnings se presenti
        if result.stderr:
            print(f"\n⚠ Warnings/Messages da Pandoc:\n{result.stderr}")

        return True, output_path

    except subprocess.CalledProcessError as e:
        print(f"✗ Errore durante la conversione:")
        print(f"  {e.stderr}")
        return False, None


def main():
    parser = argparse.ArgumentParser(
        description='Converti Markdown in LaTeX con Pandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:

  # Conversione base (usa path di default)
  %(prog)s bridging-the-gap-article-draft.md

  # Con template personalizzato
  %(prog)s bridging-the-gap-article-draft.md -t templates/template_latex.tex

  # Con bibliografia e citazioni
  %(prog)s bridging-the-gap-article-draft.md -b references/references.bib -c references/apa.csl

  # Completo con tutti i parametri
  %(prog)s bridging-the-gap-article-draft.md -o output/latex/output.tex -t templates/template_latex.tex -b references/references.bib -c references/apa.csl

  # Con opzioni aggiuntive pandoc
  %(prog)s bridging-the-gap-article-draft.md --pandoc-opts "--toc --toc-depth=3"
        """
    )

    parser.add_argument('input',
                       help='File Markdown di input (.md)')
    parser.add_argument('-o', '--output',
                       help='File LaTeX di output (.tex). Default: output/build_<timestamp>/[nome_input].tex')
    parser.add_argument('-t', '--template',
                       default='templates/template_latex.tex',
                       help='Template LaTeX personalizzato (default: templates/template_latex.tex)')
    parser.add_argument('-b', '--bibliography',
                       default='references/references.bib',
                       help='File bibliografia BibTeX (default: references/references.bib)')
    parser.add_argument('-c', '--csl',
                       default='references/apa.csl',
                       help='File stile citazioni CSL (default: references/apa.csl)')
    parser.add_argument('--no-template',
                       action='store_true',
                       help='Non usare template personalizzato')
    parser.add_argument('--no-bib',
                       action='store_true',
                       help='Non includere bibliografia')
    parser.add_argument('--no-csl',
                       action='store_true',
                       help='Non usare file CSL')
    parser.add_argument('--pandoc-opts',
                       help='Opzioni aggiuntive per pandoc (tra virgolette)')

    args = parser.parse_args()

    # Verifica pandoc
    pandoc_available, pandoc_version = check_pandoc()
    if not pandoc_available:
        sys.exit(1)

    if pandoc_version == 'old':
        print("⚠ Warning: Versione Pandoc < 2.11 rilevata.")
        print("  Tentativo di usare pandoc-citeproc come filtro...")

    print(f"\n{'='*60}")
    print(f"  Conversione Markdown → LaTeX")
    print(f"{'='*60}\n")

    # Prepara parametri
    template = None if args.no_template else args.template
    bibliography = None if args.no_bib else args.bibliography
    csl = None if args.no_csl else args.csl

    # Parse opzioni pandoc aggiuntive
    pandoc_options = []
    if args.pandoc_opts:
        pandoc_options = args.pandoc_opts.split()

    # Esegui conversione
    success, generated_path = convert_md_to_latex(
        input_file=args.input,
        output_file=args.output,
        template=template,
        bibliography=bibliography,
        csl=csl,
        options=pandoc_options,
        pandoc_version=pandoc_version
    )

    if success:
        print(f"\n{'='*60}")
        print(f"  Conversione completata!")
        print(f"{'='*60}\n")

        print("Prossimi passi:")
        print(f"  1. Modifica il preambolo in template_latex.tex se necessario")
        print(f"  2. Controlla il file generato: {generated_path}")
        print(f"  3. Compila con: pdflatex -output-directory {generated_path.parent} {generated_path}")
        print(f"     oppure:     latexmk -pdf -outdir={generated_path.parent} {generated_path}")
        sys.exit(0)
    else:
        print("\n✗ Conversione fallita")
        sys.exit(1)


if __name__ == '__main__':
    main()

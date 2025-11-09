#!/usr/bin/env python3
"""
Script to convert Markdown article to PDF with APA citations
Uses pandoc for conversion with comprehensive error handling
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
import urllib.request
from datetime import datetime

# Configuration
CONFIG = {
    'input_file': 'master.md',
    'output_dir': 'output/pdf',
    'template': 'templates/template_latex.tex',
    'csl_style': 'references/apa.csl',
    'bibliography': 'references/references.bib',
    'filters': ['scripts/md_to_latex.py'],
    'title': 'Your Article Title'
}

_CITEPROC_OPTS = None

LOCAL_PANDOC = Path('tools/bin/pandoc')
PANDOC_BIN = str(LOCAL_PANDOC) if LOCAL_PANDOC.exists() else 'pandoc'


def check_command(command):
    """Check if a command is available in PATH"""
    try:
        subprocess.run([command, '--version'],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")

    dependencies = {
        PANDOC_BIN: 'sudo apt-get install pandoc',
        'pdflatex': 'sudo apt-get install texlive-full'
    }

    missing = []
    for cmd, install_msg in dependencies.items():
        if check_command(cmd):
            print(f"  ✓ {cmd} found")
        else:
            print(f"  ✗ {cmd} NOT found")
            print(f"    Install with: {install_msg}")
            missing.append(cmd)

    if missing:
        print(f"\nError: Missing required dependencies: {', '.join(missing)}")
        return False

    print("  ✓ All dependencies satisfied\n")
    return True


def download_apa_style(csl_file):
    """Download APA 7th edition CSL style file"""
    if os.path.exists(csl_file):
        print(f"✓ APA style file already exists: {csl_file}")
        return True

    print(f"Downloading APA 7th edition citation style...")
    try:
        urllib.request.urlretrieve(CONFIG['apa_csl_url'], csl_file)
        print(f"✓ APA style downloaded: {csl_file}")
        return True
    except Exception as e:
        print(f"✗ Could not download APA style: {e}")
        print("  Continuing without custom CSL...")
        return False


def convert_ris_to_bibtex(ris_file, bib_file):
    """Convert RIS file to BibTeX format"""
    if not os.path.exists(ris_file):
        print(f"Warning: {ris_file} not found, skipping conversion")
        return False

    if os.path.exists(bib_file):
        print(f"✓ BibTeX file already exists: {bib_file}")
        return True

    print(f"Converting {ris_file} to {bib_file}...")

    # Try using pandoc to convert
    try:
        result = subprocess.run(
            [PANDOC_BIN, ris_file, '-t', 'biblatex', '-o', bib_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and os.path.exists(bib_file):
            print(f"✓ Converted to BibTeX: {bib_file}")
            return True
        else:
            print(f"✗ Conversion failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error during conversion: {e}")
        return False


def get_citeproc_opts():
    """Determine the appropriate citeproc option for pandoc"""
    global _CITEPROC_OPTS
    if _CITEPROC_OPTS is not None:
        return _CITEPROC_OPTS

    try:
        version_line = subprocess.check_output([PANDOC_BIN, '--version'], text=True).splitlines()[0]
        version = version_line.split()[1]
        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        if major > 2 or (major == 2 and minor >= 11):
            _CITEPROC_OPTS = ['--citeproc']
            return _CITEPROC_OPTS
    except Exception:
        pass

    if shutil.which('pandoc-citeproc'):
        _CITEPROC_OPTS = ['--filter', 'pandoc-citeproc']
    else:
        print("⚠ Warning: citeproc not available - citations will rely on LaTeX processing.")
        _CITEPROC_OPTS = []

    return _CITEPROC_OPTS


def run_pandoc(input_file, output_file, file_type='pdf'):
    """Run pandoc conversion with specified options"""

    # Base pandoc command
    cmd = [
        PANDOC_BIN, input_file,
        '-o', output_file,
        '--toc',
        '--toc-depth=3',
        '--lua-filter', 'filters/promote_headings.lua',
        '--lua-filter', 'filters/limit_image_width.lua',
        '--lua-filter', 'filters/language_filter.lua',
        '--lua-filter', 'filters/custom_numbering.lua',
        '-V', 'documentclass=article',
        '-V', 'papersize=a4',
        '-V', 'fontsize=12pt',
        '-V', 'geometry:margin=2.5cm',
        '-V', 'linestretch=1.5',
        '-V', 'fontfamily=times',
        '-V', 'linkcolor=blue',
        '-V', 'urlcolor=blue',
        '-V', 'toccolor=black',
        '--highlight-style=tango',
        '--metadata', f'title={CONFIG["title"]}',
        '--metadata', f'author={CONFIG["authors"]}',
    ]

    # Add bibliography if available
    if os.path.exists(CONFIG['bib_file']):
        cmd.extend(['--bibliography', CONFIG['bib_file']])

    citeproc_opts = get_citeproc_opts()

    # Only include CSL style if citeproc can process it
    if citeproc_opts and os.path.exists(CONFIG['csl_file']):
        cmd.extend(['--csl', CONFIG['csl_file']])
    elif not citeproc_opts and os.path.exists(CONFIG['csl_file']):
        print("ℹ CSL style skipped (citeproc unavailable).")

    # Add citeproc option if available
    cmd.extend(citeproc_opts)

    # Add PDF-specific options
    if file_type == 'pdf':
        pdf_engine = CONFIG.get('pdf_engine', 'pdflatex')
        cmd.extend(['--pdf-engine', pdf_engine])
    elif file_type == 'tex':
        cmd.append('--standalone')

    # Add verbose output
    cmd.append('--verbose')

    print(f"\nRunning pandoc command:")
    print(f"  {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Conversion timed out after 5 minutes"
    except Exception as e:
        return False, str(e)


def main():
    """Main conversion function"""
    print("=" * 60)
    print("Converting Markdown to PDF with APA citations")
    print("=" * 60)
    print()

    # Check input file exists
    if not os.path.exists(CONFIG['input_file']):
        print(f"Error: Input file '{CONFIG['input_file']}' not found!")
        return 1

    # Check dependencies
    if not check_dependencies():
        return 1

    # Download APA style
    print("Step 1: Preparing citation style...")
    download_apa_style(CONFIG['csl_file'])
    print()

    # Convert RIS to BibTeX if needed
    print("Step 2: Preparing bibliography...")
    convert_ris_to_bibtex('references/references.ris', CONFIG['bib_file'])
    print()

    # Prepare output paths
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    build_dir = Path(CONFIG['output_base_dir']) / f"build-{timestamp}"
    build_dir.mkdir(parents=True, exist_ok=True)
    output_pdf_path = build_dir / f"{CONFIG['output_basename']}.pdf"
    output_tex_path = build_dir / f"{CONFIG['output_basename']}.tex"

    # Convert to PDF
    print("Step 3: Converting to PDF...")
    print(f"  Input:  {CONFIG['input_file']}")
    print(f"  Output: {output_pdf_path}")

    success, output = run_pandoc(
        CONFIG['input_file'],
        str(output_pdf_path),
        'pdf'
    )

    if success:
        print()
        print("=" * 60)
        print(f"✓ PDF created successfully: {output_pdf_path}")
        print("=" * 60)
        print()

        # Show file size
        size = os.path.getsize(output_pdf_path)
        print(f"File size: {size:,} bytes ({size/1024:.1f} KB)")
    else:
        print()
        print("=" * 60)
        print("✗ Error creating PDF")
        print("=" * 60)
        print()
        print("Error details:")
        print(output)
        return 1

    # Also create LaTeX file
    print()
    print("Step 4: Creating standalone LaTeX file...")
    success, output = run_pandoc(
        CONFIG['input_file'],
        str(output_tex_path),
        'tex'
    )

    if success:
        print(f"✓ LaTeX file created: {output_tex_path}")
        manual_cmd = (
            f"pdflatex -output-directory {build_dir} {output_tex_path}"
        )
        print(f"  (Edit manually and compile with: {manual_cmd})")
    else:
        print(f"✗ Could not create LaTeX file: {output}")

    # Summary
    print()
    print("=" * 60)
    print("Conversion complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    generated_files = [
        output_pdf_path,
        output_tex_path,
        Path(CONFIG['csl_file']),
        Path(CONFIG['bib_file'])
    ]
    for file_path in generated_files:
        if file_path.exists():
            size = os.path.getsize(file_path)
            print(f"  ✓ {file_path} ({size:,} bytes)")

    print()
    print("To view the PDF:")
    print(f"  xdg-open {output_pdf_path}")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Convert RIS format to BibTeX format for use with LaTeX/pandoc
"""

import re
from pathlib import Path


def clean_string(s):
    """Clean string for BibTeX"""
    if not s:
        return ""
    # Remove newlines and extra spaces
    s = ' '.join(s.split())
    # Escape special LaTeX characters
    s = s.replace('&', r'\&')
    s = s.replace('%', r'\%')
    s = s.replace('_', r'\_')
    return s


def generate_cite_key(entry):
    """Generate a citation key from entry data"""
    author = entry.get('AU', ['Unknown'])[0].split(',')[0].split()[-1]
    year = entry.get('PY', ['0000'])[0]
    title_words = entry.get('TI', ['Untitled'])[0].split()[:2]
    title_part = ''.join(title_words).replace(' ', '')[:10]

    key = f"{author}{year}{title_part}"
    # Remove non-alphanumeric characters
    key = re.sub(r'[^a-zA-Z0-9]', '', key)
    return key


def ris_to_bibtex_entry(entry, entry_num):
    """Convert a single RIS entry to BibTeX format"""

    # Map RIS types to BibTeX types
    type_map = {
        'JOUR': 'article',
        'BOOK': 'book',
        'CHAP': 'inbook',
        'CONF': 'inproceedings',
        'RPRT': 'techreport',
        'THES': 'phdthesis',
        'UNPB': 'unpublished',
        'GEN': 'misc',
    }

    ris_type = entry.get('TY', ['GEN'])[0]
    bib_type = type_map.get(ris_type, 'misc')

    cite_key = generate_cite_key(entry)

    lines = [f"@{bib_type}{{{cite_key},"]

    # Title
    if 'TI' in entry:
        title = clean_string(entry['TI'][0])
        lines.append(f"  title = {{{title}}},")

    # Authors
    if 'AU' in entry:
        authors = ' and '.join(entry['AU'])
        lines.append(f"  author = {{{authors}}},")

    # Editors
    if 'ED' in entry:
        editors = ' and '.join(entry['ED'])
        lines.append(f"  editor = {{{editors}}},")

    # Year
    if 'PY' in entry:
        lines.append(f"  year = {{{entry['PY'][0]}}},")

    # Journal
    if 'JO' in entry:
        journal = clean_string(entry['JO'][0])
        lines.append(f"  journal = {{{journal}}},")

    # Publisher
    if 'PB' in entry:
        publisher = clean_string(entry['PB'][0])
        lines.append(f"  publisher = {{{publisher}}},")

    # Volume
    if 'VL' in entry:
        lines.append(f"  volume = {{{entry['VL'][0]}}},")

    # Issue/Number
    if 'IS' in entry:
        lines.append(f"  number = {{{entry['IS'][0]}}},")

    # Pages
    if 'SP' in entry and 'EP' in entry:
        lines.append(f"  pages = {{{entry['SP'][0]}--{entry['EP'][0]}}},")

    # ISBN
    if 'ISBN' in entry:
        lines.append(f"  isbn = {{{entry['ISBN'][0]}}},")

    # DOI
    if 'DOI' in entry:
        lines.append(f"  doi = {{{entry['DOI'][0]}}},")

    # URL
    if 'UR' in entry:
        url = entry['UR'][0]
        lines.append(f"  url = {{{url}}},")

    # Abstract
    if 'AB' in entry:
        abstract = clean_string(entry['AB'][0])
        lines.append(f"  abstract = {{{abstract}}},")

    # Note
    if 'N1' in entry:
        note = clean_string(entry['N1'][0])
        lines.append(f"  note = {{{note}}},")

    lines.append("}")
    lines.append("")

    return '\n'.join(lines)


def parse_ris_file(ris_path):
    """Parse RIS file and return list of entries"""
    with open(ris_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    current_entry = {}
    current_tag = None

    for line in content.split('\n'):
        line = line.strip()

        if not line:
            continue

        # Check for tag
        if line.startswith('TY  -'):
            # Start new entry
            if current_entry:
                entries.append(current_entry)
            current_entry = {}
            current_tag = 'TY'
            value = line[6:].strip()
            current_entry[current_tag] = [value]

        elif line.startswith('ER  -'):
            # End entry
            if current_entry:
                entries.append(current_entry)
                current_entry = {}

        elif '  - ' in line:
            # New tag
            parts = line.split('  - ', 1)
            current_tag = parts[0].strip()
            value = parts[1].strip() if len(parts) > 1 else ''

            if current_tag not in current_entry:
                current_entry[current_tag] = []
            current_entry[current_tag].append(value)

        elif current_tag and line:
            # Continuation of previous field
            current_entry[current_tag][-1] += ' ' + line

    # Add last entry if exists
    if current_entry:
        entries.append(current_entry)

    return entries


def convert_ris_to_bibtex(ris_path, bib_path):
    """Main conversion function"""
    print(f"Reading RIS file: {ris_path}")
    entries = parse_ris_file(ris_path)
    print(f"Found {len(entries)} entries")

    print(f"\nConverting to BibTeX format...")
    bibtex_entries = []
    for i, entry in enumerate(entries, 1):
        try:
            bib_entry = ris_to_bibtex_entry(entry, i)
            bibtex_entries.append(bib_entry)
            print(f"  ✓ Converted entry {i}/{len(entries)}: {entry.get('TI', ['No title'])[0][:50]}")
        except Exception as e:
            print(f"  ✗ Error converting entry {i}: {e}")

    # Write to file
    print(f"\nWriting BibTeX file: {bib_path}")
    with open(bib_path, 'w', encoding='utf-8') as f:
        f.write("% BibTeX bibliography converted from RIS format\n")
        f.write("% Generated automatically - may need manual adjustment\n\n")
        f.write('\n'.join(bibtex_entries))

    print(f"✓ Conversion complete!")
    print(f"  Input:  {ris_path} ({len(entries)} entries)")
    print(f"  Output: {bib_path}")
    print(f"\nYou can now use this with pandoc:")
    print(f"  pandoc document.md --bibliography={bib_path} --citeproc -o output.pdf")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        ris_file = sys.argv[1]
        bib_file = sys.argv[2] if len(sys.argv) > 2 else 'references.bib'
    else:
        ris_file = 'references.ris'
        bib_file = 'references.bib'

    if not Path(ris_file).exists():
        print(f"Error: File not found: {ris_file}")
        sys.exit(1)

    convert_ris_to_bibtex(ris_file, bib_file)

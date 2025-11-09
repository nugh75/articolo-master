#!/usr/bin/env python3
"""Print the correct citeproc option for the current pandoc installation."""

import shutil
import subprocess
from pathlib import Path


LOCAL_PANDOC = Path('tools/bin/pandoc')
PANDOC_BIN = str(LOCAL_PANDOC) if LOCAL_PANDOC.exists() else 'pandoc'


def main() -> int:
    try:
        version_line = subprocess.check_output([PANDOC_BIN, '--version'], text=True).splitlines()[0]
        version = version_line.split()[1]
        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        if major > 2 or (major == 2 and minor >= 11):
            print('--citeproc')
            return 0
    except Exception:
        # Fall back to checking for pandoc-citeproc
        pass

    if shutil.which('pandoc-citeproc'):
        print('--filter pandoc-citeproc')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

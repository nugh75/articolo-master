#!/usr/bin/env python3
"""
Script to add language markers to bilingual markdown content.
Converts italic paragraphs (assumed to be Italian translations) 
to use <!-- lang:it --> markers, and English paragraphs to use <!-- lang:en --> markers.
"""

import re
import sys

def process_markdown(content):
    """
    Process markdown content to add language markers.
    
    Assumes pattern:
    - English paragraph (no italic)
    - Italian paragraph (starts with *)
    """
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an italic paragraph (Italian translation)
        if line.strip().startswith('*') and line.strip().endswith('*') and len(line.strip()) > 2:
            # This is an Italian paragraph
            # Check if previous non-empty line needs English marker
            if result and not result[-1].strip().startswith('<!--'):
                # Find last non-empty line that's not already marked
                for j in range(len(result) - 1, -1, -1):
                    if result[j].strip() and not result[j].strip().startswith('<!--'):
                        # Check if this looks like English content (not a heading)
                        if not result[j].strip().startswith('#'):
                            # Insert English markers around previous content
                            # Find the start of the English paragraph
                            start_idx = j
                            while start_idx > 0 and result[start_idx - 1].strip() and not result[start_idx - 1].strip().startswith('<!--'):
                                start_idx -= 1
                                if result[start_idx].strip().startswith('#'):
                                    start_idx += 1
                                    break
                            
                            # Insert opening marker
                            result.insert(start_idx, '<!-- lang:en -->')
                            # Insert closing marker after the last line
                            result.insert(j + 2, '<!-- /lang:en -->')
                            result.append('')
                        break
            
            # Remove italic markers and add Italian markers
            italian_text = line.strip()[1:-1].strip()  # Remove surrounding *
            result.append('<!-- lang:it -->')
            result.append(italian_text)
            result.append('<!-- /lang:it -->')
            
        else:
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed = process_markdown(content)
        
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + '.marked'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed)
        
        print(f"Processed {input_file} -> {output_file}")
    else:
        # Read from stdin
        content = sys.stdin.read()
        processed = process_markdown(content)
        print(processed)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Script to automatically add language markers to markdown sections with Italian translations.
Finds paragraphs in italic (assumed Italian) preceded by English paragraphs and wraps them.
"""

import re
import sys

def add_language_markers(content):
    """Add language markers to content with pattern: English para + Italian para (italic)"""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is already marked
        if line.strip().startswith('<!--'):
            result.append(line)
            i += 1
            continue
            
        # Check if this is a full italic paragraph (Italian translation)
        # Pattern: starts with *, ends with *, not empty, not heading
        is_italic_para = (
            line.strip().startswith('*') and 
            line.strip().endswith('*') and 
            len(line.strip()) > 2 and
            not line.strip().startswith('#')
        )
        
        if is_italic_para:
            # Remove italic markers
            italian_text = line.strip()[1:-1]  # Remove first and last *
            
            # Look back to find the English paragraph
            # It should be the last non-empty, non-comment line before this
            english_start = -1
            english_end = -1
            
            for j in range(len(result) - 1, -1, -1):
                prev_line = result[j].strip()
                if not prev_line:  # Empty line
                    continue
                if prev_line.startswith('<!--'):  # Already marked
                    break
                if prev_line.startswith('#'):  # Heading
                    break
                # Found potential English text
                if english_end == -1:
                    english_end = j
                english_start = j
                # Check if previous line is also part of paragraph
                if j > 0 and result[j-1].strip() and not result[j-1].strip().startswith('<!--') and not result[j-1].strip().startswith('#'):
                    continue
                else:
                    break
            
            # If we found English text, wrap it
            if english_start != -1 and english_end != -1:
                # Insert markers around English
                result.insert(english_start, '<!-- lang:en -->')
                result.insert(english_end + 2, '<!-- /lang:en -->')
                result.append('')
            
            # Add Italian markers
            result.append('<!-- lang:it -->')
            result.append(italian_text)
            result.append('<!-- /lang:it -->')
            
        else:
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 auto_mark_languages.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + '.marked'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    marked_content = add_language_markers(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(marked_content)
    
    print(f"✓ Processed: {input_file} -> {output_file}")
    print(f"  Added language markers to bilingual content")

if __name__ == '__main__':
    main()

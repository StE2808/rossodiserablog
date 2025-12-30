#!/usr/bin/env python3
"""
Fix smart quotes in Jekyll post front matter.
Replaces curly quotes with straight quotes to fix YAML parsing issues.
"""

import glob
import re

def fix_smart_quotes(content):
    """Replace smart quotes with straight quotes"""
    # Replace smart double quotes
    content = content.replace('"', '"')
    content = content.replace('"', '"')
    # Replace smart single quotes/apostrophes
    content = content.replace(''', "'")
    content = content.replace(''', "'")
    return content

def process_file(filepath):
    """Process a single markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has smart quotes in front matter
    front_matter_end = content.find('---', 3)
    if front_matter_end == -1:
        return False

    front_matter = content[:front_matter_end + 3]

    # Check if smart quotes exist
    has_smart_quotes = any(c in front_matter for c in ['"', '"', ''', '''])

    if has_smart_quotes:
        # Fix the content
        fixed_content = fix_smart_quotes(content)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        return True

    return False

def main():
    """Main function"""
    print("Fixing smart quotes in Jekyll posts...")
    print()

    fixed_count = 0
    total_count = 0

    for filepath in glob.glob('_posts/*.md'):
        total_count += 1
        if process_file(filepath):
            fixed_count += 1
            print(f"✓ Fixed: {filepath}")

    print()
    print(f"Total posts processed: {total_count}")
    print(f"Posts fixed: {fixed_count}")
    print(f"Posts unchanged: {total_count - fixed_count}")

if __name__ == '__main__':
    main()

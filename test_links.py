import os
import re

repo_dir = r'c:\Users\abdow\Downloads\Obsidian\waer-cybersecurity-kb'
broken_links = []

link_pattern = re.compile(r'\[.*?\]\((?!http|mailto|#)(.*?\.md.*?)\)')

for root, _, files in os.walk(repo_dir):
    if '.git' in root: continue
    for file in files:
        if not file.endswith('.md'): continue
        filepath = os.path.join(root, file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        links = link_pattern.findall(content)
        for link in links:
            clean_link = link.split('#')[0]
            target_path = os.path.normpath(os.path.join(root, clean_link))
            if not os.path.exists(target_path):
                # Also try checking if it was meant to be relative to the markdown file directory
                rel_path = os.path.relpath(filepath, repo_dir)
                broken_links.append((rel_path, link))

with open('links_report.txt', 'w', encoding='utf-8') as f:
    if not broken_links:
        f.write('All links are valid!')
    else:
        f.write(f'Found {len(broken_links)} broken links:\n')
        for file, link in broken_links:
            f.write(f'File: {file} --> Link: {link}\n')

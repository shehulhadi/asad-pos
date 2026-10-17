import re
with open('index.html', 'r') as f: html = f.read()

# Change file type to .txt for sharing
old_code = '''        const filename = `AsadTech_Backup_${new Date().toISOString().split('T')[0]}.json`;
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const file = new File([blob], filename, { type: 'application/json' });'''

new_code = '''        const filename = `AsadTech_Backup_${new Date().toISOString().split('T')[0]}.txt`;
        const blob = new Blob([jsonStr], { type: 'text/plain' });
        const file = new File([blob], filename, { type: 'text/plain' });'''

html = html.replace(old_code, new_code)

# Update the download function to also use text/plain
old_download = '''        const blob = new Blob([content], { type: 'application/json' });'''
new_download = '''        const blob = new Blob([content], { type: 'text/plain' });'''
html = html.replace(old_download, new_download)

with open('index.html', 'w') as f: f.write(html)

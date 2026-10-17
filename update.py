import re
with open('index.html', 'r') as f: content = f.read()
pattern = r'function exportJSON\(\) \{.*?\n    \}'
replacement = '''async function exportJSON() {
        const data = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('asad:')) data[key] = JSON.parse(localStorage.getItem(key));
        }
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const filename = \`AsadTech_Backup_\${new Date().toISOString().split('T')[0]}.json\`;
        const file = new File([blob], filename, { type: 'application/json' });
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            try { await navigator.share({ files: [file], title: 'Business Backup', text: 'Here is the backup file.' }); } catch (e) { console.log(e); }
        } else {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = filename; a.click();
            window.URL.revokeObjectURL(url);
            alert('Sharing not supported. File downloaded instead.');
        }
    }'''
content = re.sub(pattern, replacement, content, flags=re.DOTALL)
content = content.replace('Backup JSON', 'Share Backup File')
with open('index.html', 'w') as f: f.write(content)

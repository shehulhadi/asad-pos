import re
with open('index.html', 'r') as f: html = f.read()

# Replace exportJSON function
pattern = r'    async function exportJSON\(\) \{.*?\n    \}'
new_func = '''    async function exportJSON() {
        const data = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('asad:')) data[key] = JSON.parse(localStorage.getItem(key));
        }
        const jsonStr = JSON.stringify(data, null, 2);
        const filename = `AsadTech_Backup_${new Date().toISOString().split('T')[0]}.json`;
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const file = new File([blob], filename, { type: 'application/json' });

        // Try Native Share API (Google Drive, WhatsApp, etc.)
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            try {
                await navigator.share({ files: [file], title: 'Business Backup' });
                showToast('Backup shared', 'success');
                return;
            } catch (e) {
                if (e.name === 'AbortError') return; // User cancelled
            }
        }

        // Fallback: Beautiful Save Modal
        document.getElementById('modal-body').innerHTML = `
            <h3>Save Backup File</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Tap Download to save to your phone, or Copy to paste it into Google Keep/Notes.</p>
            <textarea id="backup-text" style="width:100%; height:150px; font-family:monospace; font-size:12px; padding:10px; border-radius:8px; border:1px solid var(--line); margin-bottom:12px;" readonly>${jsonStr}</textarea>
            <div class="row">
                <button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('backup-text').value).then(()=>showToast('Copied to clipboard!','success'))">📋 Copy</button>
                <button class="btn" onclick="downloadBackup('${filename}', document.getElementById('backup-text').value)">📥 Download</button>
            </div>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function downloadBackup(filename, content) {
        const blob = new Blob([content], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('File downloaded', 'success');
    }'''
html = re.sub(pattern, new_func, html, flags=re.DOTALL)

# Update button text
html = html.replace('📤 \${t.exportJSON}', '📤 Backup & Share')

with open('index.html', 'w') as f: f.write(html)

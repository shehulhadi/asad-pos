import re
with open('index.html', 'r') as f: html = f.read()

# 1. Replace the Copy button with a Share button in the modal HTML
old_modal_html = '''            <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Tap Download to save to your phone, or Copy to paste it into Google Keep/Notes.</p>
            <textarea id="backup-text" style="width:100%; height:150px; font-family:monospace; font-size:12px; padding:10px; border-radius:8px; border:1px solid var(--line); margin-bottom:12px;" readonly>${jsonStr}</textarea>
            <div class="row">
                <button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('backup-text').value).then(()=>showToast('Copied to clipboard!','success'))">📋 Copy</button>
                <button class="btn" onclick="downloadBackup('${filename}', document.getElementById('backup-text').value)">📥 Download</button>
            </div>'''

new_modal_html = '''            <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Tap Download to save to your phone, or Share to send the text via WhatsApp/Email.</p>
            <textarea id="backup-text" style="width:100%; height:150px; font-family:monospace; font-size:12px; padding:10px; border-radius:8px; border:1px solid var(--line); margin-bottom:12px;" readonly>${jsonStr}</textarea>
            <div class="row">
                <button class="btn btn-outline" onclick="shareBackupText()">📤 Share</button>
                <button class="btn" onclick="downloadBackup('${filename}', document.getElementById('backup-text').value)">📥 Download</button>
            </div>'''
html = html.replace(old_modal_html, new_modal_html)

# 2. Add the shareBackupText function
share_func = '''
    function shareBackupText() {
        const text = document.getElementById('backup-text').value;
        if (navigator.share) {
            navigator.share({
                title: 'Business Backup',
                text: text
            }).then(() => showToast('Shared successfully', 'success'))
              .catch(e => { 
                  if (e.name !== 'AbortError') {
                      console.log('Share failed', e);
                      // Fallback to copy if share fails unexpectedly
                      navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard instead!', 'success'));
                  }
              });
        } else {
            navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard!', 'success'));
        }
    }
'''
if 'function shareBackupText()' not in html:
    html = html.replace('    function importJSON(event) {', share_func + '\n    function importJSON(event) {')

with open('index.html', 'w') as f: f.write(html)

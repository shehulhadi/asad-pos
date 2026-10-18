with open('index.html', 'r') as f: html = f.read()

# 1. Update the modal HTML to say "Share File"
old_modal_html = '''<button class="btn btn-outline" onclick="shareBackupText()">📤 Share</button>'''
new_modal_html = '''<button class="btn btn-outline" onclick="shareBackupFile()">📤 Share File</button>'''
html = html.replace(old_modal_html, new_modal_html)

# 2. Replace shareBackupText with shareBackupFile logic
old_share_func = '''    function shareBackupText() {
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
    }'''

new_share_func = '''    function shareBackupFile() {
        const text = document.getElementById('backup-text').value;
        const filename = `AsadTech_Backup_${new Date().toISOString().split('T')[0]}.txt`;
        const blob = new Blob([text], { type: 'text/plain' });
        const file = new File([blob], filename, { type: 'text/plain' });

        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            navigator.share({
                files: [file],
                title: 'Business Backup',
                text: 'Here is the backup file.'
            }).then(() => showToast('File shared successfully', 'success'))
              .catch(e => {
                  if (e.name !== 'AbortError') {
                      console.log('Share failed', e);
                      showToast('Share failed. Please Download instead.', 'err');
                  }
              });
        } else {
            showToast('File sharing not supported. Please Download.', 'err');
        }
    }'''
html = html.replace(old_share_func, new_share_func)

with open('index.html', 'w') as f: f.write(html)

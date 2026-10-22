import re
with open('app.js', 'r') as f: js = f.read()

# 1. Add the Email Backup button to the Reports screen
old_reports_html = '''            <input type="file" id="import-file" accept=".json" style="display:none;" onchange="importJSON(event)">
            <button class="btn" style="background:#64748b;" onclick="document.getElementById('import-file').click()">📥 Import JSON Backup</button>
        </div>'''

new_reports_html = '''            <input type="file" id="import-file" accept=".json" style="display:none;" onchange="importJSON(event)">
            <button class="btn" style="background:#64748b;" onclick="document.getElementById('import-file').click()">📥 Import JSON Backup</button>
            
            <button class="btn" style="background:#2563eb; margin-top:12px;" onclick="emailBackup()">✉️ Email Backup File</button>
        </div>'''
js = js.replace(old_reports_html, new_reports_html)

# 2. Inject the emailBackup function
email_func = '''
async function emailBackup() {
    const data = {
        settings: JSON.parse(localStorage.getItem('elbabs:settings')) || {},
        inventory: JSON.parse(localStorage.getItem('elbabs:inventory')) || [],
        sales: JSON.parse(localStorage.getItem('elbabs:sales')) || [],
        expenses: JSON.parse(localStorage.getItem('elbabs:expenses')) || []
    };
    
    const jsonStr = JSON.stringify(data, null, 2);
    const filename = 'Elbabs_Backup_' + new Date().toISOString().split('T')[0] + '.json';
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const file = new File([blob], filename, { type: 'application/json' });

    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({
                files: [file],
                title: 'Elbabs Communications Backup',
                text: 'Please find attached the latest backup for Elbabs Communications.'
            });
        } catch (e) {
            console.log('Share failed', e);
        }
    } else {
        // Fallback: If sharing files is not supported, trigger a mailto link
        const subject = encodeURIComponent('Elbabs Communications Backup - ' + new Date().toISOString().split('T')[0]);
        const body = encodeURIComponent('Please find the backup file attached. (Note: You must download the file first using the Export button, then attach it to this email).');
        window.location.href = `mailto:?subject=${subject}&body=${body}`;
        alert("Your device doesn't support direct file sharing. The JSON file has been downloaded, you can manually attach it to your email.");
        exportJSON(); // Also download it as fallback
    }
}

'''
if 'function emailBackup()' not in js:
    js = js.replace('function icon(name) {', email_func + '\nfunction icon(name) {')

with open('app.js', 'w') as f: f.write(js)
print("Email backup feature added successfully.")

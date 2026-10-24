import re

# 1. Update index.html to include Toast and Dialog containers
with open('index.html', 'r') as f: html = f.read()
if 'id="toast-container"' not in html:
    modal_html = '''
    <div id="toast-container"></div>
    <div id="dialog-overlay" class="modal" style="z-index: 10000;">
        <div class="modal-content" style="text-align: center;">
            <h3 id="dialog-title">Title</h3>
            <p id="dialog-msg" style="font-size: 14px; color: var(--muted); margin-bottom: 24px;">Message</p>
            <div class="row">
                <button class="btn btn-outline" onclick="closeDialog()">Cancel</button>
                <button class="btn btn-primary" id="dialog-confirm-btn">Confirm</button>
            </div>
        </div>
    </div>
    '''
    html = html.replace('</body>', modal_html + '\n</body>')
    with open('index.html', 'w') as f: f.write(html)

# 2. Update style.css with Toast and Dialog styles
with open('style.css', 'r') as f: css = f.read()
if '#toast-container' not in css:
    css_addition = '''
/* Toast and Dialog Styles */
#toast-container { position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%); z-index: 2000; display: flex; flex-direction: column; gap: 10px; width: 90%; max-width: 350px; pointer-events: none; }
.toast { background: var(--ink); color: #fff; padding: 14px 20px; border-radius: 12px; font-size: 14px; font-weight: 600; box-shadow: var(--shadow-md); display: flex; align-items: center; gap: 10px; animation: slideUpToast 0.3s ease, fadeOut 0.3s ease 2.7s forwards; }
.toast.err { background: var(--danger); }
.toast.success { background: #059669; }
@keyframes slideUpToast { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes fadeOut { to { opacity: 0; transform: translateY(-10px); } }

/* Custom Dialog overrides */
#dialog-overlay { background: rgba(11,18,32,.7); backdrop-filter: blur(4px); }
#dialog-overlay .modal-content { max-width: 340px; padding: 24px; animation: pop .2s ease; }
@keyframes pop { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
#dialog-overlay .row { margin-top: 20px; }
#dialog-overlay .btn { margin-top: 0; }
'''
    with open('style.css', 'a') as f: f.write(css_addition)

# 3. Update app.js: Add helper functions and replace alerts/confirms
with open('app.js', 'r') as f: js = f.read()

# Add helper functions before the login function
helpers = '''
function showToast(msg, type = 'default') {
    const container = document.getElementById('toast-container');
    if(!container) return alert(msg);
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    let icon = type === 'success' ? '<svg class="ic" style="width:18px;height:18px;stroke:#fff;" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>' : (type === 'err' ? '<svg class="ic" style="width:18px;height:18px;stroke:#fff;" viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/></svg>' : '');
    toast.innerHTML = `${icon} <span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

function showDialog(title, msg, onConfirm) {
    const overlay = document.getElementById('dialog-overlay');
    if(!overlay) {
        if(confirm(title + '\\n\\n' + msg)) onConfirm();
        return;
    }
    document.getElementById('dialog-title').textContent = title;
    document.getElementById('dialog-msg').textContent = msg;
    const confirmBtn = document.getElementById('dialog-confirm-btn');
    const newBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
    newBtn.onclick = () => {
        closeDialog();
        if (onConfirm) onConfirm();
    };
    overlay.classList.add('active');
}

function closeDialog() {
    const overlay = document.getElementById('dialog-overlay');
    if(overlay) overlay.classList.remove('active');
}

'''
js = js.replace('function login() {', helpers + 'function login() {')

# Replace forceUpdate confirm
js = js.replace('''if (confirm("This will download the latest app version.\\nYOUR DATA WILL NOT BE DELETED.\\n\\nContinue?")) {
        caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k)))).then(() => {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.getRegistrations().then(regs => {
                    for(let r of regs) r.unregister();
                    window.location.reload(true);
                });
            } else {
                window.location.reload(true);
            }
        });
    }''', '''showDialog("Update App?", "This will download the latest app version. Your data will not be deleted.", () => {
        caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k)))).then(() => {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.getRegistrations().then(regs => {
                    for(let r of regs) r.unregister();
                    window.location.reload(true);
                });
            } else {
                window.location.reload(true);
            }
        });
    });''')

# Replace deleteDevice confirm
js = js.replace('''if (confirm("Are you sure you want to delete this device? This cannot be undone.")) {
        inventory = inventory.filter(p => p.id !== id);
        saveData('inventory', inventory);
        closeModal();
        nav('inventory');
    }''', '''showDialog("Delete Device?", "Are you sure you want to delete this device? This cannot be undone.", () => {
        inventory = inventory.filter(p => p.id !== id);
        saveData('inventory', inventory);
        closeModal();
        nav('inventory');
    });''')

# Replace deleteSale confirm
js = js.replace('''if (confirm("Are you sure? Deleting this sale will return the device to Available stock.")) {
        const sale = sales.find(s => s.id === id);
        if (sale) {
            const device = inventory.find(p => p.id === sale.deviceId);
            if (device) device.status = 'Available';
            saveData('inventory', inventory);
        }
        sales = sales.filter(s => s.id !== id);
        saveData('sales', sales);
        closeModal();
        nav('sales');
    }''', '''showDialog("Delete Sale?", "Are you sure? Deleting this sale will return the device to Available stock.", () => {
        const sale = sales.find(s => s.id === id);
        if (sale) {
            const device = inventory.find(p => p.id === sale.deviceId);
            if (device) device.status = 'Available';
            saveData('inventory', inventory);
        }
        sales = sales.filter(s => s.id !== id);
        saveData('sales', sales);
        closeModal();
        nav('sales');
    });''')

# Replace remaining alerts
js = re.sub(r"alert\('Storage Error: Could not save data\. Your device storage may be full\.'\);", "showToast('Storage Error: Could not save data. Device storage may be full.', 'err');", js)
js = re.sub(r"return alert\('Please fill Brand, Model and Selling Price'\);", "return showToast('Please fill Brand, Model and Selling Price', 'err');", js)
js = re.sub(r"alert\('Enter the Kakara device details below\. Customer info has been pre-filled as the Seller\.'\);", "showToast('Enter the Kakara device details below.', 'success');", js)
js = re.sub(r"return alert\('Please select a device\.'\);", "return showToast('Please select a device.', 'err');", js)
js = re.sub(r"return alert\('Please enter a valid selling price\.'\);", "return showToast('Please enter a valid selling price.', 'err');", js)
js = re.sub(r"return alert\('Device not found in inventory\.'\);", "return showToast('Device not found in inventory.', 'err');", js)
js = re.sub(r"return alert\('Enter a valid amount'\);", "return showToast('Enter a valid amount', 'err');", js)
js = re.sub(r"alert\(\"Your device doesn't support direct file sharing\. The JSON file has been downloaded\.\"\);", "showToast(\"Share not supported. File downloaded.\", 'default');", js)
js = re.sub(r"alert\('Data restored successfully! App will reload\.'\);", "showToast('Data restored successfully! Reloading...', 'success');", js)
js = re.sub(r"alert\('Error parsing file: ' \+ err\.message\);", "showToast('Error: ' + err.message, 'err');", js)
js = re.sub(r"alert\(\`Press back \$\{3 - backPressCount\} more time\$\{3 - backPressCount > 1 \? 's' : ''\} to exit\`\);", "showToast(\`Press back \${3 - backPressCount} more time\${3 - backPressCount > 1 ? 's' : ''} to exit\`, 'default');", js)

with open('app.js', 'w') as f: f.write(js)
print("Modals and toasts successfully injected.")

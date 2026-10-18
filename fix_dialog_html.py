with open('index.html', 'r') as f: html = f.read()

# 1. Re-inject the missing Dialog HTML right before the closing body tag
if 'id="dialog-overlay"' not in html:
    dialog_html = '''
    <!-- DIALOG MODAL (For Alerts/Confirms) -->
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
    html = html.replace('</body>', dialog_html + '\n</body>')

# 2. Update the showDialog function to use the new modal classes
old_show_dialog = '''    function showDialog(title, msg, onConfirm, isPrompt = false) {
        document.getElementById('dialog-title').textContent = title;
        if (isPrompt) {
            document.getElementById('dialog-msg').innerHTML = `<input type="password" id="dialog-input" style="width:100%; padding:12px; border:1.5px solid var(--line); border-radius:8px; font-size:16px; text-align:center; margin-top:10px;" placeholder="••••">`;
            setTimeout(() => document.getElementById('dialog-input').focus(), 100);
        } else {
            document.getElementById('dialog-msg').innerHTML = msg;
        }
        const confirmBtn = document.getElementById('dialog-confirm-btn');
        const newBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
        newBtn.onclick = () => {
            let val = isPrompt ? document.getElementById('dialog-input').value : true;
            closeDialog();
            if (onConfirm) onConfirm(val);
        };
        document.getElementById('dialog-overlay').classList.add('active');
    }
    function closeDialog() { document.getElementById('dialog-overlay').classList.remove('active'); }'''

new_show_dialog = '''    function showDialog(title, msg, onConfirm, isPrompt = false) {
        document.getElementById('dialog-title').textContent = title;
        if (isPrompt) {
            document.getElementById('dialog-msg').innerHTML = `<input type="password" id="dialog-input" style="width:100%; padding:12px; border:1.5px solid var(--line); border-radius:8px; font-size:16px; text-align:center; margin-top:10px;" placeholder="••••">`;
            setTimeout(() => document.getElementById('dialog-input').focus(), 100);
        } else {
            document.getElementById('dialog-msg').innerHTML = msg;
        }
        const confirmBtn = document.getElementById('dialog-confirm-btn');
        const newBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
        newBtn.onclick = () => {
            let val = isPrompt ? document.getElementById('dialog-input').value : true;
            closeDialog();
            if (onConfirm) onConfirm(val);
        };
        document.getElementById('dialog-overlay').classList.add('active');
    }
    function closeDialog() { document.getElementById('dialog-overlay').classList.remove('active'); }'''
html = html.replace(old_show_dialog, new_show_dialog)

# 3. Simplify the forceUpdate function for reliability
old_force = '''    async function forceUpdate() {
        showDialog("Update App?", "This will download the latest version.\\nYOUR STOCK, SALES, AND DEBTS WILL NOT BE DELETED.", async () => {
            try {
                if ('serviceWorker' in navigator) {
                    const registrations = await navigator.serviceWorker.getRegistrations();
                    for (let registration of registrations) { await registration.unregister(); }
                }
                const keys = await caches.keys();
                for (let key of keys) { await caches.delete(key); }
            } catch(e) { console.log('Cache clear error', e); }
            
            showToast('Clearing cache and updating...', 'success');
            setTimeout(() => {
                window.location.href = window.location.pathname + '?v=' + Date.now();
            }, 1000);
        });
    }'''

new_force = '''    async function forceUpdate() {
        showDialog("Update App?", "This will download the latest version.\\nYOUR STOCK, SALES, AND DEBTS WILL NOT BE DELETED.", async () => {
            showToast('Clearing cache and updating...', 'success');
            try {
                if ('serviceWorker' in navigator) {
                    const registrations = await navigator.serviceWorker.getRegistrations();
                    for (let registration of registrations) { await registration.unregister(); }
                }
                const keys = await caches.keys();
                for (let key of keys) { await caches.delete(key); }
            } catch(e) { console.log('Cache clear error', e); }
            
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        });
    }'''
html = html.replace(old_force, new_force)

with open('index.html', 'w') as f: f.write(html)

import re
with open('index.html', 'r') as f: html = f.read()

# 1. Force inject the Dialog HTML right before the closing body tag
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
# Remove if exists, then add at the end
html = re.sub(r'<!-- DIALOG MODAL.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
html = html.replace('</body>', dialog_html + '\n</body>')

# 2. Rewrite showDialog with a bulletproof fallback
old_show_dialog = re.search(r'    function showDialog\(title, msg, onConfirm, isPrompt = false\) \{.*?\n    \}', html, re.DOTALL).group(0)
new_show_dialog = '''    function showDialog(title, msg, onConfirm, isPrompt = false) {
        const overlay = document.getElementById('dialog-overlay');
        
        // Fallback to native browser dialogs if the HTML is missing or broken
        if (!overlay) {
            if (isPrompt) {
                const val = prompt(title + "\\n\\n" + msg);
                if (val !== null && onConfirm) onConfirm(val);
            } else {
                if (confirm(title + "\\n\\n" + msg)) {
                    if (onConfirm) onConfirm(true);
                }
            }
            return;
        }

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
        overlay.classList.add('active');
    }
    function closeDialog() { 
        const overlay = document.getElementById('dialog-overlay');
        if(overlay) overlay.classList.remove('active'); 
    }'''
html = html.replace(old_show_dialog, new_show_dialog)

# 3. Make forceUpdate (Clear Cache) bulletproof
old_force = re.search(r'    async function forceUpdate\(\) \{.*?\n    \}', html, re.DOTALL).group(0)
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
                // Force a hard reload bypassing all caches
                window.location.href = window.location.href.split('?')[0] + '?v=' + Date.now();
            }, 1000);
        });
    }'''
html = html.replace(old_force, new_force)

with open('index.html', 'w') as f: f.write(html)

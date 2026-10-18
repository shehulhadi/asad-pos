import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add Dark Mode CSS
dark_css = '''
        /* --- DARK MODE --- */
        body.dark {
            --bg: #0b1220; --surface: #131d33; --text: #f8fafc; --line: #334155; --muted: #94a3b8;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.3); --shadow-md: 0 6px 20px -6px rgba(0,0,0,0.5);
            --brand-soft: rgba(16,185,129,0.15); --danger-soft: rgba(220,38,38,0.15); --accent-soft: rgba(245,158,11,0.15);
            --blue-soft: rgba(37,99,235,0.15);
        }
        body.dark .card, body.dark .modal-content, body.dark .list-item, body.dark .stat, body.dark .empty, body.dark .dialog-box { background: var(--surface); border-color: var(--line); }
        body.dark .form-group input, body.dark .form-group select, body.dark textarea { background: #0f172a; color: #fff; border-color: #334155; }
        body.dark .btn-outline { background: transparent; color: var(--text); }
        body.dark .calc-box { background: rgba(16,185,129,0.1); border-color: #059669; }
        body.dark .periods > div { background: #0f172a; }
        body.dark .quick button { background: var(--surface); color: var(--text); }
        body.dark .segmented { background: #0f172a; }
        body.dark .segmented button.on { background: var(--surface); color: var(--text); }
        body.dark .stock-tile { background: var(--brand-soft); border-color: #059669; }
        body.dark .stock-tile.low { background: var(--danger-soft); border-color: var(--danger); }
'''
if 'body.dark {' not in html:
    html = html.replace('</style>', dark_css + '\n</style>')

# 2. Add Dark Mode and Directory UI to Settings
old_settings = '''            <button class="btn" onclick="saveSettings()">${t.saveSettings}</button>
            <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>'''
new_settings = '''            <div class="form-group" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; background:var(--bg); padding:12px; border-radius:8px;">
                <label style="margin:0; font-size:14px; font-weight:700;">Dark Mode</label>
                <input type="checkbox" id="set-dark-mode" style="width:20px; height:20px;" ${settings.darkMode ? 'checked' : ''}>
            </div>
            <button class="btn btn-outline" style="margin-top:16px;" onclick="openDirectory()">📂 Customer & Supplier Directory</button>
            <button class="btn" style="margin-top:16px;" onclick="saveSettings()">${t.saveSettings}</button>
            <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>'''
html = html.replace(old_settings, new_settings)

# 3. Update saveSettings logic
old_save = '''        settings.lang = newLang;
        settings.marginAlertPct = parseFloat(document.getElementById('set-margin').value) || 0;'''
new_save = '''        settings.lang = newLang;
        settings.darkMode = document.getElementById('set-dark-mode').checked;
        if(settings.darkMode) document.body.classList.add('dark');
        else document.body.classList.remove('dark');
        
        settings.marginAlertPct = parseFloat(document.getElementById('set-margin').value) || 0;'''
html = html.replace(old_save, new_save)

# 4. Apply Dark Mode on initial load
html = html.replace(
    "restoreSession();\n</script>",
    "if(settings.darkMode) document.body.classList.add('dark');\n    restoreSession();\n</script>"
)

# 5. Add the Directory logic
directory_js = '''
    function openDirectory() {
        const uniqueCustomers = {};
        sales.forEach(s => { if(s.customerName && s.customerName !== 'Walk-in') uniqueCustomers[s.customerName] = s.customerPhone; });
        
        const uniqueSuppliers = [...new Set(purchases.map(p => p.supplierName).filter(n => n && n !== 'Unknown'))];

        let custHtml = Object.keys(uniqueCustomers).map(c => `
            <div class="list-item neutral" style="padding:12px; margin-bottom:8px;">
                <div class="list-header"><span>${c}</span> <span style="font-size:12px; color:var(--muted);">${uniqueCustomers[c] || 'No phone'}</span></div>
                ${uniqueCustomers[c] ? `<div class="actions" style="margin-top:8px;">
                    <a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a>
                    <a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a>
                </div>` : ''}
            </div>
        `).join('');

        let suppHtml = uniqueSuppliers.map(s => `
            <div class="list-item neutral" style="padding:12px; margin-bottom:8px;">
                <div class="list-header"><span>${s}</span></div>
            </div>
        `).join('');

        document.getElementById('modal-body').innerHTML = `
            <h3>Directory</h3>
            <div class="segmented">
                <button class="on" id="dir-tab-cust" onclick="switchDirTab('cust')">Customers (${Object.keys(uniqueCustomers).length})</button>
                <button id="dir-tab-supp" onclick="switchDirTab('supp')">Suppliers (${uniqueSuppliers.length})</button>
            </div>
            <div id="dir-content-cust" style="max-height: 50vh; overflow-y:auto;">${custHtml || '<p style="text-align:center; color:var(--muted); font-size:13px;">No customers yet.</p>'}</div>
            <div id="dir-content-supp" style="display:none; max-height: 50vh; overflow-y:auto;">${suppHtml || '<p style="text-align:center; color:var(--muted); font-size:13px;">No suppliers yet.</p>'}</div>
            <button class="btn btn-outline" style="margin-top:16px;" onclick="closeModal()">Close</button>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function switchDirTab(tab) {
        document.getElementById('dir-tab-cust').classList.toggle('on', tab === 'cust');
        document.getElementById('dir-tab-supp').classList.toggle('on', tab === 'supp');
        document.getElementById('dir-content-cust').style.display = tab === 'cust' ? 'block' : 'none';
        document.getElementById('dir-content-supp').style.display = tab === 'supp' ? 'block' : 'none';
    }
'''
if 'function openDirectory()' not in html:
    html = html.replace('// --- Clear Cache ---', directory_js + '\n// --- Clear Cache ---')

with open('index.html', 'w') as f: f.write(html)

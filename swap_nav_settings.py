import re
with open('index.html', 'r') as f: html = f.read()
with open('app.js', 'r') as f: js = f.read()

# 1. Remove Settings icon from the top header in index.html
html = html.replace('<button class="icon-btn" id="btn-settings" onclick="openSettings()" title="Settings"></button>\n                ', '')

# 2. Remove Settings icon logic from loadApp in app.js
js = js.replace("document.getElementById('btn-settings').innerHTML = ico('settings');\n        ", "")
js = js.replace("document.getElementById('btn-settings').classList.toggle('show', owner);\n        ", "")

# 3. Update buildNav to remove Production and add Settings
old_nav = '''function buildNav() {
    const navEl = document.getElementById('bottom-nav');
    const t = i18n[settings.lang];
    const item = (v, icon, isLarge = false) => `<button class="nav-btn ${isLarge ? 'nav-btn-large' : ''}" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
    
    let html = item('dashboard', 'box'); 
    html += item('production', 'production');
    html += item('sales', 'sales', true); // Large middle button
    html += item('expenses', 'expenses');
    
    if (currentUser === 'owner') { html += item('analytics', 'dashboard'); } 
    else { html += item('debts', 'debts'); }
    
    navEl.innerHTML = html;
}'''

new_nav = '''function buildNav() {
    const navEl = document.getElementById('bottom-nav');
    const t = i18n[settings.lang];
    const item = (v, icon, isLarge = false) => `<button class="nav-btn ${isLarge ? 'nav-btn-large' : ''}" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
    
    let html = item('dashboard', 'box'); 
    html += item('sales', 'sales', true); // Large middle button
    html += item('expenses', 'expenses');
    
    if (currentUser === 'owner') { html += item('analytics', 'dashboard'); } 
    else { html += item('debts', 'debts'); }
    
    // Add Settings to bottom nav (opens modal)
    html += `<button class="nav-btn" onclick="openSettings()"><span class="pill">${ico('settings')}</span>${t.settings || 'Settings'}</button>`;
    
    navEl.innerHTML = html;
}'''
js = js.replace(old_nav, new_nav)

# 4. Update Quick Actions on the Stock page (renderDashboard) to include Production
old_quick = '''        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="nav('debts')">${ico('debts')} Debts</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')">${ico('report')} Reports</button>` : ''}
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
        </div>'''
new_quick = '''        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            <button onclick="nav('production')" style="flex: 1 1 45%;">${ico('production')} Production</button>
            <button onclick="nav('debts')" style="flex: 1 1 45%;">${ico('debts')} Debts</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 45%;">${ico('report')} Reports</button>` : ''}
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 45%;">📊 Close Day</button>
        </div>'''
js = js.replace(old_quick, new_quick)

with open('index.html', 'w') as f: f.write(html)
with open('app.js', 'w') as f: f.write(js)

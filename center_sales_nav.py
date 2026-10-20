with open('app.js', 'r') as f: js = f.read()

start_nav = js.find('function buildNav() {')
end_nav = js.find('function nav(view) {')

if start_nav != -1 and end_nav != -1:
    new_nav = '''function buildNav() {
    const navEl = document.getElementById('bottom-nav');
    const t = i18n[settings.lang];
    const item = (v, icon, isLarge = false) => `<button class="nav-btn ${isLarge ? 'nav-btn-large' : ''}" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
    
    let html = '';
    html += item('dashboard', 'box');       // 1. Stock
    html += item('expenses', 'expenses');   // 2. Expenses
    
    html += item('sales', 'sales', true);   // 3. Sales (Large Middle)
    
    if (currentUser === 'owner') { 
        html += item('analytics', 'dashboard'); // 4. Analytics
    } else { 
        html += item('debts', 'debts');         // 4. Debts
    }
    
    // 5. Settings
    html += `<button class="nav-btn" onclick="openSettings()"><span class="pill">${ico('settings')}</span>${t.settings || 'Settings'}</button>`;
    
    navEl.innerHTML = html;
}

'''
    js = js[:start_nav] + new_nav + js[end_nav:]

with open('app.js', 'w') as f: f.write(js)

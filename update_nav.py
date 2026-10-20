with open('app.js', 'r') as f: js = f.read()

old_build = '''function buildNav() {
    const navEl = document.getElementById('bottom-nav');
    const t = i18n[settings.lang];
    const item = (v, icon) => `<button class="nav-btn" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
    let html = item('dashboard', 'box'); 
    html += item('sales', 'sales') + item('production', 'production') + item('expenses', 'expenses');
    if (currentUser === 'owner') { html += item('analytics', 'dashboard'); } 
    else { html += item('debts', 'debts'); }
    navEl.innerHTML = html;
}'''

new_build = '''function buildNav() {
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
js = js.replace(old_build, new_build)

with open('app.js', 'w') as f: f.write(js)

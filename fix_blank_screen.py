import re
with open('app.js', 'r') as f: js = f.read()

# 1. Fix loadApp to remove references to deleted elements
start_load = js.find('function loadApp() {')
end_load = js.find('function logout() {')
if start_load != -1 and end_load != -1:
    new_load = '''function loadApp() {
    document.getElementById('login-view').classList.remove('active');
    document.getElementById('app-view').classList.add('active');
    document.getElementById('role-badge').textContent = currentUser === 'owner' ? 'Owner' : 'Staff';
    
    const ibUpdate = document.getElementById('ib-update');
    if (ibUpdate) ibUpdate.innerHTML = ico('refresh');
    const ibBackup = document.getElementById('ib-backup');
    if (ibBackup) ibBackup.innerHTML = ico('update');
    const ibLogout = document.getElementById('ib-logout');
    if (ibLogout) ibLogout.innerHTML = ico('logout');

    document.getElementById('pin-input').value = '';
    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    document.getElementById('app-title').textContent = bizName;
    
    buildNav();
    nav('dashboard');
}

'''
    js = js[:start_load] + new_load + js[end_load:]

# 2. Fix buildNav to ensure Sales is the middle large button
start_nav = js.find('function buildNav() {')
end_nav = js.find('function nav(view) {')
if start_nav != -1 and end_nav != -1:
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
}

'''
    js = js[:start_nav] + new_nav + js[end_nav:]

# 3. Fix nav routing so it doesn't crash on old links
start_router = js.find('function nav(view) {')
end_router = js.find('function openSettings() {')
if start_router != -1 and end_router != -1:
    new_router = '''function nav(view) {
    currentView = view;
    if (view === 'inventory') view = 'dashboard';
    
    document.querySelectorAll('.nav-btn').forEach(b => {
        if (b.dataset.view) {
            b.classList.toggle('active', b.dataset.view === view);
        }
    });
    
    const main = document.getElementById('main-content');
    main.innerHTML = '';
    main.scrollTop = 0;
    
    try {
        if (view === 'dashboard') renderDashboard(main);
        else if (view === 'analytics') renderAnalytics(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'reports') renderReports(main);
    } catch (e) {
        console.error(e);
        main.innerHTML = `<div style="padding:20px;text-align:center;color:var(--danger);">Error loading page: ${e.message}</div>`;
    }
}

'''
    js = js[:start_router] + new_router + js[end_router:]

# 4. Make sure the Quick Actions in renderDashboard have the Production button safely
start_quick = js.find('<div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">')
if start_quick != -1:
    end_quick = js.find('</div>', start_quick)
    if end_quick != -1:
        new_quick = '''<div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            <button onclick="nav('production')" style="flex: 1 1 45%;">${ico('production')} Production</button>
            <button onclick="nav('debts')" style="flex: 1 1 45%;">${ico('debts')} Debts</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 45%;">${ico('report')} Reports</button>` : ''}
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 45%;">📊 Close Day</button>
        </div>'''
        js = js[:start_quick] + new_quick + js[end_quick+6:]

with open('app.js', 'w') as f: f.write(js)

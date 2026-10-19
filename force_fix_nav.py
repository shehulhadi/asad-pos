import re
with open('index.html', 'r') as f: html = f.read()

# 1. Fix Translation Dictionary
if 'dashboard: "Stock"' not in html:
    html = html.replace('home: "Home", sales: "Sales"', 'home: "Home", dashboard: "Stock", analytics: "Analytics", sales: "Sales"')
    html = html.replace('home: "Gida", sales: "Tallace"', 'home: "Gida", dashboard: "Kaya", analytics: "Analytics", sales: "Tallace"')

# 2. Replace buildNav function completely
start_build = html.find('    function buildNav() {')
end_build = html.find('    function nav(view) {')
if start_build != -1 and end_build != -1:
    new_build = '''    function buildNav() {
        const navEl = document.getElementById('bottom-nav');
        const t = i18n[settings.lang];
        const item = (v, icon) => `<button class="nav-btn" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
        
        let html = item('dashboard', 'box'); 
        html += item('sales', 'sales') + item('production', 'production') + item('expenses', 'expenses');
        
        if (currentUser === 'owner') {
            html += item('analytics', 'dashboard');
        } else {
            html += item('debts', 'debts');
        }
        navEl.innerHTML = html;
    }

'''
    html = html[:start_build] + new_build + html[end_build:]

# 3. Replace nav function completely
start_nav = html.find('    function nav(view) {')
end_nav = html.find('    function openSettings() {')
if start_nav != -1 and end_nav != -1:
    new_nav = '''    function nav(view) {
        currentView = view;
        
        // Handle legacy view names
        if (view === 'inventory' || view === 'home') view = 'dashboard';
        
        const tabFor = { reports: 'analytics', inventory: 'dashboard', home: 'dashboard' };
        const activeTab = tabFor[view] || view;
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.view === activeTab));
        
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
            showToast("Error loading page: " + e.message, "err");
        }
    }

'''
    html = html[:start_nav] + new_nav + html[end_nav:]

# 4. Replace loadApp function completely
start_load = html.find('    function loadApp() {')
end_load = html.find('    function logout() {')
if start_load != -1 and end_load != -1:
    new_load = '''    function loadApp() {
        document.getElementById('login-view').classList.remove('active');
        document.getElementById('app-view').classList.add('active');
        document.getElementById('role-badge').textContent = currentUser === 'owner' ? 'Owner' : 'Staff';
        
        document.getElementById('ib-update').innerHTML = ico('refresh');
        document.getElementById('ib-backup').innerHTML = ico('update');
        document.getElementById('ib-logout').innerHTML = ico('logout');
        document.getElementById('btn-settings').innerHTML = ico('settings');
        
        const owner = currentUser === 'owner';
        document.getElementById('btn-settings').classList.toggle('show', owner);
        document.getElementById('pin-input').value = '';
        
        const bizName = settings.businessName || 'My Business';
        document.title = bizName;
        document.getElementById('app-title').textContent = bizName;
        
        buildNav();
        nav('dashboard'); // Always start on stock dashboard
    }

'''
    html = html[:start_load] + new_load + html[end_load:]

# 5. Ensure UI buttons match new flow
# Fix Quick Actions on Stock Dashboard
html = html.replace(
    '''<div class="quick" style="margin-bottom: 20px;">
                <button onclick="nav('debts')">${ico('debts')} Debts</button>
                ${currentUser === 'owner' ? `<button onclick="nav('reports')">${ico('report')} Reports</button>` : ''}
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>''',
    '''<div class="quick" style="margin-bottom: 20px;">
                <button onclick="nav('debts')">${ico('debts')} Debts</button>
                ${currentUser === 'owner' ? `<button onclick="nav('reports')">${ico('report')} Reports</button>` : ''}
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>'''
)

# Fix Quick Actions on Analytics page
html = html.replace(
    '''<div class="quick">
                <button onclick="nav('dashboard')">${ico('box')} Stock</button>
                <button onclick="nav('reports')">${ico('report')} Reports</button>
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>''',
    '''<div class="quick">
                <button onclick="nav('dashboard')">${ico('box')} Stock</button>
                <button onclick="nav('reports')">${ico('report')} Reports</button>
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>'''
)

with open('index.html', 'w') as f: f.write(html)

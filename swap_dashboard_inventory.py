import re
with open('index.html', 'r') as f: html = f.read()

# 1. Update Translations
html = html.replace('home: "Home", sales: "Sales"', 'home: "Home", dashboard: "Stock", analytics: "Analytics", sales: "Sales"')
html = html.replace('home: "Gida", sales: "Tallace"', 'home: "Gida", dashboard: "Kaya", analytics: "Analytics", sales: "Tallace"')

# 2. Rename the functions
html = html.replace('function renderDashboard(main) {', 'function renderAnalytics(main) {')
html = html.replace('function renderInventory(main) {', 'function renderDashboard(main) {')

# 3. Update the Bottom Navigation
old_nav = '''    function buildNav() {
        const navEl = document.getElementById('bottom-nav');
        const t = i18n[settings.lang];
        const item = (v, icon) => `<button class="nav-btn" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v]}</button>`;
        let html = currentUser === 'owner' ? item('dashboard', 'dashboard') : item('home', 'home');
        html += item('sales', 'sales') + item('production', 'production') + item('expenses', 'expenses') + item('debts', 'debts');
        navEl.innerHTML = html;
    }'''
new_nav = '''    function buildNav() {
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
    }'''
html = html.replace(old_nav, new_nav)

# 4. Update the Router
old_router = '''        if (view === 'home') renderHome(main);
        else if (view === 'dashboard') renderDashboard(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'inventory') renderInventory(main);
        else if (view === 'reports') renderReports(main);'''
new_router = '''        if (view === 'inventory') view = 'dashboard';
        currentView = view;
        const tabFor = { reports: 'analytics' };
        const activeTab = tabFor[view] || view;
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.view === activeTab));
        const main = document.getElementById('main-content');
        main.innerHTML = '';
        main.scrollTop = 0;
        
        if (view === 'dashboard') renderDashboard(main);
        else if (view === 'analytics') renderAnalytics(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'reports') renderReports(main);'''
html = html.replace(old_router, new_router)
# Remove the old nav routing logic above the router since we replaced it
html = re.sub(r'    function nav\(view\) \{\n        currentView = view;\n        const tabFor = \{.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n        \}', new_router, html, flags=re.DOTALL)

# 5. Update loadApp to start on Dashboard
html = html.replace("buildNav();\n        nav(owner ? 'dashboard' : 'home');", "buildNav();\n        nav('dashboard');")

# 6. Update the new renderDashboard (Stock) Quick Actions
old_new_dash = '''        main.innerHTML = `
            ${backBtn(currentUser === 'owner' ? 'dashboard' : 'home')}
            <div class="page-title">${t.inventory}</div>
            <div class="page-sub">Raw materials and finished blocks</div>'''
new_new_dash = '''        main.innerHTML = `
            <div class="quick" style="margin-bottom: 20px;">
                <button onclick="nav('debts')">${ico('debts')} Debts</button>
                ${currentUser === 'owner' ? `<button onclick="nav('reports')">${ico('report')} Reports</button>` : ''}
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>
            <div class="page-title">Stock & Inventory</div>
            <div class="page-sub">Raw materials and finished blocks</div>'''
html = html.replace(old_new_dash, new_new_dash)

# 7. Update the old Dashboard (Analytics) Quick Actions & Permissions
html = html.replace('if (currentUser !== \'owner\') return nav(\'home\');', 'if (currentUser !== \'owner\') return nav(\'dashboard\');')
old_ana_quick = '''            <div class="quick">
                <button onclick="nav('inventory')">${ico('box')} ${t.inventory}</button>
                <button onclick="nav('reports')">${ico('report')} ${t.reports}</button>
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>'''
new_ana_quick = '''            <div class="quick">
                <button onclick="nav('dashboard')">${ico('box')} Stock</button>
                <button onclick="nav('reports')">${ico('report')} Reports</button>
                <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
            </div>'''
html = html.replace(old_ana_quick, new_ana_quick)

# 8. Update Reports back button
html = html.replace('${backBtn(\'dashboard\')}', '${backBtn(\'analytics\')}')

with open('index.html', 'w') as f: f.write(html)

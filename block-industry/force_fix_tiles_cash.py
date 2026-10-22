import re
with open('app.js', 'r') as f: js = f.read()

# 1. Forcefully rewrite the nav function to route everything correctly
start_nav = js.find('function nav(view')
end_nav = js.find('function openSettings() {')
if start_nav != -1 and end_nav != -1:
    new_nav = '''function nav(view, btn = null, type = null, size = null) {
    currentView = view;
    if (type) stockType = type;
    if (size) stockSize = size;
    
    if (btn) {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    } else {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        if(document.querySelector(`.nav-btn[data-view="${view}"]`)) {
            document.querySelector(`.nav-btn[data-view="${view}"]`).classList.add('active');
        }
    }

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
        else if (view === 'stock_details') renderStockDetails(main, stockType, stockSize);
    } catch (e) {
        console.error(e);
        main.innerHTML = `<div style="padding:20px;text-align:center;color:var(--danger);">Error: ${e.message}</div>`;
    }
}

function openStockDetailsPage(type, size) {
    stockType = type;
    stockSize = size;
    nav('stock_details');
}

'''
    js = js[:start_nav] + new_nav + js[end_nav:]

# 2. Ensure the tile onclick uses the new function
js = js.replace("onclick=\"nav('stock_details', null, '${type}', '${size}')\"", "onclick=\"openStockDetailsPage('${type}', '${size}')\"")

# 3. Fix Cash in Hand (force replacement)
js = re.sub(r"const cashInHand = cashIn - allExpenses;", "const totalPurchaseCash = purchases.reduce((sum, p) => sum + (p.amountPaid || 0), 0);\n    const cashInHand = cashIn - allExpenses - totalPurchaseCash;", js)

with open('app.js', 'w') as f: f.write(js)
print("Navigation and Cash calculations fixed.")

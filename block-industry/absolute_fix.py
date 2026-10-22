import re
with open('app.js', 'r') as f: js = f.read()

# ==========================================
# 1. ENSURE TILE CLICKS WORK
# ==========================================
# Find the exact tile function and replace it
old_tile = re.search(r'const tile = \(title, stock, type, size\) => `.*?`;', js, re.DOTALL).group(0)
new_tile = '''const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockDetailsPage('${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight: 700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;'''
js = js.replace(old_tile, new_tile)

# ==========================================
# 2. ENSURE ROUTING FUNCTION EXISTS
# ==========================================
if 'function openStockDetailsPage(type, size) {' not in js:
    # Add the helper function right before renderStockDetails
    js = js.replace('function renderStockDetails(main, type, size) {', 
        "function openStockDetailsPage(type, size) {\n    stockType = type;\n    stockSize = size;\n    nav('stock_details');\n}\n\nfunction renderStockDetails(main, type, size) {")

# ==========================================
# 3. REWRITE THE NAV FUNCTION COMPLETELY
# ==========================================
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

'''
    js = js[:start_nav] + new_nav + js[end_nav:]

# ==========================================
# 4. FIX CASH IN HAND MATH (Deduct Purchases)
# ==========================================
# Find the exact line calculating cashInHand in renderAnalytics
js = re.sub(r"const cashInHand = cashIn - allExpenses;", 
    "const totalPurchaseCash = purchases.reduce((sum, p) => sum + (p.amountPaid || 0), 0);\n    const cashInHand = cashIn - allExpenses - totalPurchaseCash;", 
    js)

with open('app.js', 'w') as f: f.write(js)
print("Forced tile clicks, routing, and cash math successfully.")

import re
with open('app.js', 'r') as f: js = f.read()

# ==========================================
# 1. FIX TILE CLICKS
# ==========================================
old_tile = '''    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="nav('stock_details', null, '${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight: 700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;'''

new_tile = '''    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockDetailsPage('${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight: 700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;'''
js = js.replace(old_tile, new_tile)

# Add the new routing function right before renderStockDetails
if 'function openStockDetailsPage(type, size) {' not in js:
    new_route = '''
function openStockDetailsPage(type, size) {
    stockType = type;
    stockSize = size;
    nav('stock_details');
}

function renderStockDetails(main, type, size) {'''
    js = js.replace('function renderStockDetails(main, type, size) {', new_route)

# ==========================================
# 2. FIX CASH IN HAND CALCULATION
# ==========================================
old_cash = '''    const cashIn = sales.reduce((sum, s) => sum + s.amountPaidAtSale, 0) + payments.reduce((sum, p) => sum + p.amount, 0);
    const cashInHand = cashIn - allExpenses;'''

new_cash = '''    const cashIn = sales.reduce((sum, s) => sum + s.amountPaidAtSale, 0) + payments.reduce((sum, p) => sum + p.amount, 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + (p.amountPaid || 0), 0); // Money spent on stock
    const cashInHand = cashIn - allExpenses - totalPurchaseCash;'''

# Check if it exists in renderAnalytics
if old_cash in js:
    js = js.replace(old_cash, new_cash)
else:
    # Fallback regex just in case formatting changed
    js = re.sub(r"const cashInHand = cashIn - allExpenses;", "const totalPurchaseCash = purchases.reduce((sum, p) => sum + (p.amountPaid || 0), 0);\n    const cashInHand = cashIn - allExpenses - totalPurchaseCash;", js)

with open('app.js', 'w') as f: f.write(js)
print("Tiles click fixed and Cash in Hand updated to deduct purchases.")

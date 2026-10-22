import re
with open('app.js', 'r') as f: js = f.read()

# 1. Ensure capital array is loaded
if "let capital = " not in js:
    js = js.replace("let expenses = JSON.parse(localStorage.getItem('asad:expenses')) || [];", "let expenses = JSON.parse(localStorage.getItem('asad:expenses')) || [];\nlet capital = JSON.parse(localStorage.getItem('asad:capital')) || [];")

# 2. Force replace the Cash in Hand tile in renderAnalytics
old_tile = r'<div class="stat"><div class="top"><span class="dot g">\$\{ico\(\'cash\'\)\}</span><h4>\$\{t\.cashInHand\}</h4></div><div class="val">\$\{formatNaira\(cashInHand\)\}</div></div>'
# Since regex on template literals is risky, let's target the exact string
old_tile_exact = '''<div class="stat"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand}</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>'''
new_tile_exact = '''<div class="stat" onclick="openAddCapitalModal()" style="cursor:pointer; border: 2px dashed var(--brand); position:relative;"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand} <span style="color:var(--brand); font-size:16px; font-weight:bold;">+ Add Cash</span></h4></div><div class="val">${formatNaira(cashInHand)}</div></div>'''

js = js.replace(old_tile_exact, new_tile_exact)

# 3. Update the Cash math to include capital
old_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash;'''

new_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const totalCapitalAdded = capital.reduce((sum, c) => sum + N(c.amount), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash + totalCapitalAdded;'''
js = js.replace(old_cash, new_cash)

# 4. Ensure the Modal functions exist
if 'function openAddCapitalModal()' not in js:
    capital_js = '''
function openAddCapitalModal() {
    document.getElementById('modal-body').innerHTML = `
        <h3>Add Cash to Business</h3>
        <p style="font-size:13px; color:var(--muted); margin-bottom:16px;">Use this to add money from outside (e.g. personal savings, bank loan) to balance your Cash in Hand.</p>
        <div class="form-group">
            <label>Amount (₦)</label>
            <input type="number" id="cap-amount" placeholder="0" min="1">
        </div>
        <div class="form-group">
            <label>Note / Source</label>
            <input type="text" id="cap-note" placeholder="e.g. Owner Capital, Bank Loan" value="Owner Capital">
        </div>
        <button class="btn" onclick="saveCapital()">Add Cash</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function saveCapital() {
    const amount = parseFloat(document.getElementById('cap-amount').value) || 0;
    if (amount <= 0) return showToast('Enter a valid amount', 'err');
    
    capital.push({
        id: Date.now().toString(),
        date: getTodayStr(),
        amount: amount,
        note: document.getElementById('cap-note').value || 'Owner Capital'
    });
    
    saveData('capital', capital);
    closeModal();
    nav('analytics');
    showToast('Cash added successfully', 'success');
}

'''
    js = js.replace('function toggleAlerts() {', capital_js + '\nfunction toggleAlerts() {')

with open('app.js', 'w') as f: f.write(js)
print("Capital feature forced and applied.")

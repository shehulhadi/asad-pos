import re
with open('app.js', 'r') as f: js = f.read()

# 1. Add capital array to state
js = js.replace("let expenses = JSON.parse(localStorage.getItem('asad:expenses')) || [];", "let expenses = JSON.parse(localStorage.getItem('asad:expenses')) || [];\nlet capital = JSON.parse(localStorage.getItem('asad:capital')) || [];")

# 2. Update Cash in Hand calculation in renderAnalytics
old_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash;'''

new_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const totalCapitalAdded = capital.reduce((sum, c) => sum + N(c.amount), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash + totalCapitalAdded;'''
js = js.replace(old_cash, new_cash)

# 3. Make the Cash in Hand tile clickable
old_tile = '''<div class="stat"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand}</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>'''
new_tile = '''<div class="stat" onclick="openAddCapitalModal()" style="cursor:pointer; position:relative;"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand} <span style="color:var(--brand); font-size:16px;">+</span></h4></div><div class="val">${formatNaira(cashInHand)}</div></div>'''
js = js.replace(old_tile, new_tile)

# 4. Add the Modal and Save Logic
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
if 'function openAddCapitalModal()' not in js:
    js = js.replace('function toggleAlerts() {', capital_js + '\nfunction toggleAlerts() {')

with open('app.js', 'w') as f: f.write(js)
print("Capital injection feature added.")

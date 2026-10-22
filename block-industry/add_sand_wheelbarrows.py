import re
with open('app.js', 'r') as f: js = f.read()

# 1. Update openPurchase to include Sand Trip Types
start_pur = js.find('function openPurchase() {')
end_pur = js.find('function savePurchase() {')
if start_pur != -1 and end_pur != -1:
    new_pur = '''function openPurchase() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.logPurchase}</h3>
        <div class="form-group"><label>${t.supplierName}</label><input type="text" id="pur-supplier" list="supplier-names" placeholder="e.g. Dangote"><datalist id="supplier-names"></datalist></div>
        <div class="form-group">
            <label>Material</label>
            <select id="pur-mat" onchange="toggleSandInput()">
                <option value="cement">${t.cement}</option>
                <option value="sand">${t.sand}</option>
                <option value="empty_bag">${t.empty_bag}</option>
            </select>
        </div>
        
        <div id="sand-trip-section" style="display:none; background:var(--bg); padding:12px; border-radius:8px; margin-bottom:14px;">
            <div class="form-group" style="margin-bottom:0;">
                <label>Trip Size</label>
                <select id="pur-sand-type">
                    <option value="150">Tangul (150 Wheelbarrows)</option>
                    <option value="60">Single (60 Wheelbarrows)</option>
                </select>
            </div>
        </div>

        <div class="row">
            <div class="form-group"><label id="qty-label">Qty</label><input type="number" id="pur-qty" value="" placeholder="0" oninput="calcPurchase()"></div>
            <div class="form-group"><label id="cost-label">Cost per Unit (₦)</label><input type="number" id="pur-unit-cost" value="" placeholder="0" oninput="calcPurchase()"></div>
        </div>
        
        <div id="sand-calc" class="calc-box" style="display:none; margin-bottom:14px;">
            <div class="line"><span>Total Wheelbarrows</span> <span id="pur-sand-total">0</span></div>
        </div>

        <div class="calc-box">
            <div class="line"><span>Total Cost</span> <span>₦<span id="pur-total-display">0</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="pur-balance-display">0</span></span></div>
        </div>
        <div class="form-group"><label>${t.paid}</label><input type="number" id="pur-paid" value="" placeholder="0" oninput="calcPurchase()"></div>
        <button class="btn" onclick="savePurchase()">Save</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    const uniqueSuppliers = [...new Set(purchases.map(p => p.supplierName).filter(n => n && n !== 'Unknown'))];
    document.getElementById('supplier-names').innerHTML = uniqueSuppliers.map(name => `<option value="${name}"></option>`).join('');
    document.getElementById('modal').classList.add('active');
    calcPurchase();
}

function toggleSandInput() {
    const mat = document.getElementById('pur-mat').value;
    if (mat === 'sand') {
        document.getElementById('sand-trip-section').style.display = 'block';
        document.getElementById('sand-calc').style.display = 'flex';
        document.getElementById('qty-label').innerText = 'Number of Trips';
        document.getElementById('cost-label').innerText = 'Cost per Trip (₦)';
    } else {
        document.getElementById('sand-trip-section').style.display = 'none';
        document.getElementById('sand-calc').style.display = 'none';
        document.getElementById('qty-label').innerText = 'Qty';
        document.getElementById('cost-label').innerText = 'Cost per Unit (₦)';
    }
    calcPurchase();
}

function calcPurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    
    const mat = document.getElementById('pur-mat').value;
    let total = qty * unitCost;
    let balance = total - paid;
    
    if (mat === 'sand') {
        const multiplier = parseInt(document.getElementById('pur-sand-type').value);
        document.getElementById('pur-sand-total').innerText = (qty * multiplier).toLocaleString() + ' wheelbarrows';
    }
    
    document.getElementById('pur-total-display').textContent = total.toLocaleString();
    document.getElementById('pur-balance-display').textContent = balance.toLocaleString();
}

'''
    js = js[:start_pur] + new_pur + js[end_pur:]

# 2. Update savePurchase to handle sand multiplication
start_save = js.find('function savePurchase() {')
end_save = js.find('function openAdjustStock() {')
if start_save != -1 and end_save != -1:
    new_save = '''function savePurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const cost = qty * unitCost;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    const mat = document.getElementById('pur-mat').value;
    
    if (qty <= 0) return showToast('Enter valid quantity', 'err');
    
    let finalQty = qty;
    if (mat === 'sand') {
        const multiplier = parseInt(document.getElementById('pur-sand-type').value);
        finalQty = qty * multiplier;
    }
    
    purchases.push({ 
        id: Date.now().toString(), 
        date: getTodayStr(), 
        supplierName: document.getElementById('pur-supplier').value || 'Unknown', 
        material: mat, 
        qty: finalQty, 
        cost: cost, 
        amountPaid: paid 
    });
    
    saveData('purchases', purchases); 
    closeModal();
    if (currentView === 'debts') { currentDebtTab = 'supplier'; nav('debts'); } 
    else { nav('dashboard'); }
    showToast('Purchase logged', 'success');
}

'''
    js = js[:start_save] + new_save + js[end_save:]

# 3. Update Production Form label for Sand
js = js.replace('<label>${t.sandQty}</label>', '<label>Sand Qty (Wheelbarrows)</label>')

# 4. Update Stock Dashboard Display for Sand
js = js.replace("${tile('Sand', sandStock, 'sand', '')}", "${tile('Sand (Wheelbarrows)', sandStock, 'sand', '')}")

# 5. Ensure Cash in Hand math is strictly Sales + Capital - Expenses - Purchases Paid
old_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const totalCapitalAdded = capital.reduce((sum, c) => sum + N(c.amount), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash + totalCapitalAdded;'''
new_cash = '''    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const totalCapitalAdded = capital.reduce((sum, c) => sum + N(c.amount), 0);
    // Strict math: Cash In - Cash Out + Injected Capital
    const cashInHand = cashFromSales + totalCapitalAdded - allExpenses - totalPurchaseCash;'''
js = js.replace(old_cash, new_cash)

with open('app.js', 'w') as f: f.write(js)
print("Sand wheelbarrow logic and cash math applied.")

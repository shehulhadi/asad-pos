import re
with open('app.js', 'r') as f: js = f.read()

# 1. Update openPurchase
start_purchase = js.find('function openPurchase() {')
end_purchase = js.find('function savePurchase() {')
if start_purchase != -1 and end_purchase != -1:
    new_purchase = '''function openPurchase() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.logPurchase}</h3>
        <div class="form-group"><label>${t.supplierName}</label><input type="text" id="pur-supplier" list="supplier-names" placeholder="e.g. Dangote"><datalist id="supplier-names"></datalist></div>
        <div class="form-group"><label>Material</label><select id="pur-mat"><option value="cement">${t.cement}</option><option value="sand">${t.sand}</option></select></div>
        <div class="row">
            <div class="form-group"><label>Qty</label><input type="number" id="pur-qty" value="" placeholder="0" oninput="calcPurchase()"></div>
            <div class="form-group"><label>Cost per Unit (₦)</label><input type="number" id="pur-unit-cost" value="" placeholder="0" oninput="calcPurchase()"></div>
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

function calcPurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    
    const total = qty * unitCost;
    const balance = total - paid;
    
    document.getElementById('pur-total-display').textContent = total.toLocaleString();
    document.getElementById('pur-balance-display').textContent = balance.toLocaleString();
}

'''
    js = js[:start_purchase] + new_purchase + js[end_purchase:]

# 2. Update savePurchase
start_save = js.find('function savePurchase() {')
end_save = js.find('function openAdjustStock() {')
if start_save != -1 and end_save != -1:
    new_save = '''function savePurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const cost = qty * unitCost;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    
    if (qty <= 0) return showToast('Enter valid quantity', 'err');
    
    purchases.push({ id: Date.now().toString(), date: getTodayStr(), supplierName: document.getElementById('pur-supplier').value || 'Unknown', material: document.getElementById('pur-mat').value, qty: qty, cost: cost, amountPaid: paid });
    saveData('purchases', purchases); closeModal();
    if (currentView === 'debts') { currentDebtTab = 'supplier'; nav('debts'); } else { nav('dashboard'); }
    showToast('Purchase logged', 'success');
}

'''
    js = js[:start_save] + new_save + js[end_save:]

# 3. Update editPurchase
start_edit = js.find('function editPurchase(id) {')
end_edit = js.find('function saveEditedPurchase(id) {')
if start_edit != -1 and end_edit != -1:
    new_edit = '''function editPurchase(id) {
    const p = purchases.find(x => x.id === id);
    const unitCost = p.qty > 0 ? (p.cost / p.qty) : 0;
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Purchase</h3>
        <div class="form-group"><label>Supplier Name</label><input type="text" id="edit-p-supplier" value="${p.supplierName}"></div>
        <div class="form-group"><label>Material</label><select id="edit-p-mat"><option value="cement" ${p.material==='cement'?'selected':''}>Cement</option><option value="sand" ${p.material==='sand'?'selected':''}>Sand</option></select></div>
        <div class="row">
            <div class="form-group"><label>Quantity</label><input type="number" id="edit-p-qty" value="${p.qty || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
            <div class="form-group"><label>Cost per Unit</label><input type="number" id="edit-p-unit-cost" value="${unitCost || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
        </div>
        <div class="calc-box">
            <div class="line"><span>Total Cost</span> <span>₦<span id="edit-p-total-display">${p.cost.toLocaleString()}</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="edit-p-balance-display">${(p.cost - (p.amountPaid || 0)).toLocaleString()}</span></span></div>
        </div>
        <div class="form-group"><label>Amount Paid</label><input type="number" id="edit-p-paid" value="${p.amountPaid || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
        <div class="row"><button class="btn btn-outline" onclick="openPurchaseDetails('${p.id}')">Back</button><button class="btn" onclick="saveEditedPurchase('${p.id}')">Save Changes</button></div>
    `;
}

function calcEditPurchase() {
    const qty = parseFloat(document.getElementById('edit-p-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('edit-p-unit-cost').value) || 0;
    const paid = parseFloat(document.getElementById('edit-p-paid').value) || 0;
    
    const total = qty * unitCost;
    const balance = total - paid;
    
    document.getElementById('edit-p-total-display').textContent = total.toLocaleString();
    document.getElementById('edit-p-balance-display').textContent = balance.toLocaleString();
}

'''
    js = js[:start_edit] + new_edit + js[end_edit:]

# 4. Update saveEditedPurchase
start_save_edit = js.find('function saveEditedPurchase(id) {')
end_save_edit = js.find('function openStockCheck(size, expected) {')
if start_save_edit != -1 and end_save_edit != -1:
    new_save_edit = '''function saveEditedPurchase(id) {
    const p = purchases.find(x => x.id === id);
    p.supplierName = document.getElementById('edit-p-supplier').value || 'Unknown';
    p.material = document.getElementById('edit-p-mat').value;
    p.qty = parseFloat(document.getElementById('edit-p-qty').value) || 0;
    p.cost = p.qty * (parseFloat(document.getElementById('edit-p-unit-cost').value) || 0);
    p.amountPaid = parseFloat(document.getElementById('edit-p-paid').value) || 0;
    saveData('purchases', purchases); closeModal(); nav('dashboard'); showToast('Purchase updated', 'success');
}

'''
    js = js[:start_save_edit] + new_save_edit + js[end_save_edit:]

with open('app.js', 'w') as f: f.write(js)

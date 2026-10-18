import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add stockAdjustments to state
html = html.replace(
    "let purchases = JSON.parse(localStorage.getItem('asad:purchases')) || [];",
    "let purchases = JSON.parse(localStorage.getItem('asad:purchases')) || [];\n    let stockAdjustments = JSON.parse(localStorage.getItem('asad:stockAdjustments')) || [];"
)

# 2. Update stock calculations in renderInventory
old_calc = '''        const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
        const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
        const cementStock = cementPurchased - cementUsed;

        const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
        const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
        const sandStock = sandPurchased - sandUsed;

        const fuelPurchased = purchases.filter(p=>p.material==='fuel').reduce((s,p)=>s+p.qty,0);
        const fuelUsed = batches.reduce((s,b)=>s+(b.fuelQty||0),0);
        const fuelStock = fuelPurchased - fuelUsed;'''

new_calc = '''        const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
        const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
        const cementAdj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
        const cementStock = cementPurchased - cementUsed + cementAdj;

        const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
        const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
        const sandAdj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
        const sandStock = sandPurchased - sandUsed + sandAdj;

        const fuelPurchased = purchases.filter(p=>p.material==='fuel').reduce((s,p)=>s+p.qty,0);
        const fuelUsed = batches.reduce((s,b)=>s+(b.fuelQty||0),0);
        const fuelAdj = stockAdjustments.filter(a=>a.material==='fuel').reduce((s,a)=>s+a.qty,0);
        const fuelStock = fuelPurchased - fuelUsed + fuelAdj;'''
html = html.replace(old_calc, new_calc)

# 3. Update the Inventory HTML to show Recent Purchases and Adjust button
old_raw_html = '''                <button class="btn btn-dark" style="margin-top:0;" onclick="openPurchase()">+ ${t.logPurchase}</button>
            </div>

            <div class="section-title">${ico('production')} ${t.finishedBlocks}</div>'''

new_raw_html = '''                <div class="row">
                    <button class="btn btn-dark" style="margin-top:0;" onclick="openPurchase()">+ ${t.logPurchase}</button>
                    <button class="btn btn-outline" style="margin-top:0;" onclick="openAdjustStock()">Adjust Stock</button>
                </div>
                <div class="section-title" style="margin-top:16px; margin-bottom:8px;">Recent Purchases</div>
                ${purchases.length > 0 ? [...purchases].reverse().slice(0,5).map(p => `
                    <div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')">
                        <div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div>
                        <div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div>
                    </div>
                `).join('') : '<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases logged yet.</p>'}
            </div>

            <div class="section-title">${ico('production')} ${t.finishedBlocks}</div>'''
html = html.replace(old_raw_html, new_raw_html)

# 4. Inject the new functions
new_functions = '''
    function openAdjustStock() {
        document.getElementById('modal-body').innerHTML = `
            <h3>Adjust Raw Material</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:16px;">Use negative numbers for spoilage/loss, positive for extra stock found.</p>
            <div class="form-group">
                <label>Material</label>
                <select id="adj-mat"><option value="cement">Cement</option><option value="sand">Sand</option><option value="fuel">Fuel</option></select>
            </div>
            <div class="form-group">
                <label>Adjustment Qty</label>
                <input type="number" id="adj-qty" value="0" placeholder="e.g. -5">
            </div>
            <div class="form-group">
                <label>Reason</label>
                <input type="text" id="adj-reason" placeholder="e.g. Spoiled, extra found">
            </div>
            <button class="btn" onclick="saveAdjustStock()">Save Adjustment</button>
            <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function saveAdjustStock() {
        const qty = parseFloat(document.getElementById('adj-qty').value) || 0;
        if (qty === 0) return showToast('Enter a non-zero value', 'err');
        stockAdjustments.push({
            id: Date.now().toString(),
            date: new Date().toISOString().split('T')[0],
            material: document.getElementById('adj-mat').value,
            qty: qty,
            reason: document.getElementById('adj-reason').value || 'Manual adjustment'
        });
        saveData('stockAdjustments', stockAdjustments);
        closeModal();
        nav('inventory');
        showToast('Stock adjusted', 'success');
    }

    function openPurchaseDetails(id) {
        const p = purchases.find(x => x.id === id);
        if (!p) return;
        document.getElementById('modal-body').innerHTML = `
            <h3>Purchase Details</h3>
            <div class="kv"><span>Supplier</span><strong>${p.supplierName}</strong></div>
            <div class="kv"><span>Material</span><strong>${p.material.toUpperCase()}</strong></div>
            <div class="kv"><span>Quantity</span><strong>${p.qty}</strong></div>
            <div class="kv"><span>Total Cost</span><strong>₦${p.cost.toLocaleString()}</strong></div>
            <div class="kv"><span>Amount Paid</span><strong>₦${(p.amountPaid || 0).toLocaleString()}</strong></div>
            <div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editPurchase('${p.id}')">Edit Purchase</button>
            </div>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function editPurchase(id) {
        const p = purchases.find(x => x.id === id);
        document.getElementById('modal-body').innerHTML = `
            <h3>Edit Purchase</h3>
            <div class="form-group"><label>Supplier Name</label><input type="text" id="edit-p-supplier" value="${p.supplierName}"></div>
            <div class="form-group"><label>Material</label><select id="edit-p-mat"><option value="cement" ${p.material==='cement'?'selected':''}>Cement</option><option value="sand" ${p.material==='sand'?'selected':''}>Sand</option><option value="fuel" ${p.material==='fuel'?'selected':''}>Fuel</option></select></div>
            <div class="row">
                <div class="form-group"><label>Quantity</label><input type="number" id="edit-p-qty" value="${p.qty}"></div>
                <div class="form-group"><label>Total Cost</label><input type="number" id="edit-p-cost" value="${p.cost}"></div>
            </div>
            <div class="form-group"><label>Amount Paid</label><input type="number" id="edit-p-paid" value="${p.amountPaid || 0}"></div>
            <div class="row">
                <button class="btn btn-outline" onclick="openPurchaseDetails('${p.id}')">Back</button>
                <button class="btn" onclick="saveEditedPurchase('${p.id}')">Save Changes</button>
            </div>
        `;
    }

    function saveEditedPurchase(id) {
        const p = purchases.find(x => x.id === id);
        p.supplierName = document.getElementById('edit-p-supplier').value || 'Unknown';
        p.material = document.getElementById('edit-p-mat').value;
        p.qty = parseFloat(document.getElementById('edit-p-qty').value) || 0;
        p.cost = parseFloat(document.getElementById('edit-p-cost').value) || 0;
        p.amountPaid = parseFloat(document.getElementById('edit-p-paid').value) || 0;
        
        saveData('purchases', purchases);
        closeModal();
        nav('inventory');
        showToast('Purchase updated successfully', 'success');
    }

    // --- Debts Module ---
'''
html = html.replace('// --- Debts Module ---', new_functions)

with open('index.html', 'w') as f: f.write(html)

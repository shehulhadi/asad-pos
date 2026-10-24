import re
with open('app.js', 'r') as f: js = f.read()

# 1. Update openDeviceDetails to add Edit/Delete buttons
start_details = js.find('function openDeviceDetails(id) {')
end_details = js.find('// --- SALES ---')

if start_details != -1 and end_details != -1:
    new_details = '''function openDeviceDetails(id) {
    const p = inventory.find(x => x.id === id);
    if (!p) return;
    
    let saleInfo = '';
    if (p.status === 'Sold') {
        const sale = sales.find(s => s.deviceId === p.id);
        if (sale) {
            saleInfo = `
                <div class="eyebrow" style="color:var(--brand);">Sale Info</div>
                <div class="kv"><span>Sold To</span><strong>${sale.customerName}</strong></div>
                <div class="kv"><span>Customer Phone</span><strong>${sale.customerPhone || 'N/A'}</strong></div>
                <div class="kv"><span>Sale Price</span><strong>${formatNaira(sale.totalAmount)}</strong></div>
                <div class="kv"><span>Date Sold</span><strong>${sale.date}</strong></div>
            `;
        }
    }

    document.getElementById('modal-body').innerHTML = `
        <h3>${p.brand} ${p.model}</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <span class="tag ${p.status === 'Available' ? 'green' : ''}" style="font-size:14px; padding:6px 12px; background:${p.status === 'Available' ? 'var(--brand-soft)' : '#eee'}; color:${p.status === 'Available' ? 'var(--brand-dark)' : '#555'};">
                ${p.status.toUpperCase()}
            </span>
        </div>
        
        <div class="eyebrow">Device Specs</div>
        <div class="kv"><span>Storage</span><strong>${p.storage}</strong></div>
        <div class="kv"><span>Condition</span><strong>${p.condition}</strong></div>
        <div class="kv"><span>IMEI / Serial</span><strong>${p.imei || 'N/A'}</strong></div>
        
        <div class="eyebrow">Seller Info (Intake)</div>
        <div class="kv"><span>Name</span><strong>${p.sellerName || 'N/A'}</strong></div>
        <div class="kv"><span>Phone</span><strong>${p.sellerPhone || 'N/A'}</strong></div>
        <div class="kv"><span>Address</span><strong>${p.sellerAddress || 'N/A'}</strong></div>

        ${saleInfo}
        
        <div class="eyebrow">Financials</div>
        <div class="kv"><span>Cost Price</span><strong>${formatNaira(p.costPrice)}</strong></div>
        <div class="kv"><span>Target Selling Price</span><strong>${formatNaira(p.sellingPrice)}</strong></div>
        
        <div class="row" style="margin-top:20px;">
            <button class="btn outline" onclick="closeModal()">Close</button>
            <button class="btn" onclick="editDevice('${p.id}')">Edit Device</button>
        </div>
        ${p.status === 'Available' ? `<button class="btn btn-danger" style="margin-top:10px;" onclick="deleteDevice('${p.id}')">Delete Device</button>` : ''}
    `;
    document.getElementById('modal').classList.add('active');
}

function editDevice(id) {
    const p = inventory.find(x => x.id === id);
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Device</h3>
        <div class="row">
            <div class="form-group"><label>Brand</label><input type="text" id="edit-p-brand" value="${p.brand}"></div>
            <div class="form-group"><label>Model</label><input type="text" id="edit-p-model" value="${p.model}"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Storage</label><input type="text" id="edit-p-storage" value="${p.storage}"></div>
            <div class="form-group"><label>Condition</label><select id="edit-p-condition">
                <option value="New" ${p.condition==='New'?'selected':''}>New</option>
                <option value="Used - Grade A" ${p.condition==='Used - Grade A'?'selected':''}>Used - Grade A</option>
                <option value="Used - Grade B" ${p.condition==='Used - Grade B'?'selected':''}>Used - Grade B</option>
                <option value="Needs Repair" ${p.condition==='Needs Repair'?'selected':''}>Needs Repair</option>
            </select></div>
        </div>
        <div class="form-group"><label>IMEI</label><input type="text" id="edit-p-imei" value="${p.imei || ''}"></div>
        
        <div class="eyebrow">Seller Info</div>
        <div class="form-group"><label>Seller Name</label><input type="text" id="edit-p-seller-name" value="${p.sellerName || ''}"></div>
        <div class="row">
            <div class="form-group"><label>Seller Phone</label><input type="tel" id="edit-p-seller-phone" value="${p.sellerPhone || ''}"></div>
            <div class="form-group"><label>Seller Address</label><input type="text" id="edit-p-seller-address" value="${p.sellerAddress || ''}"></div>
        </div>

        <div class="row">
            <div class="form-group"><label>Cost Price (₦)</label><input type="number" id="edit-p-cost" value="${p.costPrice}"></div>
            <div class="form-group"><label>Selling Price (₦)</label><input type="number" id="edit-p-sell" value="${p.sellingPrice}"></div>
        </div>
        <div class="row">
            <button class="btn outline" onclick="openDeviceDetails('${p.id}')">Back</button>
            <button class="btn" onclick="saveEditedDevice('${p.id}')">Save Changes</button>
        </div>
    `;
}

function saveEditedDevice(id) {
    const p = inventory.find(x => x.id === id);
    p.brand = document.getElementById('edit-p-brand').value;
    p.model = document.getElementById('edit-p-model').value;
    p.storage = document.getElementById('edit-p-storage').value;
    p.condition = document.getElementById('edit-p-condition').value;
    p.imei = document.getElementById('edit-p-imei').value;
    p.sellerName = document.getElementById('edit-p-seller-name').value;
    p.sellerPhone = document.getElementById('edit-p-seller-phone').value;
    p.sellerAddress = document.getElementById('edit-p-seller-address').value;
    p.costPrice = parseFloat(document.getElementById('edit-p-cost').value) || 0;
    p.sellingPrice = parseFloat(document.getElementById('edit-p-sell').value) || 0;
    
    saveData('inventory', inventory);
    closeModal();
    nav('inventory');
}

function deleteDevice(id) {
    if (confirm("Are you sure you want to delete this device? This cannot be undone.")) {
        inventory = inventory.filter(p => p.id !== id);
        saveData('inventory', inventory);
        closeModal();
        nav('inventory');
    }
}

'''
    js = js[:start_details] + new_details + js[end_details:]

# 2. Update renderSales history items to be clickable
old_history = '''    recentSales.forEach(s => {
        historyHtml += `
            <div class="list-item">
                <div class="list-header">
                    <span>${s.customerName}</span>
                    <strong style="color:var(--brand);">${formatNaira(s.totalAmount)}</strong>
                </div>
                <div class="list-sub">${s.date} · ${s.phoneName}</div>
                ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
            </div>
        `;
    });'''
new_history = '''    recentSales.forEach(s => {
        historyHtml += `
            <div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')">
                <div class="list-header">
                    <span>${s.customerName}</span>
                    <strong style="color:var(--brand);">${formatNaira(s.totalAmount)}</strong>
                </div>
                <div class="list-sub">${s.date} · ${s.phoneName}</div>
                ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
            </div>
        `;
    });'''
js = js.replace(old_history, new_history)

# 3. Add openSaleDetails, editSale, and deleteSale functions
sale_details_js = '''
function openSaleDetails(id) {
    const s = sales.find(x => x.id === id);
    if (!s) return;
    
    document.getElementById('modal-body').innerHTML = `
        <h3>Sale Receipt</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted);">${s.date}</p>
            <p style="font-size:28px; font-weight:800; color:var(--brand); margin-top:8px;">${formatNaira(s.totalAmount)}</p>
            ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Owing ${formatNaira(s.balanceOwing)}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
        </div>
        <div class="kv"><span>Customer</span><strong>${s.customerName}</strong></div>
        <div class="kv"><span>Phone</span><strong>${s.customerPhone || 'N/A'}</strong></div>
        <div class="kv"><span>Device</span><strong>${s.phoneName}</strong></div>
        <div class="kv"><span>Amount Paid</span><strong>${formatNaira(s.amountPaid)}</strong></div>
        
        <div class="actions" style="margin-top:20px;">
            <a href="https://wa.me/${(s.customerPhone||'').replace(/^0/, '234')}?text=${encodeURIComponent(`*Receipt - Elbabs Communications*\\n\\nCustomer: ${s.customerName}\\nDevice: ${s.phoneName}\\n\\n*Total: ${formatNaira(s.totalAmount)}*\\nPaid: ${formatNaira(s.amountPaid)}\\n*Balance: ${formatNaira(s.balanceOwing)}*`)}" target="_blank"><button class="wa">WhatsApp</button></a>
        </div>
        <div class="row" style="margin-top:12px;">
            <button class="btn outline" onclick="closeModal()">Close</button>
            <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
        </div>
        <button class="btn btn-danger" style="margin-top:10px;" onclick="deleteSale('${s.id}')">Delete Sale</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function editSale(id) {
    const s = sales.find(x => x.id === id);
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Sale</h3>
        <div class="form-group"><label>Customer</label><input type="text" id="edit-s-customer" value="${s.customerName}"></div>
        <div class="form-group"><label>Phone</label><input type="tel" id="edit-s-phone" value="${s.customerPhone || ''}"></div>
        <div class="row">
            <div class="form-group"><label>Selling Price (₦)</label><input type="number" id="edit-s-price" value="${s.totalAmount}"></div>
            <div class="form-group"><label>Amount Paid (₦)</label><input type="number" id="edit-s-paid" value="${s.amountPaid}"></div>
        </div>
        <div class="row">
            <button class="btn outline" onclick="openSaleDetails('${s.id}')">Back</button>
            <button class="btn" onclick="saveEditedSale('${s.id}')">Save Changes</button>
        </div>
    `;
}

function saveEditedSale(id) {
    const s = sales.find(x => x.id === id);
    s.customerName = document.getElementById('edit-s-customer').value;
    s.customerPhone = document.getElementById('edit-s-phone').value;
    s.totalAmount = parseFloat(document.getElementById('edit-s-price').value) || 0;
    s.amountPaid = parseFloat(document.getElementById('edit-s-paid').value) || 0;
    s.balanceOwing = s.totalAmount - s.amountPaid;
    
    saveData('sales', sales);
    closeModal();
    nav('sales');
}

function deleteSale(id) {
    if (confirm("Are you sure? Deleting this sale will return the device to Available stock.")) {
        const sale = sales.find(s => s.id === id);
        if (sale) {
            const device = inventory.find(p => p.id === sale.deviceId);
            if (device) device.status = 'Available';
            saveData('inventory', inventory);
        }
        sales = sales.filter(s => s.id !== id);
        saveData('sales', sales);
        closeModal();
        nav('sales');
    }
}

'''
if 'function openSaleDetails(id)' not in js:
    js = js.replace('function startTradeIn() {', sale_details_js + '\nfunction startTradeIn() {')

with open('app.js', 'w') as f: f.write(js)
print("Edit and Delete features successfully added to Elbabs.")

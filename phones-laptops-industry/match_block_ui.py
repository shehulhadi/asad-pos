import re
with open('app.js', 'r') as f: js = f.read()

# 1. Rewrite renderInventory to use a Modal
start_inv = js.find('function renderInventory(main) {')
end_inv = js.find('function openDeviceDetails(id) {')

if start_inv != -1 and end_inv != -1:
    new_inv = '''function renderInventory(main) {
    let listHtml = '';
    const available = inventory.filter(p => p.status === 'Available').reverse();
    
    available.forEach(p => {
        listHtml += `
            <div class="list-item" style="cursor:pointer;" onclick="openDeviceDetails('${p.id}')">
                <div class="list-header">
                    <span>${p.brand} ${p.model}</span>
                    <strong style="color:var(--brand);">${formatNaira(p.sellingPrice)}</strong>
                </div>
                <div class="list-sub">${p.storage} · ${p.condition} · IMEI: ${p.imei || 'N/A'}</div>
                <div class="list-sub" style="margin-top:4px;">Seller: ${p.sellerName || 'Unknown'}</div>
                <div style="margin-top:6px;"><span class="tag green">In Stock</span></div>
            </div>
        `;
    });

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="openAddDeviceModal()" style="background:var(--brand); color:#fff; border:none; padding:14px; font-size:15px; border-radius:8px; font-weight:700; width:100%; box-shadow:0 4px 12px rgba(37,99,235,0.3);">+ Add New Device / Trade-In</button>
        </div>

        <h3 style="margin: 0 0 10px; font-size: 16px;">Available Inventory (${available.length})</h3>
        ${listHtml || '<p style="text-align:center; color:var(--muted);">No devices in stock yet.</p>'}
    `;
}

function openAddDeviceModal() {
    document.getElementById('modal-body').innerHTML = `
        <h3>Add New Device / Trade-In</h3>
        <div class="eyebrow" style="margin-top:0;">Device Info</div>
        <div class="row">
            <div class="form-group"><label>Brand</label><input type="text" id="p-brand" placeholder="e.g. Apple"></div>
            <div class="form-group"><label>Model</label><input type="text" id="p-model" placeholder="e.g. iPhone 13"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Storage</label><input type="text" id="p-storage" placeholder="128GB"></div>
            <div class="form-group"><label>Condition</label><select id="p-condition">
                <option value="New">New</option>
                <option value="Used - Grade A">Used - Grade A</option>
                <option value="Used - Grade B">Used - Grade B</option>
                <option value="Needs Repair">Needs Repair</option>
            </select></div>
        </div>
        <div class="form-group"><label>IMEI / Serial Number</label><input type="text" id="p-imei" placeholder="Enter IMEI"></div>
        
        <div class="eyebrow">Seller Info (Where did you buy it?)</div>
        <div class="form-group"><label>Seller Name</label><input type="text" id="p-seller-name" placeholder="Name"></div>
        <div class="row">
            <div class="form-group"><label>Seller Phone</label><input type="tel" id="p-seller-phone" placeholder="Phone"></div>
            <div class="form-group"><label>Seller Address</label><input type="text" id="p-seller-address" placeholder="Address"></div>
        </div>

        <div class="eyebrow">Financials</div>
        <div class="row">
            <div class="form-group"><label>Cost Price (₦)</label><input type="number" id="p-cost" placeholder="0"></div>
            <div class="form-group"><label>Selling Price (₦)</label><input type="number" id="p-sell" placeholder="0"></div>
        </div>
        <button class="btn" onclick="savePhone()">Add to Inventory</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start_inv] + new_inv + js[end_inv:]

# 2. Update savePhone to close modal
js = js.replace("saveData('inventory', inventory);\n    nav('inventory');", "saveData('inventory', inventory);\n    closeModal();\n    nav('inventory');")

# 3. Rewrite renderSales to use a Modal
start_sales = js.find('function renderSales(main) {')
end_sales = js.find('function startTradeIn() {')

if start_sales != -1 and end_sales != -1:
    new_sales = '''function renderSales(main) {
    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 15);
    
    recentSales.forEach(s => {
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
    });

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="openSaleModal()" style="background:var(--brand); color:#fff; border:none; padding:14px; font-size:15px; border-radius:8px; font-weight:700; width:100%; box-shadow:0 4px 12px rgba(37,99,235,0.3);">+ New Sale</button>
        </div>

        <h3 style="margin: 0 0 10px; font-size: 16px;">Recent Sales</h3>
        ${historyHtml || '<p style="text-align:center; color:var(--muted);">No sales recorded yet.</p>'}
    `;
}

function openSaleModal() {
    const availablePhones = inventory.filter(p => p.status === 'Available');
    
    let optionsHtml = '<option value="">-- Select a device --</option>';
    availablePhones.forEach(p => {
        optionsHtml += `<option value="${p.id}" data-price="${p.sellingPrice}">${p.brand} ${p.model} (${p.storage}) - ${formatNaira(p.sellingPrice)}</option>`;
    });

    document.getElementById('modal-body').innerHTML = `
        <h3>New Sale</h3>
        <div class="row">
            <div class="form-group" style="flex:2;">
                <label>Select Device</label>
                <select id="s-device" onchange="updateSalePrice()">
                    ${optionsHtml}
                </select>
            </div>
            <div class="form-group" style="flex:1; display:flex; align-items:flex-end;">
                <button class="btn" style="margin:0; padding:12px; font-size:12px; background:var(--accent); color:#fff; border:none; border-radius:8px;" onclick="startTradeIn()">🔄 Trade-In</button>
            </div>
        </div>
        
        <div class="form-group"><label>Customer Name</label><input type="text" id="s-customer" placeholder="Name"></div>
        <div class="form-group"><label>Customer Phone</label><input type="tel" id="s-phone" placeholder="Phone"></div>
        
        <div class="row">
            <div class="form-group"><label>Selling Price (₦)</label><input type="number" id="s-price" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Amount Paid (₦)</label><input type="number" id="s-paid" value="" placeholder="0" oninput="calcSale()"></div>
        </div>

        <div class="calc-box">
            <div class="line"><span>Balance Owing</span> <span>₦<span id="s-balance-display">0</span></span></div>
        </div>

        <button class="btn" onclick="saveSale()">Complete Sale</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start_sales] + new_sales + js[end_sales:]

# 4. Fix startTradeIn to work from the modal
old_tradein = '''function startTradeIn() {
    const custName = document.getElementById('s-customer').value;
    const custPhone = document.getElementById('s-phone').value;
    
    nav('inventory');
    
    setTimeout(() => {
        if(document.getElementById('p-seller-name')) {
            document.getElementById('p-seller-name').value = custName;
            document.getElementById('p-seller-phone').value = custPhone;
            window.scrollTo(0, document.body.scrollHeight);
            alert('Enter the Trade-In device details below. Customer info has been pre-filled as the Seller.');
        }
    }, 100);
}'''
new_tradein = '''function startTradeIn() {
    const custName = document.getElementById('s-customer').value;
    const custPhone = document.getElementById('s-phone').value;
    
    closeModal();
    nav('inventory');
    
    setTimeout(() => {
        openAddDeviceModal();
        setTimeout(() => {
            if(document.getElementById('p-seller-name')) {
                document.getElementById('p-seller-name').value = custName;
                document.getElementById('p-seller-phone').value = custPhone;
                alert('Enter the Trade-In device details below. Customer info has been pre-filled as the Seller.');
            }
        }, 100);
    }, 100);
}'''
js = js.replace(old_tradein, new_tradein)

# 5. Ensure saveSale closes the modal and updates nav
js = js.replace("sales.push(sale);\n    saveData('sales', sales);", "sales.push(sale);\n    saveData('sales', sales);")

with open('app.js', 'w') as f: f.write(js)
print("UI matched to Block app successfully.")

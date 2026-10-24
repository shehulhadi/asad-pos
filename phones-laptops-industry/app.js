let settings = JSON.parse(localStorage.getItem('elbabs:settings')) || { pin: '1234' };
let inventory = JSON.parse(localStorage.getItem('elbabs:inventory')) || [];
let sales = JSON.parse(localStorage.getItem('elbabs:sales')) || [];
let expenses = JSON.parse(localStorage.getItem('elbabs:expenses')) || [];
let capital = JSON.parse(localStorage.getItem('elbabs:capital')) || [];
let currentView = 'inventory';

function N(val) { return Number(val) || 0; }
function saveData(key, data) { 
    try {
        localStorage.setItem('elbabs:' + key, JSON.stringify(data)); 
    } catch (e) {
        showToast('Storage Error: Could not save data. Device storage may be full.', 'err');
        console.error('saveData failed', e);
    }
}
function formatNaira(num) { return '₦' + Number(num).toLocaleString(); }
function closeModal() { document.getElementById('modal').classList.remove('active'); }

function forceUpdate() {
    showDialog("Update App?", "This will download the latest app version. Your data will not be deleted.", () => {
        caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k)))).then(() => {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.getRegistrations().then(regs => {
                    for(let r of regs) r.unregister();
                    window.location.reload(true);
                });
            } else {
                window.location.reload(true);
            }
        });
    });
}


function showToast(msg, type = 'default') {
    const container = document.getElementById('toast-container');
    if(!container) return alert(msg);
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    let icon = type === 'success' ? '<svg class="ic" style="width:18px;height:18px;stroke:#fff;" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>' : (type === 'err' ? '<svg class="ic" style="width:18px;height:18px;stroke:#fff;" viewBox="0 0 24 24"><path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/></svg>' : '');
    toast.innerHTML = `${icon} <span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

function showDialog(title, msg, onConfirm) {
    const overlay = document.getElementById('dialog-overlay');
    if(!overlay) {
        if(confirm(title + '\n\n' + msg)) onConfirm();
        return;
    }
    document.getElementById('dialog-title').textContent = title;
    document.getElementById('dialog-msg').textContent = msg;
    const confirmBtn = document.getElementById('dialog-confirm-btn');
    const newBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
    newBtn.onclick = () => {
        closeDialog();
        if (onConfirm) onConfirm();
    };
    overlay.classList.add('active');
}

function closeDialog() {
    const overlay = document.getElementById('dialog-overlay');
    if(overlay) overlay.classList.remove('active');
}

function login() {
    const pin = document.getElementById('pin-input').value;
    const err = document.getElementById('login-error');
    if (pin === settings.pin) {
        sessionStorage.setItem('elbabs:auth', 'true');
        document.getElementById('login-view').classList.remove('active');
        document.getElementById('app-view').classList.add('active');
        nav('inventory');
    } else {
        err.style.display = 'block';
    }
}

function logout() {
    sessionStorage.removeItem('elbabs:auth');
    document.getElementById('app-view').classList.remove('active');
    document.getElementById('login-view').classList.add('active');
    document.getElementById('pin-input').value = '';
}

function nav(view, btn = null) {
    currentView = view;
    if (btn) {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }
    const main = document.getElementById('main-content');
    main.innerHTML = '';

    if (view === 'inventory') renderInventory(main);
    else if (view === 'sales') renderSales(main);
    else if (view === 'dashboard') renderDashboard(main);
    else if (view === 'reports') renderReports(main);
}

// --- INVENTORY ---
function renderInventory(main) {
    let listHtml = '';
    const available = inventory.filter(p => p.status === 'Available').reverse();
    
    available.forEach(p => {
        listHtml += `
            <div class="list-item" style="cursor:pointer;" onclick="openDeviceDetails('${p.id}')">
                <div class="list-header">
                    <span>${p.brand} ${p.model}</span>
                    <strong style="color:var(--brand);">${formatNaira(p.sellingPrice)}</strong>
                </div>
                <div class="list-sub">${p.ram || ''} ${p.rom || p.storage || ''} · ${p.condition} · IMEI 1: ${p.imei || 'N/A'}</div>
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
        <h3>Add New Device / Kakara</h3>
        <div class="eyebrow" style="margin-top:0;">Device Info</div>
        <div class="row">
            <div class="form-group"><label>Brand</label><input type="text" id="p-brand" placeholder="e.g. Apple"></div>
            <div class="form-group"><label>Model</label><input type="text" id="p-model" placeholder="e.g. iPhone 13"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>RAM</label><input type="text" id="p-ram" placeholder="4GB"></div>
            <div class="form-group"><label>ROM (Storage)</label><input type="text" id="p-rom" placeholder="128GB"></div>
        </div>
        <div class="form-group">
            <label>Condition</label>
            <select id="p-condition">
                <option value="New">New</option>
                <option value="Used - Grade A">Used - Grade A</option>
                <option value="Used - Grade B">Used - Grade B</option>
                <option value="Needs Repair">Needs Repair</option>
            </select>
        </div>
        <div class="row">
            <div class="form-group"><label>IMEI 1 / Serial</label><input type="text" id="p-imei" placeholder="Enter IMEI 1"></div>
            <div class="form-group"><label>IMEI 2</label><input type="text" id="p-imei2" placeholder="Enter IMEI 2 (Optional)"></div>
        </div>
        
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

function openDeviceDetails(id) {
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
        <div class="kv"><span>RAM</span><strong>${p.ram || 'N/A'}</strong></div>
        <div class="kv"><span>ROM (Storage)</span><strong>${p.rom || p.storage || 'N/A'}</strong></div>
        <div class="kv"><span>Condition</span><strong>${p.condition}</strong></div>
        <div class="kv"><span>IMEI 1</span><strong>${p.imei || 'N/A'}</strong></div>
        ${p.imei2 ? `<div class="kv"><span>IMEI 2</span><strong>${p.imei2}</strong></div>` : ''}
        
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
            <div class="form-group"><label>RAM</label><input type="text" id="edit-p-ram" value="${p.ram || ''}"></div>
            <div class="form-group"><label>ROM (Storage)</label><input type="text" id="edit-p-rom" value="${p.rom || p.storage || ''}"></div>
        </div>
        <div class="form-group"><label>Condition</label><select id="edit-p-condition">
                <option value="New" ${p.condition==='New'?'selected':''}>New</option>
                <option value="Used - Grade A" ${p.condition==='Used - Grade A'?'selected':''}>Used - Grade A</option>
                <option value="Used - Grade B" ${p.condition==='Used - Grade B'?'selected':''}>Used - Grade B</option>
                <option value="Needs Repair" ${p.condition==='Needs Repair'?'selected':''}>Needs Repair</option>
            </select></div>
        </div>
        <div class="row">
            <div class="form-group"><label>IMEI 1</label><input type="text" id="edit-p-imei" value="${p.imei || ''}"></div>
            <div class="form-group"><label>IMEI 2</label><input type="text" id="edit-p-imei2" value="${p.imei2 || ''}"></div>
        </div>
        
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
    p.ram = document.getElementById('edit-p-ram').value;
    p.rom = document.getElementById('edit-p-rom').value;
    p.storage = p.rom;
    p.condition = document.getElementById('edit-p-condition').value;
    p.imei = document.getElementById('edit-p-imei').value;
    p.imei2 = document.getElementById('edit-p-imei2').value;
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
    showDialog("Delete Device?", "Are you sure you want to delete this device? This cannot be undone.", () => {
        inventory = inventory.filter(p => p.id !== id);
        saveData('inventory', inventory);
        closeModal();
        nav('inventory');
    });
}

// --- SALES ---
function renderSales(main) {
    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 15);
    
    recentSales.forEach(s => {
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
        optionsHtml += `<option value="${p.id}" data-price="${p.sellingPrice}">${p.brand} ${p.model} (${p.ram || ''}/${p.rom || p.storage || ''}) - ${formatNaira(p.sellingPrice)}</option>`;
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
                <button class="btn" style="margin:0; padding:12px; font-size:12px; background:var(--accent); color:#fff; border:none; border-radius:8px;" onclick="startTradeIn()">🔄 Kakara</button>
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
            <a href="https://wa.me/${(s.customerPhone||'').replace(/^0/, '234')}?text=${encodeURIComponent(`*Receipt - Elbabs Communications*\n\nCustomer: ${s.customerName}\nDevice: ${s.phoneName}\n\n*Total: ${formatNaira(s.totalAmount)}*\nPaid: ${formatNaira(s.amountPaid)}\n*Balance: ${formatNaira(s.balanceOwing)}*`)}" target="_blank"><button class="wa">WhatsApp</button></a>
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
    showDialog("Delete Sale?", "Are you sure? Deleting this sale will return the device to Available stock.", () => {
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
    });
}


function startTradeIn() {
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
                showToast('Enter the Kakara device details below.', 'success');
            }
        }, 100);
    }, 100);
}

function updateSalePrice() {
    const select = document.getElementById('s-device');
    const selectedOption = select.options[select.selectedIndex];
    if (selectedOption.value) {
        document.getElementById('s-price').value = selectedOption.getAttribute('data-price');
        calcSale();
    }
}

function calcSale() {
    const price = parseFloat(document.getElementById('s-price').value) || 0;
    const paid = parseFloat(document.getElementById('s-paid').value) || 0;
    const balance = price - paid;
    document.getElementById('s-balance-display').textContent = balance.toLocaleString();
}

function saveSale() {
    const deviceId = document.getElementById('s-device').value;
    const custName = document.getElementById('s-customer').value || 'Walk-in';
    const custPhone = document.getElementById('s-phone').value || '';
    const price = parseFloat(document.getElementById('s-price').value) || 0;
    const paid = parseFloat(document.getElementById('s-paid').value) || 0;

    if (!deviceId) return showToast('Please select a device.', 'err');
    if (price <= 0) return showToast('Please enter a valid selling price.', 'err');

    const deviceIndex = inventory.findIndex(p => p.id === deviceId);
    if (deviceIndex === -1) return showToast('Device not found in inventory.', 'err');

    const device = inventory[deviceIndex];
    const balance = price - paid;

    inventory[deviceIndex].status = 'Sold';
    saveData('inventory', inventory);

    const sale = {
        id: Date.now().toString(),
        date: new Date().toISOString().split('T')[0],
        customerName: custName,
        customerPhone: custPhone,
        deviceId: deviceId,
        costPrice: device.costPrice,
        phoneName: `${device.brand} ${device.model} (${device.ram || ''}/${device.rom || device.storage || ''})`,
        totalAmount: price,
        amountPaid: paid,
        balanceOwing: balance
    };

    sales.push(sale);
    saveData('sales', sales);

    const waText = encodeURIComponent(`*Receipt - Elbabs Communications*\n\nCustomer: ${custName}\nDevice: ${sale.phoneName}\n\n*Total: ${formatNaira(price)}*\nPaid: ${formatNaira(paid)}\n*Balance: ${formatNaira(balance)}*\n\nThank you for your business!`);
    const waPhone = custPhone.replace(/^0/, '234');
    const waLink = `https://wa.me/${waPhone}?text=${waText}`;

    document.getElementById('modal-body').innerHTML = `
        <div style="text-align:center; margin-bottom:20px;">
            <div style="width:56px; height:56px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 14px;">
                <svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
            </div>
            <h3 style="margin-bottom:4px;">Sale Recorded</h3>
            <p style="font-size:13px; color:var(--muted);">${custName}</p>
            <p style="font-size:28px; font-weight:800; color:var(--brand); margin-top:12px;">${formatNaira(price)}</p>
            ${balance > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Owing ${formatNaira(balance)}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
        </div>
        <div class="actions">
            <a href="${waLink}" target="_blank"><button class="wa">WhatsApp</button></a>
            <button class="outline" onclick="closeModal(); nav('sales')">Close</button>
        </div>
    `;
    document.getElementById('modal').classList.add('active');
}

// --- DASHBOARD ---
function renderDashboard(main) {
    const totalRevenue = sales.reduce((sum, s) => sum + N(s.totalAmount), 0);
    const totalCostSold = sales.reduce((sum, s) => sum + N(s.costPrice), 0);
    const totalExpenses = expenses.reduce((sum, e) => sum + N(e.amount), 0);
    const netProfit = totalRevenue - totalCostSold - totalExpenses;
    
    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaid), 0);
    const totalCapitalAdded = capital.reduce((sum, c) => sum + N(c.amount), 0);
    const cashInHand = cashFromSales + totalCapitalAdded - totalExpenses;
    
    const moneyOwed = sales.reduce((sum, s) => sum + N(s.balanceOwing), 0);
    const capitalInStock = inventory.filter(p => p.status === 'Available').reduce((sum, p) => sum + N(p.costPrice), 0);

    let recentExpenses = [...expenses].reverse().slice(0, 5).map(e => `
        <div class="kv"><span>${e.date} · ${e.note}</span><strong style="color:var(--danger);">-${formatNaira(e.amount)}</strong></div>
    `).join('');

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            <button onclick="openAddExpense()" style="color:var(--danger); border-color:var(--danger); flex: 1 1 45%;">+ Add Expense</button>
            <button onclick="nav('reports')" style="flex: 1 1 45%;">📁 Reports & Backup</button>
        </div>

        <div class="hero">
            <div class="lbl">Net Profit</div>
            <div class="big ${netProfit < 0 ? 'neg' : ''}">${formatNaira(netProfit)}</div>
            <div class="meta">
                <div>Revenue<strong>${formatNaira(totalRevenue)}</strong></div>
                <div>Expenses<strong>${formatNaira(totalExpenses)}</strong></div>
            </div>
        </div>

        <div class="dash-grid">
            <div class="stat" onclick="openAddCapitalModal()" style="cursor:pointer; border: 2px dashed var(--brand); position:relative;">
                <div class="top"><span class="dot g">${icon('cash')}</span><h4>Cash in Hand <span style="color:var(--brand); font-size:16px; font-weight:bold;">+ Add Cash</span></h4></div>
                <div class="val">${formatNaira(cashInHand)}</div>
            </div>
            <div class="stat"><div class="top"><span class="dot r">${icon('arrowIn')}</span><h4>Owed to You</h4></div><div class="val">${formatNaira(moneyOwed)}</div></div>
            <div class="stat"><div class="top"><span class="dot b">${icon('box')}</span><h4>Capital in Stock</h4></div><div class="val">${formatNaira(capitalInStock)}</div></div>
        </div>

        <div class="card">
            <h3>Recent Expenses</h3>
            ${recentExpenses || '<p style="font-size:13px; color:var(--muted);">No expenses logged yet.</p>'}
        </div>
    `;
}

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
        date: new Date().toISOString().split('T')[0],
        amount: amount,
        note: document.getElementById('cap-note').value || 'Owner Capital'
    });
    
    saveData('capital', capital);
    closeModal();
    nav('dashboard');
}

// --- REPORTS & BACKUP ---
function renderReports(main) {
    main.innerHTML = `
        <h3 style="margin-bottom:16px;">Reports & Backup</h3>
        
        <div class="card">
            <h3>Data Backup</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:14px;">Save a backup of all your inventory, sales, and expenses to your phone.</p>
            <button class="btn btn-primary" style="margin-bottom:8px;" onclick="exportJSON()">📤 Export JSON Backup</button>
            
            <input type="file" id="import-file" accept=".json" style="display:none;" onchange="importJSON(event)">
            <button class="btn" style="background:#64748b;" onclick="document.getElementById('import-file').click()">📥 Import JSON Backup</button>
            
            <button class="btn" style="background:#2563eb; margin-top:12px;" onclick="emailBackup()">✉️ Email Backup File</button>
        </div>

        <div class="card">
            <h3>Sales Report</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:14px;">Download a CSV spreadsheet of all your sales for accounting.</p>
            <button class="btn" style="background:#059669;" onclick="exportCSV()">Export Sales to CSV</button>
        </div>

        <button class="btn outline" onclick="nav('dashboard')">Back to Dashboard</button>
    `;
}

function exportJSON() {
    const data = {
        settings: JSON.parse(localStorage.getItem('elbabs:settings')) || {},
        inventory: JSON.parse(localStorage.getItem('elbabs:inventory')) || [],
        sales: JSON.parse(localStorage.getItem('elbabs:sales')) || [],
        expenses: JSON.parse(localStorage.getItem('elbabs:expenses')) || [],
        capital: JSON.parse(localStorage.getItem('elbabs:capital')) || []
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'Elbabs_Backup_' + new Date().toISOString().split('T')[0] + '.json';
    a.click();
    URL.revokeObjectURL(url);
}

async function emailBackup() {
    const data = {
        settings: JSON.parse(localStorage.getItem('elbabs:settings')) || {},
        inventory: JSON.parse(localStorage.getItem('elbabs:inventory')) || [],
        sales: JSON.parse(localStorage.getItem('elbabs:sales')) || [],
        expenses: JSON.parse(localStorage.getItem('elbabs:expenses')) || [],
        capital: JSON.parse(localStorage.getItem('elbabs:capital')) || []
    };
    const jsonStr = JSON.stringify(data, null, 2);
    const filename = 'Elbabs_Backup_' + new Date().toISOString().split('T')[0] + '.json';
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const file = new File([blob], filename, { type: 'application/json' });

    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
            await navigator.share({ files: [file], title: 'Elbabs Communications Backup' });
        } catch (e) { console.log('Share failed', e); }
    } else {
        showToast("Share not supported. File downloaded.", 'default');
        exportJSON();
    }
}

function importJSON(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (!data.inventory || !data.sales) {
                throw new Error('Invalid backup file: missing required sections.');
            }
            if (data.settings) localStorage.setItem('elbabs:settings', JSON.stringify(data.settings));
            localStorage.setItem('elbabs:inventory', JSON.stringify(data.inventory));
            localStorage.setItem('elbabs:sales', JSON.stringify(data.sales));
            localStorage.setItem('elbabs:expenses', JSON.stringify(data.expenses || []));
            localStorage.setItem('elbabs:capital', JSON.stringify(data.capital || []));
            showToast('Data restored successfully! Reloading...', 'success');
            location.reload();
        } catch(err) { showToast('Error: ' + err.message, 'err'); }
    };
    reader.readAsText(file);
}

function exportCSV() {
    let csv = "Date,Customer,Device,Total Amount,Paid,Balance\n";
    sales.forEach(s => {
        csv += `${s.date},"${s.customerName}","${s.phoneName}",${s.totalAmount},${s.amountPaid},${s.balanceOwing}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'Elbabs_Sales_' + new Date().toISOString().split('T')[0] + '.csv';
    a.click();
    URL.revokeObjectURL(url);
}

function icon(name) {
    const icons = {
        cash: '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
        arrowIn: '<path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/>',
        box: '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5"/>'
    };
    return `<svg class="ic" viewBox="0 0 24 24" style="width:16px;height:16px;">${icons[name]||''}</svg>`;
}

function openAddExpense() {
    document.getElementById('modal-body').innerHTML = `
        <h3>Add Expense</h3>
        <div class="form-group"><label>Date</label><input type="date" id="e-date" value="${new Date().toISOString().split('T')[0]}"></div>
        <div class="form-group"><label>Amount (₦)</label><input type="number" id="e-amount" placeholder="0"></div>
        <div class="form-group"><label>Note / Category</label><input type="text" id="e-note" placeholder="e.g. Shop Rent, Transport"></div>
        <button class="btn" onclick="saveExpense()">Save Expense</button>
        <button class="btn" style="background:var(--bg); color:var(--text); border:1px solid var(--line);" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function saveExpense() {
    const amt = parseFloat(document.getElementById('e-amount').value) || 0;
    if (amt <= 0) return showToast('Enter a valid amount', 'err');

    expenses.push({
        id: Date.now().toString(),
        date: document.getElementById('e-date').value,
        amount: amt,
        note: document.getElementById('e-note').value || 'General Expense'
    });
    saveData('expenses', expenses);
    closeModal();
    nav('dashboard');
}

// --- SMART BACK BUTTON & INIT ---
if (sessionStorage.getItem('elbabs:auth') === 'true') {
    document.getElementById('login-view').classList.remove('active');
    document.getElementById('app-view').classList.add('active');
    nav('inventory');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(err => console.log('SW registration failed', err));
}

let backPressCount = 0;
let backPressTimer = null;
history.pushState({ page: 'main' }, '', location.href);

window.addEventListener('popstate', function(event) {
    history.pushState({ page: 'main' }, '', location.href);

    if (sessionStorage.getItem('elbabs:auth') === 'true') {
        if (currentView !== 'inventory') {
            nav('inventory');
            backPressCount = 0;
            if (backPressTimer) clearTimeout(backPressTimer);
            return;
        }
    }

    backPressCount++;
    if (backPressCount === 3) {
        if (backPressTimer) clearTimeout(backPressTimer);
        backPressCount = 0;
        window.location.href = '../index.html';
    } else {
        showToast(\`Press back \${3 - backPressCount} more time\${3 - backPressCount > 1 ? 's' : ''} to exit\`, 'default');
        if (backPressTimer) clearTimeout(backPressTimer);
        backPressTimer = setTimeout(() => { backPressCount = 0; }, 2000);
    }
});

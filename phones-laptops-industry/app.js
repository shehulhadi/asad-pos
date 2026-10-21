let settings = JSON.parse(localStorage.getItem('elbabs:settings')) || { pin: '1234' };
let inventory = JSON.parse(localStorage.getItem('elbabs:inventory')) || [];
let sales = JSON.parse(localStorage.getItem('elbabs:sales')) || [];
let expenses = JSON.parse(localStorage.getItem('elbabs:expenses')) || [];
let currentView = 'inventory';

function saveData(key, data) { localStorage.setItem('elbabs:' + key, JSON.stringify(data)); }
function formatNaira(num) { return '₦' + Number(num).toLocaleString(); }
function closeModal() { document.getElementById('modal').classList.remove('active'); }

async function forceUpdate() {
    if (confirm("This will download the latest app version.\nYOUR DATA WILL NOT BE DELETED.\n\nContinue?")) {
        try {
            if ('serviceWorker' in navigator) {
                const regs = await navigator.serviceWorker.getRegistrations();
                for (let r of regs) await r.unregister();
            }
            const keys = await caches.keys();
            for (let k of keys) await caches.delete(k);
        } catch(e) {}
        window.location.reload(true);
    }
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
                <div class="list-sub">${p.storage} · ${p.condition} · IMEI: ${p.imei || 'N/A'}</div>
                <div class="list-sub" style="margin-top:4px;">Seller: ${p.sellerName || 'Unknown'} (${p.sellerPhone || 'No phone'})</div>
                <div style="margin-top:6px;"><span class="tag green">In Stock</span></div>
            </div>
        `;
    });

    main.innerHTML = `
        <div class="card">
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
        </div>

        <h3 style="margin: 20px 0 10px; font-size: 16px;">Available Inventory (${available.length})</h3>
        ${listHtml || '<p style="text-align:center; color:var(--muted);">No devices in stock yet.</p>'}
    `;
}

function savePhone() {
    const brand = document.getElementById('p-brand').value;
    const model = document.getElementById('p-model').value;
    const cost = parseFloat(document.getElementById('p-cost').value) || 0;
    const sell = parseFloat(document.getElementById('p-sell').value) || 0;
    
    if(!brand || !model || sell <= 0) return alert('Please fill Brand, Model and Selling Price');

    const phone = {
        id: Date.now().toString(),
        date: new Date().toISOString().split('T')[0],
        brand: brand,
        model: model,
        storage: document.getElementById('p-storage').value || 'N/A',
        condition: document.getElementById('p-condition').value,
        imei: document.getElementById('p-imei').value || '',
        sellerName: document.getElementById('p-seller-name').value || '',
        sellerPhone: document.getElementById('p-seller-phone').value || '',
        sellerAddress: document.getElementById('p-seller-address').value || '',
        costPrice: cost,
        sellingPrice: sell,
        status: 'Available'
    };

    inventory.push(phone);
    saveData('inventory', inventory);
    nav('inventory');
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
        
        <button class="btn outline" style="margin-top:20px;" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}

// --- SALES ---
function renderSales(main) {
    const availablePhones = inventory.filter(p => p.status === 'Available');
    
    let optionsHtml = '<option value="">-- Select a device --</option>';
    availablePhones.forEach(p => {
        optionsHtml += `<option value="${p.id}" data-price="${p.sellingPrice}">${p.brand} ${p.model} (${p.storage}) - ${formatNaira(p.sellingPrice)}</option>`;
    });

    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 10);
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
        <div class="card">
            <h3>New Sale</h3>
            <div class="row">
                <div class="form-group" style="flex:2;">
                    <label>Select Device</label>
                    <select id="s-device" onchange="updateSalePrice()">
                        ${optionsHtml}
                    </select>
                </div>
                <div class="form-group" style="flex:1; display:flex; align-items:flex-end;">
                    <button class="btn" style="margin:0; padding:10px; font-size:12px; background:var(--accent);" onclick="startTradeIn()">🔄 Trade-In</button>
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
        </div>

        <h3 style="margin: 20px 0 10px; font-size: 16px;">Recent Sales</h3>
        ${historyHtml || '<p style="text-align:center; color:var(--muted);">No sales recorded yet.</p>'}
    `;
}

function startTradeIn() {
    const custName = document.getElementById('s-customer').value;
    const custPhone = document.getElementById('s-phone').value;
    
    nav('inventory');
    
    // Pre-fill seller info with customer info
    setTimeout(() => {
        if(document.getElementById('p-seller-name')) {
            document.getElementById('p-seller-name').value = custName;
            document.getElementById('p-seller-phone').value = custPhone;
            window.scrollTo(0, document.body.scrollHeight);
            alert('Enter the Trade-In device details below. Customer info has been pre-filled as the Seller.');
        }
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

    if (!deviceId) return alert('Please select a device.');
    if (price <= 0) return alert('Please enter a valid selling price.');

    const deviceIndex = inventory.findIndex(p => p.id === deviceId);
    if (deviceIndex === -1) return alert('Device not found in inventory.');

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
        phoneName: `${device.brand} ${device.model} (${device.storage})`,
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

function renderDashboard(main) {
    const totalRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0);
    const totalCostSold = sales.reduce((sum, s) => sum + (s.costPrice || 0), 0);
    const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
    const netProfit = totalRevenue - totalCostSold - totalExpenses;
    
    const cashInHand = sales.reduce((sum, s) => sum + s.amountPaid, 0);
    const moneyOwed = sales.reduce((sum, s) => sum + s.balanceOwing, 0);
    const capitalInStock = inventory.filter(p => p.status === 'Available').reduce((sum, p) => sum + p.costPrice, 0);

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
            <div class="stat"><div class="top"><span class="dot g">${icon('cash')}</span><h4>Cash in Hand</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>
            <div class="stat"><div class="top"><span class="dot r">${icon('arrowIn')}</span><h4>Owed to You</h4></div><div class="val">${formatNaira(moneyOwed)}</div></div>
            <div class="stat"><div class="top"><span class="dot b">${icon('box')}</span><h4>Capital in Stock</h4></div><div class="val">${formatNaira(capitalInStock)}</div></div>
        </div>

        <div class="card">
            <h3>Recent Expenses</h3>
            ${recentExpenses || '<p style="font-size:13px; color:var(--muted);">No expenses logged yet.</p>'}
        </div>
    `;
}

function renderReports(main) {
    main.innerHTML = `
        <h3 style="margin-bottom:16px;">Reports & Backup</h3>
        
        <div class="card">
            <h3>Data Backup</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:14px;">Save a backup of all your inventory, sales, and expenses to your phone.</p>
            <button class="btn btn-primary" style="margin-bottom:8px;" onclick="exportJSON()">📤 Export JSON Backup</button>
            
            <input type="file" id="import-file" accept=".json" style="display:none;" onchange="importJSON(event)">
            <button class="btn" style="background:#64748b;" onclick="document.getElementById('import-file').click()">📥 Import JSON Backup</button>
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
        expenses: JSON.parse(localStorage.getItem('elbabs:expenses')) || []
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'Elbabs_Backup_' + new Date().toISOString().split('T')[0] + '.json';
    a.click();
    URL.revokeObjectURL(url);
}

function importJSON(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (data.inventory && data.sales) {
                if (data.settings) localStorage.setItem('elbabs:settings', JSON.stringify(data.settings));
                localStorage.setItem('elbabs:inventory', JSON.stringify(data.inventory));
                localStorage.setItem('elbabs:sales', JSON.stringify(data.sales));
                localStorage.setItem('elbabs:expenses', JSON.stringify(data.expenses || []));
                alert('Data restored successfully! App will reload.');
                location.reload();
            } else {
                alert('Invalid backup file.');
            }
        } catch(err) { alert('Error parsing file: ' + err.message); }
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
    if (amt <= 0) return alert('Enter a valid amount');

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

if (sessionStorage.getItem('elbabs:auth') === 'true') {
    document.getElementById('login-view').classList.remove('active');
    document.getElementById('app-view').classList.add('active');
    nav('inventory');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(err => console.log('SW registration failed', err));
}

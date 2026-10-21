let settings = JSON.parse(localStorage.getItem('elbabs:settings')) || { pin: '1234' };
let inventory = JSON.parse(localStorage.getItem('elbabs:inventory')) || [];
let sales = JSON.parse(localStorage.getItem('elbabs:sales')) || [];
let currentView = 'inventory';

function saveData(key, data) { localStorage.setItem('elbabs:' + key, JSON.stringify(data)); }
function formatNaira(num) { return '₦' + Number(num).toLocaleString(); }
function closeModal() { document.getElementById('modal').classList.remove('active'); }

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
    else if (view === 'dashboard') main.innerHTML = '<div class="card"><h3>Dashboard</h3><p style="text-align:center; color:var(--muted); padding:20px;">Coming in Phase 3</p></div>';
}

function renderInventory(main) {
    let listHtml = '';
    const available = inventory.filter(p => p.status === 'Available').reverse();
    
    available.forEach(p => {
        listHtml += `
            <div class="list-item">
                <div class="list-header">
                    <span>${p.brand} ${p.model}</span>
                    <strong style="color:var(--brand);">${formatNaira(p.sellingPrice)}</strong>
                </div>
                <div class="list-sub">${p.storage} · ${p.condition} · Cost: ${formatNaira(p.costPrice)}</div>
                <div style="margin-top:6px;"><span class="tag green">In Stock</span></div>
            </div>
        `;
    });

    main.innerHTML = `
        <div class="card">
            <h3>Add New Phone / Laptop</h3>
            <div class="form-group"><label>Brand (e.g. Apple, Samsung)</label><input type="text" id="p-brand" placeholder="Brand"></div>
            <div class="form-group"><label>Model (e.g. iPhone 13, Galaxy A54)</label><input type="text" id="p-model" placeholder="Model"></div>
            <div class="row">
                <div class="form-group"><label>Storage (e.g. 128GB)</label><input type="text" id="p-storage" placeholder="128GB"></div>
                <div class="form-group"><label>Condition</label><select id="p-condition">
                    <option value="New">New</option>
                    <option value="Used - Grade A">Used - Grade A</option>
                    <option value="Used - Grade B">Used - Grade B</option>
                    <option value="Needs Repair">Needs Repair</option>
                </select></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Cost Price (₦)</label><input type="number" id="p-cost" placeholder="0"></div>
                <div class="form-group"><label>Selling Price (₦)</label><input type="number" id="p-sell" placeholder="0"></div>
            </div>
            <button class="btn" onclick="savePhone()">Add to Inventory</button>
        </div>

        <h3 style="margin: 20px 0 10px; font-size: 16px;">Available Inventory (${available.length})</h3>
        ${listHtml || '<p style="text-align:center; color:var(--muted);">No phones in stock yet.</p>'}
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
        costPrice: cost,
        sellingPrice: sell,
        status: 'Available'
    };

    inventory.push(phone);
    saveData('inventory', inventory);
    nav('inventory');
}

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
            <div class="form-group">
                <label>Select Device</label>
                <select id="s-device" onchange="updateSalePrice()">
                    ${optionsHtml}
                </select>
            </div>
            <div class="form-group"><label>Customer Name</label><input type="text" id="s-customer" placeholder="Name"></div>
            <div class="form-group"><label>Phone Number</label><input type="tel" id="s-phone" placeholder="Phone"></div>
            
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

if (sessionStorage.getItem('elbabs:auth') === 'true') {
    document.getElementById('login-view').classList.remove('active');
    document.getElementById('app-view').classList.add('active');
    nav('inventory');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js').catch(err => console.log('SW registration failed', err));
}

import re
with open('index.html', 'r') as f: html = f.read()

# ==========================================
# 1. DASHBOARD STOCK ALERTS
# ==========================================
old_dash_start = '''        const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);'''
new_dash_start = '''        // Calculate raw stock for alerts
        const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
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
        const fuelStock = fuelPurchased - fuelUsed + fuelAdj;

        let lowStockHtml = '';
        if (cementStock <= settings.lowCement) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>🪨 Cement</span><span>${cementStock} bags left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowCement})</div></div>`;
        if (sandStock <= settings.lowSand) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>🏖️ Sand</span><span>${sandStock} trips left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowSand})</div></div>`;
        if (fuelStock <= settings.lowFuel) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>⛽ Fuel</span><span>${fuelStock} litres left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowFuel})</div></div>`;

        const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);'''
html = html.replace(old_dash_start, new_dash_start)

# Inject Low Stock into Dashboard HTML
html = html.replace(
    '''            <div class="hero">
                <div class="lbl">${t.netProfit}</div>''',
    '''            ${lowStockHtml ? `<div class="section-title neg">${ico('alert')} Low Stock Alerts</div>${lowStockHtml}` : ''}

            <div class="hero">
                <div class="lbl">${t.netProfit}</div>'''
)

# ==========================================
# 2. SEARCH: SALES
# ==========================================
old_sales_html = '''            <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('sales')} ${t.salesHistory}</span>
                <button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn || 'Log Return'}</button>
            </div>
            ${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}'''
new_sales_html = '''            <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('sales')} ${t.salesHistory}</span>
                <button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn || 'Log Return'}</button>
            </div>
            <div class="form-group" style="margin-bottom:12px;">
                <input type="text" id="search-sales" placeholder="Search by customer name or date..." oninput="filterSales(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;">
            </div>
            <div id="sales-history-list">
                ${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}
            </div>'''
html = html.replace(old_sales_html, new_sales_html)

# ==========================================
# 3. SEARCH: DEBTS
# ==========================================
old_debts_html = '''        let html = `
            <div class="segmented">
                <button class="${currentDebtTab === 'customer' ? 'on' : ''}" onclick="setDebtTab('customer')">${t.customerDebts}</button>
                <button class="${currentDebtTab === 'supplier' ? 'on' : ''}" onclick="setDebtTab('supplier')">${t.supplierDebts}</button>
            </div>
        `;'''
new_debts_html = '''        let html = `
            <div class="segmented">
                <button class="${currentDebtTab === 'customer' ? 'on' : ''}" onclick="setDebtTab('customer')">${t.customerDebts}</button>
                <button class="${currentDebtTab === 'supplier' ? 'on' : ''}" onclick="setDebtTab('supplier')">${t.supplierDebts}</button>
            </div>
            <div class="form-group" style="margin-bottom:12px;">
                <input type="text" id="search-debts" placeholder="Search name..." oninput="filterDebts(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;">
            </div>
            <div id="debts-list">
        `;'''
html = html.replace(old_debts_html, new_debts_html)

# Close the div at the end of renderDebts
old_debts_end = '''        main.innerHTML = html;
    }

    function setDebtTab(tab) {'''
new_debts_end = '''        html += `</div>`; // Close debts-list
        main.innerHTML = html;
    }

    function setDebtTab(tab) {'''
html = html.replace(old_debts_end, new_debts_end)

# ==========================================
# 4. SEARCH: INVENTORY PURCHASES
# ==========================================
old_inv_purchases = '''                <div class="section-title" style="margin-top:16px; margin-bottom:8px;">Recent Purchases</div>
                ${purchases.length > 0 ? [...purchases].reverse().slice(0,5).map(p => `
                    <div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')">
                        <div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div>
                        <div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div>
                    </div>
                `).join('') : '<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases logged yet.</p>'}'''
new_inv_purchases = '''                <div class="section-title" style="margin-top:16px; margin-bottom:8px;">Recent Purchases</div>
                <div class="form-group" style="margin-bottom:12px;">
                    <input type="text" id="search-purchases" placeholder="Search supplier..." oninput="filterPurchases(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;">
                </div>
                <div id="purchases-list">
                    ${purchases.length > 0 ? [...purchases].reverse().slice(0,5).map(p => `
                        <div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')">
                            <div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div>
                            <div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div>
                        </div>
                    `).join('') : '<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases logged yet.</p>'}
                </div>'''
html = html.replace(old_inv_purchases, new_inv_purchases)

# ==========================================
# 5. INJECT FILTER JS FUNCTIONS
# ==========================================
search_js = '''
    function filterSales(query) {
        const q = query.toLowerCase();
        const filtered = [...sales].reverse().filter(s => s.customerName.toLowerCase().includes(q) || s.date.includes(q)).slice(0, 15);
        let html = '';
        filtered.forEach(s => {
            html += `
                <div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')">
                    <div class="list-header">
                        <span>${s.customerName}</span>
                        <strong class="pos">${formatNaira(s.totalAmount)}</strong>
                    </div>
                    <div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
                </div>
            `;
        });
        document.getElementById('sales-history-list').innerHTML = html || `<div class="empty">No sales found.</div>`;
    }

    function filterDebts(query) {
        const q = query.toLowerCase();
        let html = '';
        if (currentDebtTab === 'customer') {
            const owingSales = sales.filter(s => s.balanceOwing > 0 && s.customerName.toLowerCase().includes(q));
            if (owingSales.length === 0) { html += `<div class="empty">No outstanding customer debts found.</div>`; }
            else {
                owingSales.forEach(s => {
                    const days = Math.floor((new Date() - new Date(s.date)) / (1000 * 60 * 60 * 24));
                    const waText = encodeURIComponent(`Hello ${s.customerName}, this is a reminder from ${settings.businessName}. Your outstanding balance is ₦${s.balanceOwing}. Please settle. Thank you!`);
                    const waPhone = (s.customerPhone || '').replace(/^0/, '234');
                    const waLink = `https://wa.me/${waPhone}?text=${waText}`;
                    html += `<div class="list-item owing">
                        <div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div>
                        <div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${s.size}" Blocks · ${s.quantity} pcs · ${days} ${i18n[settings.lang].daysAgo}</div>
                        <div class="actions">
                            <button onclick="openPayment('${s.id}')">${i18n[settings.lang].pay}</button>
                            <a href="${waLink}" target="_blank"><button class="wa">${i18n[settings.lang].remind}</button></a>
                        </div>
                    </div>`;
                });
            }
        } else {
            const owingPurchases = purchases.filter(p => p.cost > (p.amountPaid || 0) && p.supplierName.toLowerCase().includes(q));
            if (owingPurchases.length === 0) { html += `<div class="empty">No outstanding supplier debts found.</div>`; }
            else {
                owingPurchases.forEach(p => {
                    const balance = p.cost - (p.amountPaid || 0);
                    const days = Math.floor((new Date() - new Date(p.date)) / (1000 * 60 * 60 * 24));
                    html += `<div class="list-item owing">
                        <div class="list-header"><span>${p.supplierName || 'Unknown Supplier'}</span><span class="neg">₦${balance.toLocaleString()}</span></div>
                        <div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${p.material.toUpperCase()} · ${p.qty} units · ${days} ${i18n[settings.lang].daysAgo}</div>
                        <div class="list-sub">Total ₦${p.cost.toLocaleString()} · Paid ₦${(p.amountPaid || 0).toLocaleString()}</div>
                        <div class="actions">
                            <button onclick="openSupplierPayment('${p.id}')" style="background:var(--accent-soft); color:#92400e; border-color:#fde68a;">${i18n[settings.lang].paySupplier}</button>
                        </div>
                    </div>`;
                });
            }
        }
        document.getElementById('debts-list').innerHTML = html;
    }

    function filterPurchases(query) {
        const q = query.toLowerCase();
        const filtered = [...purchases].reverse().filter(p => p.supplierName.toLowerCase().includes(q)).slice(0, 5);
        let html = '';
        filtered.forEach(p => {
            html += `
                <div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')">
                    <div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div>
                    <div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div>
                </div>
            `;
        });
        document.getElementById('purchases-list').innerHTML = html || `<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases found.</p>`;
    }
'''
html = html.replace('// --- Details & Edit Modals ---', search_js + '\n// --- Details & Edit Modals ---')

with open('index.html', 'w') as f: f.write(html)

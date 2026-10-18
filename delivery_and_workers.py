import re
with open('index.html', 'r') as f: html = f.read()

# ==========================================
# 1. DELIVERY STATUS TRACKING
# ==========================================

# Update saveSale to default to 'pending'
html = html.replace(
    "const sale = { id: Date.now().toString(), date: saleDate, customerName: document.getElementById('s-customer').value || 'Walk-in', customerPhone: document.getElementById('s-phone').value, size: document.getElementById('s-size').value, quantity: qty, pricePerBlock: price, deliveryCharge: delivery, totalAmount: total, amountPaidAtSale: paid, balanceOwing: balance };",
    "const sale = { id: Date.now().toString(), date: saleDate, customerName: document.getElementById('s-customer').value || 'Walk-in', customerPhone: document.getElementById('s-phone').value, size: document.getElementById('s-size').value, quantity: qty, pricePerBlock: price, deliveryCharge: delivery, totalAmount: total, amountPaidAtSale: paid, balanceOwing: balance, deliveryStatus: 'pending' };"
)

# Update Sale History List to show Delivery Status
old_hist = '''<div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}'''
new_hist = '''<div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    <div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">
                        ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
                        ${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending Delivery</span>`}
                    </div>'''
html = html.replace(old_hist, new_hist)

# (Also apply to filterSales history builder)
old_filter_hist = '''<div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}'''
new_filter_hist = '''<div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    <div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">
                        ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
                        ${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending Delivery</span>`}
                    </div>'''
html = html.replace(old_filter_hist, new_filter_hist)

# Add toggle button to openSaleDetails modal
old_details_actions = '''<div class="row">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
            </div>'''
new_details_actions = '''<div class="row" style="margin-top:12px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
            </div>
            <button class="btn ${s.deliveryStatus === 'delivered' ? 'btn-outline' : 'btn-dark'}" style="margin-top:8px; ${s.deliveryStatus === 'delivered' ? 'border-color:var(--brand); color:var(--brand);' : ''}" onclick="toggleDelivery('${s.id}')">
                ${s.deliveryStatus === 'delivered' ? '✅ Mark as Pending' : '🚚 Mark as Delivered'}
            </button>'''
html = html.replace(old_details_actions, new_details_actions)

# Add toggleDelivery function
toggle_func = '''
    function toggleDelivery(id) {
        const s = sales.find(x => x.id === id);
        if (!s) return;
        s.deliveryStatus = s.deliveryStatus === 'delivered' ? 'pending' : 'delivered';
        saveData('sales', sales);
        openSaleDetails(id); // Refresh modal
        showToast('Delivery status updated', 'success');
    }
'''
html = html.replace('// --- Details & Edit Modals ---', toggle_func + '\n// --- Details & Edit Modals ---')


# ==========================================
# 2. WORKER DATALIST (AUTO-REMEMBER)
# ==========================================

old_prod_worker = '''<div class="form-group"><label>${t.worker}</label><input type="text" id="p-worker" placeholder="Worker name"></div>'''
new_prod_worker = '''<div class="form-group"><label>${t.worker}</label><input type="text" id="p-worker" list="worker-names" placeholder="Worker name"><datalist id="worker-names"></datalist></div>'''
html = html.replace(old_prod_worker, new_prod_worker)

# Populate worker datalist in renderProduction
old_prod_render = '''    function renderProduction(main) { 
        const t = i18n[settings.lang]; const today = new Date().toISOString().split('T')[0];'''
new_prod_render = '''    function renderProduction(main) { 
        const t = i18n[settings.lang]; const today = new Date().toISOString().split('T')[0];
        const uniqueWorkers = [...new Set(batches.map(b => b.worker).filter(w => w && w !== 'Unknown' && w !== 'System Adjustment'))];'''
html = html.replace(old_prod_render, new_prod_render)

# Add the datalist HTML to the production form
old_prod_datalist_anchor = '''            <div class="section-title">${ico('bars')} Recent Batches</div>${listHtml || '<div class="empty">No batches logged yet.</div>'}`;'''
new_prod_datalist_anchor = '''            <div class="section-title">${ico('bars')} Recent Batches</div>${listHtml || '<div class="empty">No batches logged yet.</div>'}`;
        document.getElementById('worker-names').innerHTML = uniqueWorkers.map(w => `<option value="${w}"></option>`).join('');'''
html = html.replace(old_prod_datalist_anchor, new_prod_datalist_anchor)

with open('index.html', 'w') as f: f.write(html)

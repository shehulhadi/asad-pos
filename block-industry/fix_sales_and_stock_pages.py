import re
with open('app.js', 'r') as f: js = f.read()

# ==========================================
# 1. FIX SALES BUG (Allow sale without blocks)
# ==========================================
old_sale_validate = '''        const qty = parseInt(document.getElementById('s-qty').value) || 0;
        const price = parseInt(document.getElementById('s-price').value) || 0;
        const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
        const paid = parseInt(document.getElementById('s-paid').value) || 0;
        const saleDate = document.getElementById('s-date').value || getTodayStr();
        const custName = document.getElementById('s-customer').value || 'Walk-in';
        if(qty <= 0) return showToast('Enter valid quantity', 'err');'''

new_sale_validate = '''        const qty = parseInt(document.getElementById('s-qty')?.value) || 0;
        const price = parseInt(document.getElementById('s-price')?.value) || 0;
        const delivery = parseInt(document.getElementById('s-delivery')?.value) || 0;
        const paid = parseInt(document.getElementById('s-paid')?.value) || 0;
        const saleDate = document.getElementById('s-date')?.value || getTodayStr();
        const custName = document.getElementById('s-customer')?.value || 'Walk-in';
        
        const cQty = parseInt(document.getElementById('s-cement-qty')?.value) || 0;
        const sQty = parseInt(document.getElementById('s-sand-qty')?.value) || 0;
        const eQty = parseInt(document.getElementById('s-empty-bag-qty')?.value) || 0;

        if (qty <= 0 && cQty <= 0 && sQty <= 0 && eQty <= 0) {
            return showToast('Enter a quantity for at least one item', 'err');
        }'''
js = js.replace(old_sale_validate, new_sale_validate)

# ==========================================
# 2. REDESIGN STOCK DETAILS (Full Page)
# ==========================================
# Add global vars for routing
js = js.replace("let currentDebtTab = 'customer';", "let currentDebtTab = 'customer';\nlet stockType = '';\nlet stockSize = '';")

# Update nav function to handle the new page
old_nav = '''        if (view === 'dashboard') renderDashboard(main);
        else if (view === 'analytics') renderAnalytics(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'reports') renderReports(main);'''
new_nav = '''        if (view === 'dashboard') renderDashboard(main);
        else if (view === 'analytics') renderAnalytics(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'reports') renderReports(main);
        else if (view === 'stock_details') renderStockDetails(main, stockType, stockSize);'''
js = js.replace(old_nav, new_nav)

# Update Dashboard tiles to use the new page routing
old_tile = '''    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockItem('${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight: 700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;'''
new_tile = '''    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="nav('stock_details', null, '${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight: 700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;'''
js = js.replace(old_tile, new_tile)

# Fix nav function to accept type/size (optional params)
js = js.replace("function nav(view) {", "function nav(view, btn = null, type = null, size = null) {")
js = js.replace("    currentView = view;", "    currentView = view;\n    if (type) stockType = type;\n    if (size) stockSize = size;")

# Remove old openStockItem function and replace with renderStockDetails
start = js.find('function openStockItem(type, size) {')
end = js.find('function openAddStock(type, size) {')

if start != -1 and end != -1:
    new_func = '''function renderStockDetails(main, type, size) {
    let title = '';
    let currentStock = 0;
    let historyHtml = '';
    let hist = [];

    if (type === 'cement' || type === 'sand' || type === 'empty_bag') {
        title = type === 'cement' ? 'Cement' : (type === 'sand' ? 'Sand' : 'Empty Bags');
        if (type === 'cement') {
            const purchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        } else if (type === 'sand') {
            const purchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.sandQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        } else {
            const purchased = purchases.filter(p=>p.material==='empty_bag').reduce((s,p)=>s+p.qty,0);
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const sold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased + produced - sold + adj;
        }

        purchases.filter(p=>p.material===type).forEach(p => hist.push({ id: p.id, timestamp: Number(p.id) || new Date(p.date).getTime(), clickType: 'pur', date: p.date, desc: `Purchase from ${p.supplierName}`, qty: `+${p.qty}`, color: 'var(--brand)' }));
        stockAdjustments.filter(a=>a.material===type).forEach(a => hist.push({ id: a.id, timestamp: Number(a.id) || new Date(a.date).getTime(), date: a.date, desc: `Adjustment: ${a.reason}`, qty: a.qty > 0 ? `+${a.qty}` : `${a.qty}`, color: a.qty > 0 ? 'var(--brand)' : 'var(--danger)' }));
        
        if(type === 'empty_bag') {
            batches.forEach(b => { if(b.cementBags > 0) hist.push({ id: b.id, timestamp: Number(b.id) || new Date(b.date).getTime(), date: b.date, desc: `Generated from cement usage`, qty: `+${b.cementBags}`, color: 'var(--brand)' }); });
            sales.forEach(s => { if(s.emptyBagQty > 0) hist.push({ id: s.id, timestamp: Number(s.id) || new Date(s.date).getTime(), clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.emptyBagQty}`, color: 'var(--danger)' }); });
        } else {
            batches.forEach(b => {
                if(type === 'cement' && b.cementBags > 0) hist.push({ id: b.id, timestamp: Number(b.id) || new Date(b.date).getTime(), date: b.date, desc: `Used in 6" batch`, qty: `-${b.cementBags}`, color: 'var(--danger)' });
                if(type === 'sand' && b.sandQty > 0) hist.push({ id: b.id, timestamp: Number(b.id) || new Date(b.date).getTime(), date: b.date, desc: `Used in 6" batch`, qty: `-${b.sandQty}`, color: 'var(--danger)' });
            });
        }
    } else {
        title = '6" Blocks';
        const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
        currentStock = produced - sold - broken + returned;

        readyBatches.forEach(b => hist.push({ id: b.id, timestamp: Number(b.id) || new Date(b.date).getTime(), date: b.date, desc: `Produced (${b.worker})`, qty: `+${b.blocksProduced}`, color: 'var(--brand)' }));
        sales.filter(s=>s.size==='6').forEach(s => hist.push({ id: s.id, timestamp: Number(s.id) || new Date(s.date).getTime(), clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.quantity}`, color: 'var(--danger)' }));
        breakagesLog.filter(b=>b.size==='6').forEach(b => hist.push({ id: b.id, timestamp: Number(b.id) || new Date(b.date).getTime(), date: b.date, desc: `Breakage: ${b.reason}`, qty: `-${b.blocks}`, color: 'var(--danger)' }));
    }

    // Sort by exact millisecond timestamp descending
    hist.sort((a,b) => b.timestamp - a.timestamp);
    
    historyHtml = hist.slice(0, 30).map(h => {
        let clickAttr = '';
        if (h.clickType === 'pur') clickAttr = `onclick="openPurchaseDetails('${h.id}')" style="cursor:pointer;"`;
        if (h.clickType === 'sale') clickAttr = `onclick="openSaleDetails('${h.id}')" style="cursor:pointer;"`;
        
        let timeStr = '';
        if (h.timestamp) {
            const dt = new Date(h.timestamp);
            const time = dt.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
            timeStr = ' ' + time;
        }
        
        return `<div class="kv" ${clickAttr}><span>${h.date}${timeStr} · ${h.desc}</span><strong style="color:${h.color};">${h.qty}</strong></div>`;
    }).join('');

    main.innerHTML = `
        <button class="back-link" onclick="nav('dashboard')">${ico('back')} Back to Stock</button>
        <div class="page-title">${title}</div>
        
        <div style="text-align:center; padding: 20px 0 30px;">
            <p style="font-size:13px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; font-weight:700;">Current Stock</p>
            <p style="font-size:48px; font-weight:800; color:var(--brand); line-height:1;">${currentStock}</p>
        </div>
        
        <div class="row" style="margin-bottom:24px;">
            <button class="btn" style="margin-top:0; background:var(--brand); padding:16px; font-size:16px;" onclick="openAddStock('${type}', '${size}')">+ Add Stock</button>
            <button class="btn" style="margin-top:0; background:var(--danger); padding:16px; font-size:16px;" onclick="openSubtractStock('${type}', '${size}')">- Subtract</button>
        </div>
        
        <div class="section-title">${ico('bars')} Recent History</div>
        <div style="border:1px solid var(--line); border-radius:12px; padding:0 16px; margin-bottom:20px; background:var(--surface);">
            ${historyHtml || '<p style="font-size:13px; color:var(--muted); padding:16px 0; text-align:center;">No history yet.</p>'}
        </div>
    `;
}

'''
    js = js[:start] + new_func + js[end:]

with open('app.js', 'w') as f: f.write(js)
print("Sales bug fixed and Stock modals converted to full pages.")

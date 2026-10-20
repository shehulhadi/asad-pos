import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace renderDashboard completely
start = js.find('function renderDashboard(main) {')
end = js.find('function toggleSection(id) {')
if start != -1 and end != -1:
    new_dash = '''function renderDashboard(main) {
    const t = i18n[settings.lang];
    const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
    const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const cementAdj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
    const cementStock = cementPurchased - cementUsed + cementAdj;

    const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
    const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
    const sandAdj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
    const sandStock = sandPurchased - sandUsed + sandAdj;

    const sizes = ['4','6','9'];
    let blockStocks = {};
    sizes.forEach(sz => {
        const readyBatches = batches.filter(b => b.size === sz && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === sz).reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);
        blockStocks[sz] = produced - sold - broken + returned;
    });

    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockItem('${type}', '${size}')">
            <div class="k" style="font-size: 12px; font-weight:700;">${title}</div>
            <div class="n" style="font-size: 28px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 11px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="nav('debts')">${ico('debts')} Debts</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')">${ico('report')} Reports</button>` : ''}
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
        </div>
        <div class="page-title">Stock & Inventory</div>
        <div class="page-sub">Tap any item to manage stock and view history</div>

        <div class="card">
            <h3>${ico('box')} Raw Materials</h3>
            <div class="stock-grid">
                ${tile('Cement (Bags)', cementStock, 'cement', '')}
                ${tile('Sand (Bags)', sandStock, 'sand', '')}
            </div>
        </div>

        <div class="card">
            <h3>${ico('production')} Finished Blocks</h3>
            <div class="stock-grid">
                ${tile('4" Blocks', blockStocks['4'], 'block', '4')}
                ${tile('6" Blocks', blockStocks['6'], 'block', '6')}
                ${tile('9" Blocks', blockStocks['9'], 'block', '9')}
            </div>
        </div>
    `;
}

function openStockItem(type, size) {
    let title = '';
    let currentStock = 0;
    let historyHtml = '';
    let hist = [];

    if (type === 'cement' || type === 'sand') {
        title = type === 'cement' ? 'Cement' : 'Sand';
        if (type === 'cement') {
            const purchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        } else {
            const purchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.sandQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        }

        purchases.filter(p=>p.material===type).forEach(p => hist.push({ id: p.id, clickType: 'pur', date: p.date, desc: `Purchase from ${p.supplierName}`, qty: `+${p.qty}`, color: 'var(--brand)' }));
        stockAdjustments.filter(a=>a.material===type).forEach(a => hist.push({ date: a.date, desc: `Adjustment: ${a.reason}`, qty: a.qty > 0 ? `+${a.qty}` : `${a.qty}`, color: a.qty > 0 ? 'var(--brand)' : 'var(--danger)' }));
        batches.forEach(b => {
            if(type === 'cement' && b.cementBags > 0) hist.push({ date: b.date, desc: `Used in ${b.size}" batch`, qty: `-${b.cementBags}`, color: 'var(--danger)' });
            if(type === 'sand' && b.sandQty > 0) hist.push({ date: b.date, desc: `Used in ${b.size}" batch`, qty: `-${b.sandQty}`, color: 'var(--danger)' });
        });

    } else {
        title = size + '" Blocks';
        const readyBatches = batches.filter(b => b.size === size && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === size).reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === size).reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === size).reduce((s, r) => s + r.quantity, 0);
        currentStock = produced - sold - broken + returned;

        readyBatches.forEach(b => hist.push({ date: b.date, desc: `Produced (${b.worker})`, qty: `+${b.blocksProduced}`, color: 'var(--brand)' }));
        sales.filter(s=>s.size===size).forEach(s => hist.push({ id: s.id, clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.quantity}`, color: 'var(--danger)' }));
        breakagesLog.filter(b=>b.size===size).forEach(b => hist.push({ date: b.date, desc: `Breakage: ${b.reason}`, qty: `-${b.blocks}`, color: 'var(--danger)' }));
    }

    hist.sort((a,b) => new Date(b.date) - new Date(a.date));
    
    historyHtml = hist.slice(0, 20).map(h => {
        let clickAttr = '';
        if (h.clickType === 'pur') clickAttr = `onclick="openPurchaseDetails('${h.id}')" style="cursor:pointer;"`;
        if (h.clickType === 'sale') clickAttr = `onclick="openSaleDetails('${h.id}')" style="cursor:pointer;"`;
        return `<div class="kv" ${clickAttr}><span>${h.date} · ${h.desc}</span><strong style="color:${h.color};">${h.qty}</strong></div>`;
    }).join('');

    document.getElementById('modal-body').innerHTML = `
        <h3>${title}</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted);">Current Stock</p>
            <p style="font-size:36px; font-weight:800; color:var(--brand);">${currentStock}</p>
        </div>
        
        <div class="row" style="margin-bottom:16px;">
            <button class="btn" style="margin-top:0; background:var(--brand);" onclick="openAddStock('${type}', '${size}')">+ Add Stock</button>
            <button class="btn" style="margin-top:0; background:var(--danger);" onclick="openSubtractStock('${type}', '${size}')">- Subtract</button>
        </div>
        
        <div class="eyebrow">Recent History</div>
        <div style="max-height: 250px; overflow-y:auto; border:1px solid var(--line); border-radius:8px; padding:0 12px; margin-bottom:16px;">
            ${historyHtml || '<p style="font-size:13px; color:var(--muted); padding:12px 0;">No history yet.</p>'}
        </div>
        
        <button class="btn btn-outline" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function openAddStock(type, size) {
    closeModal();
    if (type === 'cement' || type === 'sand') {
        openPurchase();
        setTimeout(() => {
            if(document.getElementById('pur-mat')) {
                document.getElementById('pur-mat').value = type;
                document.getElementById('pur-qty').focus();
            }
        }, 100);
    } else {
        nav('production');
        setTimeout(() => {
            if(document.getElementById('p-size')) {
                document.getElementById('p-size').value = size;
                document.getElementById('p-blocks').focus();
            }
        }, 100);
    }
}

function openSubtractStock(type, size) {
    closeModal();
    if (type === 'cement' || type === 'sand') {
        openAdjustStock();
        setTimeout(() => {
            if(document.getElementById('adj-mat')) {
                document.getElementById('adj-mat').value = type;
                document.getElementById('adj-qty').focus();
            }
        }, 100);
    } else {
        openBreakage(size);
    }
}

'''
    js = js[:start] + new_dash + js[end:]

with open('app.js', 'w') as f: f.write(js)

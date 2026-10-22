import re
with open('app.js', 'r') as f: js = f.read()

# 1. Locate and replace the entire openStockItem function
start = js.find('function openStockItem(type, size) {')
end = js.find('function openAddStock(type, size) {')

if start != -1 and end != -1:
    new_func = '''function openStockItem(type, size) {
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

'''
    js = js[:start] + new_func + js[end:]

with open('app.js', 'w') as f: f.write(js)
print("History sorting fixed using precise timestamps.")

import re
with open('app.js', 'r') as f: js = f.read()

# ==========================================
# 1. TRANSLATIONS
# ==========================================
js = js.replace('cement: "Cement", sand: "Sand"', 'cement: "Cement", sand: "Sand", empty_bag: "Empty Bags"')
js = js.replace('cement: "Siminti", sand: "Yashi"', 'cement: "Siminti", sand: "Yashi", empty_bag: "Buhu Wofi"')

# ==========================================
# 2. REMOVE 4 & 9 INCH BLOCKS
# ==========================================
js = js.replace("<option value=\"4\">4\"</option><option value=\"6\">6\"</option><option value=\"9\">9\"</option>", "<option value=\"6\">6\"</option>")
js = js.replace("const sizes = ['4','6','9'];", "const sizes = ['6'];")
js = js.replace("['4', '6', '9']", "['6']")
js = js.replace("sizeTotals = { '4': 0, '6': 0, '9': 0 }", "sizeTotals = { '6': 0 }")

# Update custom edit select for 6" only
js = re.sub(r'<select id="edit-s-size">.*?</select>', '<select id="edit-s-size"><option value="6">6"</option></select>', js)
js = re.sub(r'<select id="edit-b-size">.*?</select>', '<select id="edit-b-size"><option value="6">6"</option></select>', js)

# ==========================================
# 3. UPDATE STOCK PAGE (renderDashboard)
# ==========================================
start_dash = js.find('function renderDashboard(main) {')
end_dash = js.find('function openStockItem(type, size) {')
if start_dash != -1 and end_dash != -1:
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

    const emptyBagsProduced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const emptyBagsSold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
    const emptyBagsAdj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
    const emptyBagsStock = emptyBagsProduced - emptyBagsSold + emptyBagsAdj;

    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
    const sold = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
    const broken = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
    const returned = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
    const blockStock = produced - sold - broken + returned;

    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockItem('${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight:700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
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
            <div class="stock-grid" style="grid-template-columns: repeat(3, 1fr);">
                ${tile('Cement', cementStock, 'cement', '')}
                ${tile('Sand', sandStock, 'sand', '')}
                ${tile('Empty Bags', emptyBagsStock, 'empty_bag', '')}
            </div>
        </div>

        <div class="card">
            <h3>${ico('production')} Finished Blocks</h3>
            <div class="stock-grid">
                ${tile('6" Blocks', blockStock, 'block', '6')}
            </div>
        </div>
    `;
}

'''
    js = js[:start_dash] + new_dash + js[end_dash:]

# ==========================================
# 4. UPDATE openStockItem
# ==========================================
start_item = js.find('function openStockItem(type, size) {')
end_item = js.find('function openAddStock(type, size) {')
if start_item != -1 and end_item != -1:
    new_item = '''function openStockItem(type, size) {
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
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const sold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
            currentStock = produced - sold + adj;
        }

        purchases.filter(p=>p.material===type).forEach(p => hist.push({ id: p.id, clickType: 'pur', date: p.date, desc: `Purchase from ${p.supplierName}`, qty: `+${p.qty}`, color: 'var(--brand)' }));
        stockAdjustments.filter(a=>a.material===type).forEach(a => hist.push({ date: a.date, desc: `Adjustment: ${a.reason}`, qty: a.qty > 0 ? `+${a.qty}` : `${a.qty}`, color: a.qty > 0 ? 'var(--brand)' : 'var(--danger)' }));
        
        if(type === 'empty_bag') {
            batches.forEach(b => { if(b.cementBags > 0) hist.push({ date: b.date, desc: `Generated from cement usage`, qty: `+${b.cementBags}`, color: 'var(--brand)' }); });
            sales.forEach(s => { if(s.emptyBagQty > 0) hist.push({ id: s.id, clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.emptyBagQty}`, color: 'var(--danger)' }); });
        } else {
            batches.forEach(b => {
                if(type === 'cement' && b.cementBags > 0) hist.push({ date: b.date, desc: `Used in 6" batch`, qty: `-${b.cementBags}`, color: 'var(--danger)' });
                if(type === 'sand' && b.sandQty > 0) hist.push({ date: b.date, desc: `Used in 6" batch`, qty: `-${b.sandQty}`, color: 'var(--danger)' });
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

        readyBatches.forEach(b => hist.push({ date: b.date, desc: `Produced (${b.worker})`, qty: `+${b.blocksProduced}`, color: 'var(--brand)' }));
        sales.filter(s=>s.size==='6').forEach(s => hist.push({ id: s.id, clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.quantity}`, color: 'var(--danger)' }));
        breakagesLog.filter(b=>b.size==='6').forEach(b => hist.push({ date: b.date, desc: `Breakage: ${b.reason}`, qty: `-${b.blocks}`, color: 'var(--danger)' }));
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

'''
    js = js[:start_item] + new_item + js[end_item:]

# ==========================================
# 5. UPDATE openAddStock & openSubtractStock
# ==========================================
js = js.replace("if (type === 'cement' || type === 'sand') {", "if (type === 'cement' || type === 'sand' || type === 'empty_bag') {")

# ==========================================
# 6. UPDATE FORMS (Dropdowns & Fields)
# ==========================================
# Add empty_bag to Purchase & Adjust dropdowns
js = js.replace('<select id="pur-mat"><option value="cement">${t.cement}</option><option value="sand">${t.sand}</option></select>', '<select id="pur-mat"><option value="cement">${t.cement}</option><option value="sand">${t.sand}</option><option value="empty_bag">${t.empty_bag}</option></select>')
js = js.replace('<select id="adj-mat"><option value="cement">Cement</option><option value="sand">Sand</option></select>', '<select id="adj-mat"><option value="cement">Cement</option><option value="sand">Sand</option><option value="empty_bag">Empty Bags</option></select>')
js = js.replace('<select id="edit-p-mat"><option value="cement" ${p.material===\'cement\'?\'selected\':\'\'}>Cement</option><option value="sand" ${p.material===\'sand\'?\'selected\':\'\'}>Sand</option></select>', '<select id="edit-p-mat"><option value="cement" ${p.material===\'cement\'?\'selected\':\'\'}>Cement</option><option value="sand" ${p.material===\'sand\'?\'selected\':\'\'}>Sand</option><option value="empty_bag" ${p.material===\'empty_bag\'?\'selected\':\'\'}>Empty Bags</option></select>')

# Add Empty Bags to Sales Form
old_sales_forms = '''<div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>'''
new_sales_forms = '''<div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Empty Bags Qty</label><input type="number" id="s-empty-bag-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Empty Bag Price (₦)</label><input type="number" id="s-empty-bag-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>'''
js = js.replace(old_sales_forms, new_sales_forms)

# Add Empty Bags to Edit Sale Form
old_edit_forms = '''<div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>'''
new_edit_forms = '''<div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Empty Bags Qty</label><input type="number" id="edit-s-empty-bag-qty" value="${s.emptyBagQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Empty Bag Price (₦)</label><input type="number" id="edit-s-empty-bag-price" value="${s.emptyBagPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>'''
js = js.replace(old_edit_forms, new_edit_forms)

# ==========================================
# 7. CALCULATIONS & SAVING
# ==========================================
# calcSale
js = js.replace("const sQty = parseFloat(document.getElementById('s-sand-qty').value) || 0;", "const sQty = parseFloat(document.getElementById('s-sand-qty').value) || 0;\n    const eQty = parseFloat(document.getElementById('s-empty-bag-qty').value) || 0;\n    const ePrice = parseFloat(document.getElementById('s-empty-bag-price').value) || 0;")
js = js.replace("const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + delivery;", "const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;")

# calcEditSale
js = js.replace("const sQty = parseFloat(document.getElementById('edit-s-sand-qty').value) || 0;", "const sQty = parseFloat(document.getElementById('edit-s-sand-qty').value) || 0;\n    const eQty = parseFloat(document.getElementById('edit-s-empty-bag-qty').value) || 0;\n    const ePrice = parseFloat(document.getElementById('edit-s-empty-bag-price').value) || 0;")
js = js.replace("const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + delivery;", "const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;")

# executeSaveSale
js = js.replace("const sQty = parseInt(document.getElementById('s-sand-qty').value) || 0;", "const sQty = parseInt(document.getElementById('s-sand-qty').value) || 0;\n        const eQty = parseInt(document.getElementById('s-empty-bag-qty').value) || 0;\n        const ePrice = parseFloat(document.getElementById('s-empty-bag-price').value) || 0;")
js = js.replace("const total = (qty * price) + (cQty * cPrice) + (sQty * sPrice) + delivery;", "const total = (qty * price) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;")
js = js.replace("sandPrice: sPrice,", "sandPrice: sPrice,\n            emptyBagQty: eQty,\n            emptyBagPrice: ePrice,")
js = js.replace("if (sQty > 0) itemsHtml += `<div class=\"kv\"><span>${sQty} bags of Sand</span><strong>${formatNaira(sQty * sPrice)}</strong></div>`;", "if (sQty > 0) itemsHtml += `<div class=\"kv\"><span>${sQty} bags of Sand</span><strong>${formatNaira(sQty * sPrice)}</strong></div>`;\n        if (eQty > 0) itemsHtml += `<div class=\"kv\"><span>${eQty} Empty Bags</span><strong>${formatNaira(eQty * ePrice)}</strong></div>`;")

# saveEditedSale
js = js.replace("s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;", "s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;\n    s.emptyBagQty = parseInt(document.getElementById('edit-s-empty-bag-qty').value) || 0;\n    s.emptyBagPrice = parseFloat(document.getElementById('edit-s-empty-bag-price').value) || 0;")
js = js.replace("s.totalAmount = (s.quantity * s.pricePerBlock) + (s.cementQty * s.cementPrice) + (s.sandQty * s.sandPrice) + s.deliveryCharge;", "s.totalAmount = (s.quantity * s.pricePerBlock) + (s.cementQty * s.cementPrice) + (s.sandQty * s.sandPrice) + (s.emptyBagQty * s.emptyBagPrice) + s.deliveryCharge;")

# Receipts & WhatsApp
js = js.replace("if (sale.sandQty > 0) itemsText += `- ${sale.sandQty} bags of Sand @ ₦${sale.sandPrice.toLocaleString()}\\n`;", "if (sale.sandQty > 0) itemsText += `- ${sale.sandQty} bags of Sand @ ₦${sale.sandPrice.toLocaleString()}\\n`;\n    if (sale.emptyBagQty > 0) itemsText += `- ${sale.emptyBagQty} Empty Bags @ ₦${sale.emptyBagPrice.toLocaleString()}\\n`;")
js = js.replace("if (s.sandQty > 0) itemsHtml += `<div class=\"kv\"><span>${s.sandQty} bags of Sand</span><strong>${formatNaira(s.sandQty * s.sandPrice)}</strong></div>`;", "if (s.sandQty > 0) itemsHtml += `<div class=\"kv\"><span>${s.sandQty} bags of Sand</span><strong>${formatNaira(s.sandQty * s.sandPrice)}</strong></div>`;\n    if (s.emptyBagQty > 0) itemsHtml += `<div class=\"kv\"><span>${s.emptyBagQty} Empty Bags</span><strong>${formatNaira(s.emptyBagQty * s.emptyBagPrice)}</strong></div>`;")

with open('app.js', 'w') as f: f.write(js)

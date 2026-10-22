import re
with open('app.js', 'r') as f: js = f.read()

# 1. Remove 'Mark Ready' from Production
js = js.replace("status: 'curing'", "status: 'ready'")
js = js.replace('${isCuring ? `<div class="actions"><button onclick="markReady(\'${b.id}\')">${t.markReady}</button></div>` : \'\'}', '')
js = js.replace('<span class="tag ${isCuring ? \'blue\' : \'green\'}">${isCuring ? t.curing : t.ready}</span>', '<span class="tag green">Ready</span>')

# 2. Remove 'Mark Delivered' from Sales
js = js.replace('${s.deliveryStatus === \'delivered\' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending</span>`}', '')
js = re.sub(r'<button class="btn \$\{s\.deliveryStatus === \'delivered\' \? \'btn-outline\' : \'btn-dark\'\}".*?onclick="toggleDelivery\(\'\$\{s\.id\}\'\)">.*?</button>', '', js, flags=re.DOTALL)
js = re.sub(r'function toggleDelivery\(id\) \{.*?\n\}', '', js, flags=re.DOTALL)

# 3. Fix Analytics Calculations (COGS & Stock Value)
old_ana_calc = '''    const totalReturnsAmount = returns.reduce((sum, r) => sum + (r.refundAmount || 0), 0);
    const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0) - totalReturnsAmount;
    const allCOGS = sales.reduce((sum, s) => sum + (s.quantity * getAvgCost(s.size)), 0);'''

new_ana_calc = '''    const totalReturnsAmount = returns.reduce((sum, r) => sum + (r.refundAmount || 0), 0);
    const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0) - totalReturnsAmount;

    // Calculate Average Costs for Raw Materials
    let totalCementBags = 0, totalCementCost = 0;
    purchases.filter(p=>p.material==='cement').forEach(p => { totalCementBags += p.qty; totalCementCost += p.cost; });
    const avgCementCost = totalCementBags > 0 ? totalCementCost / totalCementBags : 0;

    let totalSandBags = 0, totalSandCost = 0;
    purchases.filter(p=>p.material==='sand').forEach(p => { totalSandBags += p.qty; totalSandCost += p.cost; });
    const avgSandCost = totalSandBags > 0 ? totalSandCost / totalSandBags : 0;

    let totalEmptyBags = 0, totalEmptyBagCost = 0;
    purchases.filter(p=>p.material==='empty_bag').forEach(p => { totalEmptyBags += p.qty; totalEmptyBagCost += p.cost; });
    const avgEmptyBagCost = totalEmptyBags > 0 ? totalEmptyBagCost / totalEmptyBags : 0;

    const blockCOGS = sales.reduce((sum, s) => sum + ((s.quantity || 0) * getAvgCost(s.size)), 0);
    const cementCOGS = sales.reduce((sum, s) => sum + ((s.cementQty || 0) * avgCementCost), 0);
    const sandCOGS = sales.reduce((sum, s) => sum + ((s.sandQty || 0) * avgSandCost), 0);
    const emptyBagCOGS = sales.reduce((sum, s) => sum + ((s.emptyBagQty || 0) * avgEmptyBagCost), 0);
    const allCOGS = blockCOGS + cementCOGS + sandCOGS + emptyBagCOGS;'''
js = js.replace(old_ana_calc, new_ana_calc)

old_stock_val = '''    let unsoldValue = 0;
    ['4', '6', '9'].forEach(sz => {
        const readyBatches = batches.filter(b => b.size === sz && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === sz).reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);
        const remaining = Math.max(0, produced - sold - broken + returned);
        unsoldValue += remaining * getAvgCost(sz);
    });'''

new_stock_val = '''    let unsoldValue = 0;
    
    // Blocks Value
    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const producedBlocks = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
    const soldBlocks = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
    const brokenBlocks = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
    const returnedBlocks = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
    const remainingBlocks = Math.max(0, producedBlocks - soldBlocks - brokenBlocks + returnedBlocks);
    unsoldValue += remainingBlocks * getAvgCost('6');

    // Cement Value
    const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
    const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const cementAdj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
    const cementStock = Math.max(0, cementPurchased - cementUsed + cementAdj);
    unsoldValue += cementStock * avgCementCost;

    // Sand Value
    const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
    const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
    const sandAdj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
    const sandStock = Math.max(0, sandPurchased - sandUsed + sandAdj);
    unsoldValue += sandStock * avgSandCost;

    // Empty Bags Value
    const ebPurchased = purchases.filter(p=>p.material==='empty_bag').reduce((s,p)=>s+p.qty,0);
    const ebProduced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const ebSold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
    const ebAdj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
    const ebStock = Math.max(0, ebPurchased + ebProduced - ebSold + ebAdj);
    unsoldValue += ebStock * avgEmptyBagCost;'''
js = js.replace(old_stock_val, new_stock_val)

# 4. Restructure renderSales to use Modal
start_sales = js.find('function renderSales(main) {')
end_sales = js.find('function updateDefaultPrice() {')
if start_sales != -1 and end_sales != -1:
    new_sales = '''function renderSales(main) { 
    const t = i18n[settings.lang];
    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 15);
    recentSales.forEach(s => {
        historyHtml += `<div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')"><div class="list-header"><span>${s.customerName}</span><strong class="pos">${formatNaira(s.totalAmount)}</strong></div><div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:4px;">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}</div>`;
    });

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="openSaleModal()" style="background:var(--brand); color:#fff; border:none; padding:14px; font-size:15px; border-radius:8px; font-weight:700; width:100%; box-shadow:0 4px 12px rgba(16,185,129,0.3);">+ New Sale</button>
        </div>
        <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;"><span>${ico('sales')} ${t.salesHistory}</span></div>
        <div class="form-group" style="margin-bottom:12px;"><input type="text" id="search-sales" placeholder="Search by customer name or date..." oninput="filterSales(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;"></div>
        <div id="sales-history-list">${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}</div>
    `;
}

function openSaleModal() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${ico('plus')} ${t.newSale}</h3>
        <div class="eyebrow">Customer Info</div>
        <div class="form-group"><label>${t.customer}</label><input type="text" id="s-customer" list="customer-names" placeholder="Name" oninput="autofillPhone(this.value)"><datalist id="customer-names"></datalist></div>
        <div class="row">
            <div class="form-group"><label>${t.phone}</label><input type="tel" id="s-phone" placeholder="Phone"></div>
            <div class="form-group"><label>${t.date}</label><input type="date" id="s-date" value="${getTodayStr()}"></div>
        </div>

        <div class="eyebrow">Items Bought</div>
        <div style="background:var(--bg); padding:12px; border-radius:8px; margin-bottom:12px;">
            <div style="font-weight:700; font-size:13px; margin-bottom:8px;">Blocks</div>
            <div class="row">
                <div class="form-group" style="flex:1.5;"><label>${t.size}</label><select id="s-size" onchange="updateDefaultPrice()"><option value="6">6"</option></select></div>
                <div class="form-group" style="flex:1;"><label>Qty</label><input type="number" id="s-qty" value="" placeholder="0" oninput="calcSale()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 50, 'calcSale')">+50</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 100, 'calcSale')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 500, 'calcSale')">+500</button></div></div>
                <div class="form-group" style="flex:1.5;"><label>Price (₦)</label><input type="number" id="s-price" value="" placeholder="0" oninput="calcSale()"></div>
            </div>
        </div>

        <div class="row">
            <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="s-cement-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="s-cement-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Empty Bags Qty</label><input type="number" id="s-empty-bag-qty" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>Empty Bag Price (₦)</label><input type="number" id="s-empty-bag-price" value="" placeholder="0" oninput="calcSale()"></div>
        </div>

        <div class="eyebrow">Payment</div>
        <div class="row">
            <div class="form-group"><label>${t.delivery}</label><input type="number" id="s-delivery" value="" placeholder="0" oninput="calcSale()"></div>
            <div class="form-group"><label>${t.paid}</label><input type="number" id="s-paid" value="" placeholder="0" oninput="calcSale()"></div>
        </div>
        <div class="calc-box">
            <div class="line"><span>Total Amount</span> <span>₦<span id="s-total-display">0</span></span></div>
            <div class="line" style="color:var(--danger);"><span>${t.balance}</span> <span>₦<span id="s-balance-display">0</span></span></div>
        </div>
        
        <button class="btn" style="margin-top:0;" onclick="saveSale()">${t.save}</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    const uniqueCustomers = {};
    sales.forEach(s => { if(s.customerName && s.customerPhone) uniqueCustomers[s.customerName] = s.customerPhone; });
    document.getElementById('customer-names').innerHTML = Object.keys(uniqueCustomers).map(name => `<option value="${name}"></option>`).join('');
    document.getElementById('modal').classList.add('active');
    calcSale();
}

'''
    js = js[:start_sales] + new_sales + js[end_sales:]

# 5. Restructure renderProduction to use Modal
start_prod = js.find('function renderProduction(main) {')
end_prod = js.find('function autoFillMaterials() {')
if start_prod != -1 and end_prod != -1:
    new_prod = '''function renderProduction(main) { 
    const t = i18n[settings.lang]; 
    let listHtml = ''; 
    const recent = [...batches].reverse().slice(0, 15);
    recent.forEach(b => {
        listHtml += `<div class="list-item" style="cursor:pointer;" onclick="openBatchDetails('${b.id}')"><div class="list-header"><span>${b.size}" Blocks · ${b.blocksProduced} pcs</span><span class="pos">${formatNaira(b.costPerBlock)}<small style="color:var(--muted); font-weight:600;">/block</small></span></div><div class="list-sub">${b.worker} · ${b.date}</div><span class="tag green">Ready</span></div>`;
    });
    
    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px;">
            <button onclick="openProductionModal()" style="background:var(--blue); color:#fff; border:none; padding:14px; font-size:15px; border-radius:8px; font-weight:700; width:100%; box-shadow:0 4px 12px rgba(37,99,235,0.3);">+ New Batch</button>
        </div>
        <div class="section-title">${ico('bars')} Recent Batches</div>
        ${listHtml || '<div class="empty">No batches logged yet.</div>'}
    `;
}

function openProductionModal() {
    const t = i18n[settings.lang]; const today = getTodayStr();
    document.getElementById('modal-body').innerHTML = `
        <h3>${ico('production')} ${t.newBatch}</h3>
        <div class="row">
            <div class="form-group"><label>Date</label><input type="date" id="p-date" value="${today}"></div>
            <div class="form-group"><label>${t.size}</label><select id="p-size"><option value="6">6"</option></select></div>
        </div>
        <div class="row">
            <div class="form-group"><label>${t.worker}</label><input type="text" id="p-worker" list="worker-names" placeholder="Worker name"><datalist id="worker-names"></datalist></div>
            <div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="" placeholder="0" oninput="calcBatchCost()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 100, 'calcBatchCost')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 500, 'calcBatchCost')">+500</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 1000, 'calcBatchCost')">+1000</button><button type="button" class="btn" style="padding:6px; font-size:12px; margin:0; background:var(--accent); color:#fff; border:none;" onclick="autoFillMaterials()">⚡ Auto-Fill Mix</button></div></div>
        </div>
        
        <div class="eyebrow">Materials Used</div>
        <div class="row">
            <div class="form-group"><label>${t.cementBags}</label><input type="number" id="p-cement-bags" value="" placeholder="0" oninput="calcBatchCost()"></div>
            <div class="form-group"><label>${t.costPerBag}</label><input type="number" id="p-cement-cost" value="" placeholder="0" oninput="calcBatchCost()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>${t.sandCost}</label><input type="number" id="p-sand-cost" value="" placeholder="0" oninput="calcBatchCost()"></div>
            <div class="form-group"><label>${t.sandQty}</label><input type="number" id="p-sand-qty" value="" placeholder="0"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>${t.labourCost}</label><input type="number" id="p-labour-cost" value="" placeholder="0" oninput="calcBatchCost()"></div>
            <div class="form-group"><label>${t.otherCost}</label><input type="number" id="p-other-cost" value="" placeholder="0" oninput="calcBatchCost()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>${t.breakages}</label><input type="number" id="p-breakages" value="" placeholder="0"></div>
            <div class="form-group"><label>${t.curingLoss}</label><input type="number" id="p-curing-loss" value="" placeholder="0"></div>
        </div>
        
        <div class="calc-box"><div class="line"><span>${t.totalCost}</span> <span>₦<span id="p-total-display">0</span></span></div><div class="line pos"><span>${t.costPerBlock}</span> <span>₦<span id="p-cpb-display">0.00</span></span></div></div>
        
        <button class="btn btn-blue" style="margin-top:0;" onclick="saveBatch()">${t.saveBatch}</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    const uniqueWorkers = [...new Set(batches.map(b => b.worker).filter(w => w && w !== 'Unknown' && w !== 'System Adjustment'))];
    document.getElementById('worker-names').innerHTML = uniqueWorkers.map(w => `<option value="${w}"></option>`).join('');
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start_prod] + new_prod + js[end_prod:]

# Ensure saveSale and saveBatch close modal and refresh page
js = js.replace("document.getElementById('modal').classList.add('active');\n    } catch (e) { showToast(\"Error: \" + e.message, \"err\"); }\n}", "document.getElementById('modal').classList.add('active');\n    } catch (e) { showToast(\"Error: \" + e.message, \"err\"); }\n}")
# Update saveBatch to close modal and refresh
js = js.replace("batches.push(batch); saveData('batches', batches); nav('production'); showToast('Production batch saved', 'success');", "batches.push(batch); saveData('batches', batches); closeModal(); nav('production'); showToast('Production batch saved', 'success');")

with open('app.js', 'w') as f: f.write(js)
print("All changes applied successfully.")

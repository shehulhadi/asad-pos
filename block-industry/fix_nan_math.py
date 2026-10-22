import re
with open('app.js', 'r') as f: js = f.read()

# 1. Fix getAvgCost to prevent NaN
old_cost = '''function getAvgCost(size) {
    const sizeBatches = batches.filter(b => b.size === size);
    if (sizeBatches.length === 0) return 0;
    const totalCost = sizeBatches.reduce((sum, b) => sum + b.totalCost, 0);
    const totalBlocks = sizeBatches.reduce((sum, b) => sum + b.blocksProduced, 0);
    return totalBlocks > 0 ? (totalCost / totalBlocks) : 0;
}'''
new_cost = '''function getAvgCost(size) {
    const sizeBatches = batches.filter(b => b.size === size);
    if (sizeBatches.length === 0) return 0;
    const totalCost = sizeBatches.reduce((sum, b) => sum + (Number(b.totalCost) || 0), 0);
    const totalBlocks = sizeBatches.reduce((sum, b) => sum + (Number(b.blocksProduced) || 0), 0);
    return totalBlocks > 0 ? (totalCost / totalBlocks) : 0;
}'''
js = js.replace(old_cost, new_cost)

# 2. Rewrite renderAnalytics with full Number() safety
start_ana = js.find('function renderAnalytics(main) {')
end_ana = js.find('function toggleAlerts() {')

if start_ana != -1 and end_ana != -1:
    new_ana = '''function renderAnalytics(main) {
    if (currentUser !== 'owner') return nav('dashboard');
    const t = i18n[settings.lang];
    const today = getWATDate();
    const todayStr = getTodayStr();

    // --- SAFE MATH HELPER ---
    const N = (val) => Number(val) || 0;

    // --- RAW STOCK & AVG COST ---
    const getStockAndCost = (material) => {
        const items = purchases.filter(p => p.material === material);
        const totalQty = items.reduce((s,p)=>s+N(p.qty),0);
        const totalCost = items.reduce((s,p)=>s+N(p.cost),0);
        const avgCost = totalQty > 0 ? totalCost / totalQty : 0;
        
        const purchased = totalQty;
        let used = 0;
        if (material === 'empty_bag') used = sales.reduce((s,v)=>s+N(v.emptyBagQty),0);
        else if (material === 'cement') used = batches.reduce((s,b)=>s+N(b.cementBags),0);
        else if (material === 'sand') used = batches.reduce((s,b)=>s+N(b.sandQty),0);
        
        const adj = stockAdjustments.filter(a=>a.material===material).reduce((s,a)=>s+N(a.qty),0);
        
        let currentStock = 0;
        if (material === 'empty_bag') {
            const produced = batches.reduce((s,b)=>s+N(b.cementBags),0);
            currentStock = purchased + produced - used + adj;
        } else {
            currentStock = purchased - used + adj;
        }
        return { stock: Math.max(0, currentStock), cost: avgCost };
    };

    const cementData = getStockAndCost('cement');
    const sandData = getStockAndCost('sand');
    const ebData = getStockAndCost('empty_bag');

    // --- REVENUE & COGS ---
    const totalReturnsAmount = returns.reduce((sum, r) => sum + N(r.refundAmount), 0);
    const allRevenue = sales.reduce((sum, s) => sum + N(s.totalAmount), 0) - totalReturnsAmount;

    let allCOGS = 0;
    sales.forEach(s => {
        allCOGS += N(s.quantity) * getAvgCost(s.size);
        allCOGS += N(s.cementQty) * cementData.cost;
        allCOGS += N(s.sandQty) * sandData.cost;
        allCOGS += N(s.emptyBagQty) * ebData.cost;
    });

    const allExpenses = expenses.reduce((sum, e) => sum + N(e.amount), 0);
    const netProfit = allRevenue - allCOGS - allExpenses;

    // --- CASH IN HAND ---
    const cashFromSales = sales.reduce((sum, s) => sum + N(s.amountPaidAtSale), 0) + payments.reduce((sum, p) => sum + N(p.amount), 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + N(p.amountPaid), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash;

    // --- DEBTS ---
    const moneyOwedToOwner = sales.filter(s => !s.writtenOff).reduce((sum, s) => sum + N(s.balanceOwing), 0);
    const moneyYouOwe = purchases.reduce((sum, p) => sum + Math.max(0, N(p.cost) - N(p.amountPaid)), 0);

    // --- STOCK VALUE ---
    let unsoldValue = 0;
    
    // Blocks Value
    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const producedBlocks = readyBatches.reduce((s,b)=>s+(N(b.blocksProduced) - N(b.breakages)),0);
    const soldBlocks = sales.filter(s => s.size === '6').reduce((s,v)=>s+N(v.quantity),0);
    const brokenBlocks = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+N(v.blocks),0);
    const returnedBlocks = returns.filter(r => r.size === '6').reduce((s, r) => s + N(r.quantity), 0);
    const remainingBlocks = Math.max(0, producedBlocks - soldBlocks - brokenBlocks + returnedBlocks);
    
    unsoldValue += remainingBlocks * getAvgCost('6');
    
    // Raw Materials Value
    unsoldValue += cementData.stock * cementData.cost;
    unsoldValue += sandData.stock * sandData.cost;
    unsoldValue += ebData.stock * ebData.cost;

    // --- CHART DATA ---
    const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + N(s.totalAmount), 0);
    const weekAgoStr = new Date(today.getTime() - 7*24*60*60*1000).toISOString().split('T')[0];
    const weekRev = sales.filter(s => s.date >= weekAgoStr).reduce((sum, s) => sum + N(s.totalAmount), 0);

    let chartHtml = ''; let maxDayRev = 0; const days = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date(today.getTime() - i*24*60*60*1000);
        const dStr = d.toISOString().split('T')[0];
        const rev = sales.filter(s => s.date === dStr).reduce((sum, s) => sum + N(s.totalAmount), 0);
        if (rev > maxDayRev) maxDayRev = rev;
        days.push({ date: dStr, day: d.toLocaleDateString('en-US', {weekday:'short'}), rev: rev });
    }
    days.forEach(d => {
        const pct = maxDayRev > 0 ? (d.rev / maxDayRev) * 100 : 0;
        chartHtml += `<div class="chart-bar" style="height:${pct}%;" title="${formatNaira(d.rev)}"><div class="chart-label">${d.day}</div></div>`;
    });

    // --- LISTS ---
    const sizeTotals = { '6': 0 };
    sales.forEach(s => { if(sizeTotals[s.size] !== undefined) sizeTotals[s.size] += N(s.quantity); });
    let bestSizeHtml = '';
    Object.keys(sizeTotals).forEach(size => {
        if (sizeTotals[size] > 0) bestSizeHtml += `<div class="kv"><span>${size}" Blocks</span><strong>${sizeTotals[size].toLocaleString()} pcs</strong></div>`;
    });

    const custTotals = {};
    sales.forEach(s => { custTotals[s.customerName] = (custTotals[s.customerName] || 0) + N(s.totalAmount); });
    let topCustHtml = ''; let rk = 0;
    Object.entries(custTotals).sort((a,b)=>b[1]-a[1]).slice(0,3).forEach(([name, amt]) => {
        rk++;
        topCustHtml += `<div class="kv"><span><span class="rank">${rk}</span>${name}</span><strong>${formatNaira(amt)}</strong></div>`;
    });

    let marginAlertHtml = '';
    sales.forEach(s => {
        const avgCost = getAvgCost(s.size);
        const minPrice = avgCost * (1 + (N(settings.marginAlertPct)/100));
        if (N(s.pricePerBlock) < minPrice && avgCost > 0) {
            marginAlertHtml += `<div class="list-item alert"><div class="list-header"><span>${s.customerName}</span><span>${formatNaira(s.pricePerBlock)}/block</span></div><div class="list-sub">${t.marginWarning} (Cost: ${formatNaira(avgCost)})</div></div>`;
        }
    });

    const totalQtySold = sales.reduce((sum, s) => sum + N(s.quantity), 0);
    const profitPerBlock = totalQtySold > 0 ? (allRevenue - allCOGS) / totalQtySold : 0;
    let breakEvenText = "Set fixed costs in Settings";
    if (N(settings.fixedCostsMonthly) > 0) breakEvenText = profitPerBlock > 0 ? Math.ceil(N(settings.fixedCostsMonthly) / profitPerBlock).toLocaleString() + " blocks/month" : "Log sales to calculate";

    let lowStockHtml = '';
    if (cementData.stock <= N(settings.lowCement)) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🪨 Cement</span><span>${cementData.stock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;
    if (sandData.stock <= N(settings.lowSand)) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🏖️ Sand</span><span>${sandData.stock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;

    let alertWrapper = '';
    if (lowStockHtml) {
        const isCollapsed = localStorage.getItem('asad:alertsCollapsed') === 'true';
        alertWrapper = `
            <div style="margin-bottom:16px;">
                <div class="section-title neg" onclick="toggleAlerts()" style="margin-top:0; margin-bottom:0; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:var(--danger-soft); padding:12px 16px; border-radius:12px; border:1px solid #f7bcbc;">
                    <span style="display:flex; align-items:center; gap:8px;">${ico('alert')} Low Stock Alerts</span>
                    <span id="alert-toggle-icon" style="font-size:12px;">${isCollapsed ? '▼' : '▲'}</span>
                </div>
                <div id="alert-list-container" style="display:${isCollapsed ? 'none' : 'block'}; margin-top:12px;">${lowStockHtml}</div>
            </div>
        `;
    }

    main.innerHTML = `
        <div class="quick">
            <button onclick="nav('dashboard')">${ico('box')} Stock</button>
            <button onclick="nav('reports')">${ico('report')} Reports</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
        </div>
        ${alertWrapper}
        <div class="hero">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="lbl">${t.netProfit}</div>
                    <div class="big ${netProfit < 0 ? 'neg' : ''}">${formatNaira(netProfit)}</div>
                </div>
                <div style="background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:20px; font-size:12px; font-weight:800; color:#f59e0b; display:flex; align-items:center; gap:4px;">🔥 ${settings.streak} Day Streak</div>
            </div>
            <div class="meta">
                <div>${t.revenue}<strong>${formatNaira(allRevenue)}</strong></div>
                <div>${t.expenses}<strong>${formatNaira(allExpenses)}</strong></div>
            </div>
        </div>
        <div class="dash-grid">
            <div class="stat"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand}</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>
            <div class="stat"><div class="top"><span class="dot a">${ico('arrowIn')}</span><h4>${t.moneyOwed}</h4></div><div class="val">${formatNaira(moneyOwedToOwner)}</div></div>
            <div class="stat"><div class="top"><span class="dot r">${ico('arrowOut')}</span><h4>${t.moneyYouOwe}</h4></div><div class="val ${moneyYouOwe > 0 ? 'neg' : ''}">${formatNaira(moneyYouOwe)}</div></div>
            <div class="stat"><div class="top"><span class="dot b">${ico('box')}</span><h4>${t.stockValue}</h4></div><div class="val">${formatNaira(unsoldValue)}</div></div>
        </div>
        <div class="card">
            <h3>${ico('bars')} ${t.turnover}</h3>
            <div class="periods">
                <div><small>Today</small><strong>${formatNaira(dayRev)}</strong></div>
                <div><small>This Week</small><strong>${formatNaira(weekRev)}</strong></div>
            </div>
            <div class="chart-container">${maxDayRev > 0 ? chartHtml : '<p style="font-size:13px; color:var(--muted); width:100%; text-align:center; align-self:center;">No sales data yet.</p>'}</div>
        </div>
        <div class="card"><h3>${ico('trophy')} ${t.bestSizes}</h3>${bestSizeHtml || '<p style="font-size:13px; color:var(--muted);">No data</p>'}</div>
        <div class="card"><h3>${ico('users')} ${t.topCustomers}</h3>${topCustHtml || '<p style="font-size:13px; color:var(--muted);">No data</p>'}</div>
        <div class="card breakeven">
            <h3>${ico('target')} Break-even (Monthly)</h3>
            <p style="font-size:13px; color:#94a3b8;">Based on fixed costs of <strong style="color:#fff;">${formatNaira(settings.fixedCostsMonthly)}</strong></p>
            <div style="font-size:24px; font-weight:800; margin-top:8px; color:#34d399; letter-spacing:-.5px;">${breakEvenText}</div>
        </div>
    `;
}

'''
    js = js[:start_ana] + new_ana + js[end_ana:]

with open('app.js', 'w') as f: f.write(js)
print("NaN errors permanently fixed.")

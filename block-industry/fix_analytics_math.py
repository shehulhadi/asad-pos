import re
with open('app.js', 'r') as f: js = f.read()

# 1. Locate renderAnalytics and replace it completely
start_ana = js.find('function renderAnalytics(main) {')
end_ana = js.find('function toggleAlerts() {')

if start_ana != -1 and end_ana != -1:
    new_ana = '''function renderAnalytics(main) {
    if (currentUser !== 'owner') return nav('dashboard');
    const t = i18n[settings.lang];
    const today = getWATDate();
    const todayStr = getTodayStr();
    const weekAgo = new Date(today.getTime() - 7*24*60*60*1000).toISOString().split('T')[0];
    const monthAgo = new Date(today.getTime() - 30*24*60*60*1000).toISOString().split('T')[0];

    // --- HELPER: Raw Stock & Avg Cost ---
    const getStockAndCost = (material) => {
        const items = purchases.filter(p => p.material === material);
        const totalQty = items.reduce((s,p)=>s+p.qty,0);
        const totalCost = items.reduce((s,p)=>s+p.cost,0);
        const avgCost = totalQty > 0 ? totalCost / totalQty : 0;
        
        const purchased = totalQty;
        const used = material === 'empty_bag' 
            ? sales.reduce((s,v)=>s+(v.emptyBagQty||0),0)
            : batches.reduce((s,b)=>s+(material==='cement'?b.cementBags:b.sandQty||0),0);
        const adj = stockAdjustments.filter(a=>a.material===material).reduce((s,a)=>s+a.qty,0);
        
        let currentStock = 0;
        if (material === 'empty_bag') {
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            currentStock = purchased + produced - used + adj;
        } else {
            currentStock = purchased - used + adj;
        }
        return { stock: Math.max(0, currentStock), cost: avgCost };
    };

    const cementData = getStockAndCost('cement');
    const sandData = getStockAndCost('sand');
    const ebData = getStockAndCost('empty_bag');

    // --- 1. REVENUE & COGS ---
    const totalReturnsAmount = returns.reduce((sum, r) => sum + (r.refundAmount || 0), 0);
    const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0) - totalReturnsAmount;

    let allCOGS = 0;
    sales.forEach(s => {
        allCOGS += (s.quantity || 0) * getAvgCost(s.size);
        allCOGS += (s.cementQty || 0) * cementData.cost;
        allCOGS += (s.sandQty || 0) * sandData.cost;
        allCOGS += (s.emptyBagQty || 0) * ebData.cost;
    });

    const allExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
    const netProfit = allRevenue - allCOGS - allExpenses;

    // --- 2. CASH IN HAND ---
    const cashFromSales = sales.reduce((sum, s) => sum + s.amountPaidAtSale, 0) + payments.reduce((sum, p) => sum + p.amount, 0);
    const totalPurchaseCash = purchases.reduce((sum, p) => sum + (p.amountPaid || 0), 0);
    const cashInHand = cashFromSales - allExpenses - totalPurchaseCash;

    // --- 3. DEBTS ---
    const moneyOwedToOwner = sales.filter(s => !s.writtenOff).reduce((sum, s) => sum + s.balanceOwing, 0);
    const moneyYouOwe = purchases.reduce((sum, p) => sum + Math.max(0, p.cost - (p.amountPaid || 0)), 0);

    // --- 4. STOCK VALUE ---
    let unsoldValue = 0;
    
    // Blocks Value
    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const producedBlocks = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
    const soldBlocks = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
    const brokenBlocks = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
    const returnedBlocks = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
    const remainingBlocks = Math.max(0, producedBlocks - soldBlocks - brokenBlocks + returnedBlocks);
    
    unsoldValue += remainingBlocks * getAvgCost('6');
    
    // Raw Materials Value
    unsoldValue += cementData.stock * cementData.cost;
    unsoldValue += sandData.stock * sandData.cost;
    unsoldValue += ebData.stock * ebData.cost;

    // --- CHART DATA ---
    const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
    const weekRev = sales.filter(s => s.date >= weekAgo).reduce((sum, s) => sum + s.totalAmount, 0);
    const monthRev = sales.filter(s => s.date >= monthAgo).reduce((sum, s) => sum + s.totalAmount, 0);

    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const thisMonthRev = sales.filter(s => { const d = new Date(s.date); return d.getMonth() === currentMonth && d.getFullYear() === currentYear; }).reduce((sum, s) => sum + s.totalAmount, 0);
    const lastMonthDate = new Date(currentYear, currentMonth - 1, 1);
    const lastMonth = lastMonthDate.getMonth();
    const lastMonthYear = lastMonthDate.getFullYear();
    const lastMonthRev = sales.filter(s => { const d = new Date(s.date); return d.getMonth() === lastMonth && d.getFullYear() === lastMonthYear; }).reduce((sum, s) => sum + s.totalAmount, 0);

    let momChangeHtml = '';
    if (lastMonthRev > 0) {
        const diff = thisMonthRev - lastMonthRev;
        const pct = (diff / lastMonthRev) * 100;
        const isUp = diff >= 0;
        momChangeHtml = `<div style="display:flex; align-items:center; justify-content:center; gap:4px; font-size:11px; font-weight:800; color:${isUp ? 'var(--brand-dark)' : 'var(--danger)'}; margin-top:4px;">${isUp ? '↑' : '↓'} ${Math.abs(pct).toFixed(1)}% vs last month</div>`;
    } else if (thisMonthRev > 0) {
        momChangeHtml = `<div style="font-size:11px; font-weight:800; color:var(--brand-dark); margin-top:4px;">↑ New sales this month</div>`;
    }

    let chartHtml = ''; let maxDayRev = 0; const days = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date(today.getTime() - i*24*60*60*1000);
        const dStr = d.toISOString().split('T')[0];
        const rev = sales.filter(s => s.date === dStr).reduce((sum, s) => sum + s.totalAmount, 0);
        if (rev > maxDayRev) maxDayRev = rev;
        days.push({ date: dStr, day: d.toLocaleDateString('en-US', {weekday:'short'}), rev: rev });
    }
    days.forEach(d => {
        const pct = maxDayRev > 0 ? (d.rev / maxDayRev) * 100 : 0;
        chartHtml += `<div class="chart-bar" style="height:${pct}%;" title="${formatNaira(d.rev)}"><div class="chart-label">${d.day}</div></div>`;
    });

    // --- LISTS ---
    const sizeTotals = { '6': 0 };
    sales.forEach(s => { if(sizeTotals[s.size] !== undefined) sizeTotals[s.size] += s.quantity; });
    let bestSizeHtml = '';
    Object.keys(sizeTotals).forEach(size => {
        if (sizeTotals[size] > 0) bestSizeHtml += `<div class="kv"><span>${size}" Blocks</span><strong>${sizeTotals[size].toLocaleString()} pcs</strong></div>`;
    });

    const custTotals = {};
    sales.forEach(s => { custTotals[s.customerName] = (custTotals[s.customerName] || 0) + s.totalAmount; });
    let topCustHtml = ''; let rk = 0;
    Object.entries(custTotals).sort((a,b)=>b[1]-a[1]).slice(0,3).forEach(([name, amt]) => {
        rk++;
        topCustHtml += `<div class="kv"><span><span class="rank">${rk}</span>${name}</span><strong>${formatNaira(amt)}</strong></div>`;
    });

    let profitHtml = '';
    const szSales = sales.filter(s => s.size === '6');
    const totalQty = szSales.reduce((sum, s) => sum + s.quantity, 0);
    const totalAmt = szSales.reduce((sum, s) => sum + s.totalAmount, 0);
    const avgSellPrice = totalQty > 0 ? (totalAmt / totalQty) : 0;
    const avgCost = getAvgCost('6');
    const profit = avgSellPrice - avgCost;
    if (avgSellPrice > 0) profitHtml += `<div class="kv"><span><strong>6"</strong> <span style="color:var(--muted); font-size:12px;">Sell ${formatNaira(avgSellPrice)}</span></span><strong class="${profit >= 0 ? 'pos' : 'neg'}">${formatNaira(profit)}</strong></div>`;

    const totalQtySold = sales.reduce((sum, s) => sum + s.quantity, 0);
    const profitPerBlock = totalQtySold > 0 ? (allRevenue - allCOGS) / totalQtySold : 0;
    let breakEvenText = "Set fixed costs in Settings";
    if (settings.fixedCostsMonthly > 0) breakEvenText = profitPerBlock > 0 ? Math.ceil(settings.fixedCostsMonthly / profitPerBlock).toLocaleString() + " blocks/month" : "Log sales to calculate";

    let lowStockHtml = '';
    if (cementData.stock <= settings.lowCement) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🪨 Cement</span><span>${cementData.stock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;
    if (sandData.stock <= settings.lowSand) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🏖️ Sand</span><span>${sandData.stock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;

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

    const currentMonthExp = expenses.filter(e => e.date.startsWith(todayStr.substring(0,7)));
    const totalExpAmt = currentMonthExp.reduce((sum, e) => sum + e.amount, 0);
    const expByCat = {};
    currentMonthExp.forEach(e => { expByCat[e.category] = (expByCat[e.category] || 0) + e.amount; });
    let expChartHtml = '';
    if (totalExpAmt > 0) {
        Object.keys(expByCat).sort((a,b)=>expByCat[b]-expByCat[a]).forEach(cat => {
            const pct = (expByCat[cat] / totalExpAmt) * 100;
            const catName = i18n[settings.lang][cat] || cat;
            expChartHtml += `<div style="margin-bottom:12px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; margin-bottom:4px;"><span style="text-transform:capitalize;">${catName}</span><span>${formatNaira(expByCat[cat])} (${pct.toFixed(0)}%)</span></div><div style="height:8px; background:var(--line); border-radius:4px; overflow:hidden;"><div style="height:100%; width:${pct}%; background:var(--danger); border-radius:4px;"></div></div></div>`;
        });
    } else expChartHtml = '<p style="font-size:13px; color:var(--muted);">No expenses logged this month.</p>';

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
                <div>Best Day<strong>${formatNaira(settings.bestDayAmount)}</strong></div>
            </div>
        </div>
        <div class="dash-grid">
            <div class="stat"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand}</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>
            <div class="stat"><div class="top"><span class="dot a">${ico('arrowIn')}</span><h4>${t.moneyOwed}</h4></div><div class="val">${formatNaira(moneyOwedToOwner)}</div></div>
            <div class="stat"><div class="top"><span class="dot r">${ico('arrowOut')}</span><h4>${t.moneyYouOwe}</h4></div><div class="val ${moneyYouOwe > 0 ? 'neg' : ''}">${formatNaira(moneyYouOwe)}</div></div>
            <div class="stat"><div class="top"><span class="dot b">${ico('box')}</span><h4>${t.stockValue}</h4></div><div class="val">${formatNaira(unsoldValue)}</div></div>
        </div>
        ${marginAlertHtml ? `<div class="section-title neg" style="margin-top:8px;">${ico('alert')} Alerts</div>${marginAlertHtml}` : ''}
        <div class="card">
            <h3>${ico('bars')} ${t.turnover}</h3>
            <div class="periods">
                <div><small>Today</small><strong>${formatNaira(dayRev)}</strong></div>
                <div><small>This Week</small><strong>${formatNaira(weekRev)}</strong></div>
                <div><small>This Month</small><strong>${formatNaira(monthRev)}</strong>${momChangeHtml}</div>
            </div>
            <div class="chart-container">${maxDayRev > 0 ? chartHtml : '<p style="font-size:13px; color:var(--muted); width:100%; text-align:center; align-self:center;">No sales data yet.</p>'}</div>
        </div>
        <div class="card">
            <h3>${ico('expenses')} Expense Breakdown</h3>
            ${expChartHtml}
        </div>
        <div class="card">
            <h3>${ico('trend')} ${t.profitMargins}</h3>
            ${profitHtml || '<p style="font-size:13px; color:var(--muted);">Log sales to see profit margins.</p>'}
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
print("Analytics math perfectly fixed.")

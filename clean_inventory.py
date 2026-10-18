import re
with open('index.html', 'r') as f: html = f.read()

# 1. Replace the renderInventory function entirely to use collapsible sections
start_idx = html.find('    function renderInventory(main) {')
end_idx = html.find('    function acceptVariance(size, expected, physical) {')

if start_idx != -1 and end_idx != -1:
    new_inventory = '''    function renderInventory(main) {
        const t = i18n[settings.lang];
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

        const sizes = ['4','6','9'];
        let blockHtml = '';

        sizes.forEach(sz => {
            const readyBatches = batches.filter(b => b.size === sz && b.status === 'ready');
            const curingBatches = batches.filter(b => b.size === sz && b.status === 'curing');
            
            const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
            const curing = curingBatches.reduce((s,b)=>s+b.blocksProduced,0);
            const sold = sales.filter(s => s.size === sz).reduce((s,v)=>s+v.quantity,0);
            const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);
            const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);
            
            const expectedReady = produced - sold - broken + returned;

            const physical = stockCounts[sz];
            let varianceHtml = '';
            if (physical !== undefined && physical !== expectedReady) {
                const diff = physical - expectedReady;
                varianceHtml = `
                    <div class="variance">
                        <div style="color: var(--danger); font-weight: 700; font-size: 13px;">${t.varianceWarning}</div>
                        <div style="font-size: 13px; margin-top: 4px;">Expected: ${expectedReady} | Counted: ${physical} (Diff: ${diff > 0 ? '+' : ''}${diff})</div>
                        <button onclick="acceptVariance('${sz}', ${expectedReady}, ${physical})" style="margin-top: 10px; padding: 11px; font-size: 13px; background: var(--danger); color: white; border: none; border-radius: 8px; width: 100%; font-weight: 700; cursor: pointer;">${t.acceptCount}</button>
                    </div>
                `;
            }

            blockHtml += `
                <div class="list-item" style="padding: 14px 16px; margin-bottom: 8px;">
                    <div class="list-header"><span>${sz}" Blocks</span><span class="pos">${expectedReady} Ready</span></div>
                    <div class="list-sub" style="margin-bottom: 8px;">Curing: ${curing} pcs · Sold: ${sold} pcs · ${t.broken}: ${broken} pcs</div>
                    <div class="actions" style="margin-top: 0;">
                        <button onclick="openStockCheck('${sz}', ${expectedReady})">${t.stockCheck}</button>
                        <button onclick="openBreakage('${sz}')" style="background:var(--accent-soft); color:#92400e; border-color:#fde68a;">${t.logBreakage}</button>
                    </div>
                    ${varianceHtml}
                </div>
            `;
        });

        const tile = (label, stock, low) => `
            <div class="stock-tile ${stock <= low ? 'low' : ''}">
                <div class="k">${label}</div>
                <div class="n">${stock}</div>
                ${stock <= low ? `<div class="w">${t.lowStock}</div>` : ''}
            </div>`;

        const isPurchasesCollapsed = localStorage.getItem('asad:purchasesCollapsed') === 'true';
        const isBlocksCollapsed = localStorage.getItem('asad:blocksCollapsed') === 'true';

        main.innerHTML = `
            ${backBtn(currentUser === 'owner' ? 'dashboard' : 'home')}
            <div class="page-title">${t.inventory}</div>
            <div class="page-sub">Raw materials and finished blocks</div>
            
            <!-- Raw Materials Card -->
            <div class="card">
                <h3>${ico('box')} ${t.rawMaterials}</h3>
                <div class="stock-grid">
                    ${tile(t.cement, cementStock, settings.lowCement)}
                    ${tile(t.sand, sandStock, settings.lowSand)}
                    ${tile(t.fuel, fuelStock, settings.lowFuel)}
                </div>
                <div class="row" style="margin-top:16px;">
                    <button class="btn btn-dark" style="margin-top:0;" onclick="openPurchase()">+ ${t.logPurchase}</button>
                    <button class="btn btn-outline" style="margin-top:0;" onclick="openAdjustStock()">Adjust Stock</button>
                </div>
            </div>

            <!-- Finished Blocks (Collapsible) -->
            <div class="section-title" onclick="toggleSection('blocks-list')" style="cursor:pointer; display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('production')} ${t.finishedBlocks}</span>
                <span id="blocks-list-icon" style="font-size:12px; color:var(--muted);">${isBlocksCollapsed ? '▼' : '▲'}</span>
            </div>
            <div id="blocks-list" style="display: ${isBlocksCollapsed ? 'none' : 'block'};">
                ${blockHtml}
            </div>

            <!-- Recent Purchases (Collapsible) -->
            <div class="section-title" onclick="toggleSection('purchases-section')" style="cursor:pointer; display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('report')} Recent Purchases</span>
                <span id="purchases-section-icon" style="font-size:12px; color:var(--muted);">${isPurchasesCollapsed ? '▼' : '▲'}</span>
            </div>
            <div id="purchases-section" style="display: ${isPurchasesCollapsed ? 'none' : 'block'};">
                <div class="form-group" style="margin-bottom:12px;">
                    <input type="text" id="search-purchases" placeholder="Search supplier..." oninput="filterPurchases(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;">
                </div>
                <div id="purchases-inner-list">
                    ${purchases.length > 0 ? [...purchases].reverse().slice(0,5).map(p => `
                        <div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')">
                            <div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div>
                            <div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div>
                        </div>
                    `).join('') : '<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases logged yet.</p>'}
                </div>
            </div>
        `;
    }

'''
    html = html[:start_idx] + new_inventory + html[end_idx:]

# 2. Update filterPurchases to target the new inner list
html = html.replace(
    "document.getElementById('purchases-list').innerHTML = html || `<p style=\"font-size:13px; color:var(--muted); text-align:center;\">No purchases found.</p>`;",
    "document.getElementById('purchases-inner-list').innerHTML = html || `<p style=\"font-size:13px; color:var(--muted); text-align:center;\">No purchases found.</p>`;"
)

# 3. Add the toggleSection function
toggle_func = '''
    function toggleSection(id) {
        const container = document.getElementById(id);
        const icon = document.getElementById(id + '-icon');
        if (!container) return;
        const isNowHidden = container.style.display === 'none';
        container.style.display = isNowHidden ? 'block' : 'none';
        if (icon) icon.textContent = isNowHidden ? '▲' : '▼';
        localStorage.setItem('asad:' + id + 'Collapsed', isNowHidden ? 'false' : 'true');
    }
'''
if 'function toggleSection' not in html:
    html = html.replace('// --- Details & Edit Modals ---', toggle_func + '\n// --- Details & Edit Modals ---')

with open('index.html', 'w') as f: f.write(html)

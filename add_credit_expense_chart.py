import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add creditLimits to settings
html = html.replace(
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500, defaultPrices: {'4': 0, '6': 0, '9': 0}",
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500, defaultPrices: {'4': 0, '6': 0, '9': 0}, creditLimits: {}"
)
if "if(!settings.creditLimits)" in html:
    html = html.replace(
        "if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};",
        "if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};\n    if(!settings.creditLimits) settings.creditLimits = {};"
    )

# 2. Update Customer Directory to show limits and allow setting them
old_dir = '''        let custHtml = Object.keys(uniqueCustomers).map(c => `
            <div class="list-item neutral" style="padding:12px; margin-bottom:8px;">
                <div class="list-header"><span>${c}</span> <span style="font-size:12px; color:var(--muted);">${uniqueCustomers[c] || 'No phone'}</span></div>
                ${uniqueCustomers[c] ? `<div class="actions" style="margin-top:8px;">
                    <a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a>
                    <a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a>
                </div>` : ''}
            </div>
        `).join('');'''

new_dir = '''        let custHtml = Object.keys(uniqueCustomers).map(c => {
            const limit = settings.creditLimits[c] || 0;
            const limitText = limit > 0 ? `Limit: ${formatNaira(limit)}` : 'No Limit';
            const totalOwed = sales.filter(s => s.customerName === c).reduce((sum, s) => sum + s.balanceOwing, 0);
            
            return `
            <div class="list-item neutral" style="padding:12px; margin-bottom:8px;">
                <div class="list-header"><span>${c}</span> <span style="font-size:12px; color:var(--muted);">${uniqueCustomers[c] || 'No phone'}</span></div>
                <div class="list-sub" style="font-size:11px; margin-top:4px;">
                    Owed: <strong style="color:${totalOwed > 0 ? 'var(--danger)' : 'var(--brand)'}">${formatNaira(totalOwed)}</strong> · ${limitText}
                    <button class="btn-outline" style="padding:2px 6px; font-size:10px; margin-left:6px; border-radius:4px;" onclick="setCreditLimit('${c.replace(/'/g, "\\'")}', ${limit})">Edit Limit</button>
                </div>
                ${uniqueCustomers[c] ? `<div class="actions" style="margin-top:8px;">
                    <a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a>
                    <a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a>
                </div>` : ''}
            </div>
        `}).join('');'''
html = html.replace(old_dir, new_dir)

# 3. Add setCreditLimit function
limit_func = '''
    function setCreditLimit(custName, currentLimit) {
        showDialog("Set Credit Limit", `Enter maximum debt allowed for ${custName} (₦). Enter 0 for no limit.`, (val) => {
            const lim = parseFloat(val) || 0;
            settings.creditLimits[custName] = lim;
            saveData('settings', settings);
            showToast('Credit limit updated', 'success');
            // Refresh the directory modal
            openDirectory();
        }, true);
        // Pre-fill the prompt
        setTimeout(() => {
            const input = document.getElementById('dialog-input');
            if(input) input.value = currentLimit || '';
        }, 100);
    }
'''
html = html.replace('    function openDirectory() {', limit_func + '\n    function openDirectory() {')

# 4. Enforce Credit Limit in saveSale
# We need to extract the saving logic into a separate function to call after confirmation
old_save_start = '''    function saveSale() {
        const qty = parseInt(document.getElementById('s-qty').value) || 0;
        const price = parseInt(document.getElementById('s-price').value) || 0;
        const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
        const paid = parseInt(document.getElementById('s-paid').value) || 0;
        const saleDate = document.getElementById('s-date').value || new Date().toISOString().split('T')[0];
        
        if(qty <= 0) return showToast('Enter valid quantity', 'err');

        const total = (qty * price) + delivery;
        const balance = total - paid;'''

new_save_start = '''    function saveSale() {
        const qty = parseInt(document.getElementById('s-qty').value) || 0;
        const price = parseInt(document.getElementById('s-price').value) || 0;
        const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
        const paid = parseInt(document.getElementById('s-paid').value) || 0;
        const saleDate = document.getElementById('s-date').value || new Date().toISOString().split('T')[0];
        const custName = document.getElementById('s-customer').value || 'Walk-in';
        
        if(qty <= 0) return showToast('Enter valid quantity', 'err');

        const total = (qty * price) + delivery;
        const balance = total - paid;

        // Credit Limit Check
        const limit = settings.creditLimits[custName] || 0;
        if (limit > 0) {
            const existingOwed = sales.filter(s => s.customerName === custName).reduce((sum, s) => sum + s.balanceOwing, 0);
            if (existingOwed + balance > limit) {
                showDialog("Credit Limit Exceeded", `Total debt for <strong>${custName}</strong> will be <strong>${formatNaira(existingOwed + balance)}</strong>, exceeding their limit of <strong>${formatNaira(limit)}</strong>.<br><br>Proceed anyway?`, () => {
                    processSaveSale(qty, price, delivery, paid, saleDate, custName);
                });
                return;
            }
        }
        processSaveSale(qty, price, delivery, paid, saleDate, custName);
    }

    function processSaveSale(qty, price, delivery, paid, saleDate, custName) {
        const total = (qty * price) + delivery;
        const balance = total - paid;'''
html = html.replace(old_save_start, new_save_start)

# Update the rest of the old saveSale function to use custName instead of reading the input again
html = html.replace(
    "customerName: document.getElementById('s-customer').value || 'Walk-in', customerPhone: document.getElementById('s-phone').value,",
    "customerName: custName, customerPhone: document.getElementById('s-phone').value,"
)

# 5. Add Expense Breakdown Chart to Dashboard
chart_js = '''
        // Expense Breakdown Chart (Current Month)
        const currentMonthExp = expenses.filter(e => e.date.startsWith(todayStr.substring(0,7)));
        const totalExpAmt = currentMonthExp.reduce((sum, e) => sum + e.amount, 0);
        const expByCat = {};
        currentMonthExp.forEach(e => { expByCat[e.category] = (expByCat[e.category] || 0) + e.amount; });
        
        let expChartHtml = '';
        if (totalExpAmt > 0) {
            Object.keys(expByCat).sort((a,b)=>expByCat[b]-expByCat[a]).forEach(cat => {
                const pct = (expByCat[cat] / totalExpAmt) * 100;
                const catName = i18n[settings.lang][cat] || cat;
                expChartHtml += `
                    <div style="margin-bottom:12px;">
                        <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; margin-bottom:4px;">
                            <span style="text-transform:capitalize;">${catName}</span>
                            <span>${formatNaira(expByCat[cat])} (${pct.toFixed(0)}%)</span>
                        </div>
                        <div style="height:8px; background:var(--line); border-radius:4px; overflow:hidden;">
                            <div style="height:100%; width:${pct}%; background:var(--danger); border-radius:4px;"></div>
                        </div>
                    </div>
                `;
            });
        } else {
            expChartHtml = '<p style="font-size:13px; color:var(--muted);">No expenses logged this month.</p>';
        }
'''
html = html.replace('        const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);', chart_js + '\n        const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);')

# Inject the chart into the Dashboard HTML
old_chart_anchor = '''            <div class="card">
                <h3>${ico('trend')} ${t.profitMargins}</h3>'''
new_chart_anchor = '''            <div class="card">
                <h3>${ico('expenses')} Expense Breakdown (This Month)</h3>
                ${expChartHtml}
            </div>

            <div class="card">
                <h3>${ico('trend')} ${t.profitMargins}</h3>'''
html = html.replace(old_chart_anchor, new_chart_anchor)

with open('index.html', 'w') as f: f.write(html)

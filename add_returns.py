with open('index.html', 'r') as f: html = f.read()

# 1. Add translations
html = html.replace('language: "Language"', 'language: "Language", logReturn: "Log Return", qtyReturned: "Qty Returned", refundAmt: "Refund Amount (₦)", reason: "Reason", recentReturns: "Recent Returns"')
html = html.replace('language: "Harshe"', 'language: "Harshe", logReturn: "Yi Rikodin Mayarwa", qtyReturned: "Yawan da aka Mayar", refundAmt: "Kudin da aka Mayar (₦)", reason: "Dalili", recentReturns: "Kwanan nan Mayarwa"')

# 2. Add returns array to state
html = html.replace("let breakagesLog = JSON.parse(localStorage.getItem('asad:breakages')) || [];", "let breakagesLog = JSON.parse(localStorage.getItem('asad:breakages')) || [];\n    let returns = JSON.parse(localStorage.getItem('asad:returns')) || [];")

# 3. Update Dashboard calculations (Revenue & COGS)
old_rev = "const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0);"
new_rev = "const totalReturnsAmount = returns.reduce((sum, r) => sum + (r.refundAmount || 0), 0);\n        const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0) - totalReturnsAmount;"
html = html.replace(old_rev, new_rev)

# 4. Update Inventory calculations (Add returned blocks to Ready stock)
old_inv = "const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);\n            \n            const expectedReady = produced - sold - broken;"
new_inv = "const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);\n            const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);\n            \n            const expectedReady = produced - sold - broken + returned;"
html = html.replace(old_inv, new_inv)

# 5. Add HTML button to Sales screen
old_sales_html = '''<div class="section-title">${ico('sales')} ${t.salesHistory}</div>'''
new_sales_html = '''<div class="section-title" style="display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('sales')} ${t.salesHistory}</span>
                <button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn}</button>
            </div>'''
html = html.replace(old_sales_html, new_sales_html)

# 6. Add Returns History to Sales screen
old_history = '''${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}'''
new_history = '''${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}
            
            <div class="section-title">${ico('back')} ${t.recentReturns}</div>
            ${returns.length > 0 ? [...returns].reverse().slice(0, 10).map(r => `
                <div class="list-item neutral" style="border-left-color:var(--warning);">
                    <div class="list-header"><span>${r.customerName}</span><span class="neg">-${formatNaira(r.refundAmount)}</span></div>
                    <div class="list-sub">${r.date} · ${r.size}" × ${r.quantity} · ${r.reason}</div>
                </div>
            `).join('') : '<div class="empty">No returns logged yet.</div>'}'''
html = html.replace(old_history, new_history)

# 7. Add openReturn and saveReturn functions
return_functions = '''
    function openReturn() {
        const t = i18n[settings.lang];
        document.getElementById('modal-body').innerHTML = `
            <h3>${t.logReturn}</h3>
            <div class="form-group"><label>${t.customer}</label><input type="text" id="r-customer" placeholder="Name"></div>
            <div class="row">
                <div class="form-group"><label>${t.date}</label><input type="date" id="r-date" value="${new Date().toISOString().split('T')[0]}"></div>
                <div class="form-group"><label>${t.size}</label><select id="r-size"><option value="4">4"</option><option value="6">6"</option><option value="9">9"</option></select></div>
            </div>
            <div class="row">
                <div class="form-group"><label>${t.qtyReturned}</label><input type="number" id="r-qty" value="1" min="1"></div>
                <div class="form-group"><label>${t.refundAmt}</label><input type="number" id="r-refund" value="0"></div>
            </div>
            <div class="form-group"><label>${t.reason}</label><input type="text" id="r-reason" placeholder="e.g. Broken, Wrong size"></div>
            <button class="btn" onclick="saveReturn()">Save Return</button>
            <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function saveReturn() {
        const qty = parseInt(document.getElementById('r-qty').value) || 0;
        if (qty <= 0) return showToast('Enter valid quantity', 'err');
        
        returns.push({
            id: Date.now().toString(),
            date: document.getElementById('r-date').value,
            customerName: document.getElementById('r-customer').value || 'Walk-in',
            size: document.getElementById('r-size').value,
            quantity: qty,
            refundAmount: parseFloat(document.getElementById('r-refund').value) || 0,
            reason: document.getElementById('r-reason').value || 'Unknown'
        });
        saveData('returns', returns);
        closeModal();
        nav('sales');
        showToast('Return logged successfully', 'success');
    }
'''
html = html.replace('// --- Debts Module ---', return_functions + '\n// --- Debts Module ---')

with open('index.html', 'w') as f: f.write(html)

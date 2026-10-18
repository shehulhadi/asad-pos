import re
with open('index.html', 'r') as f: html = f.read()

# 1. Initialize customExpenses in settings fallback
html = html.replace(
    "let settings = JSON.parse(localStorage.getItem('asad:settings')) || {\n        ownerPin: '1234', staffPin: '0000', lang: 'en', businessName: 'A. Jibrialla Construction Ltd.', businessPhone: '0906 634 4956',\n        marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20\n    };",
    "let settings = JSON.parse(localStorage.getItem('asad:settings')) || {\n        ownerPin: '1234', staffPin: '0000', lang: 'en', businessName: 'A. Jibrialla Construction Ltd.', businessPhone: '0906 634 4956',\n        marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: []\n    };\n    if(!settings.customExpenses) settings.customExpenses = [];"
)

# 2. Add Custom Expense Category UI in Settings
old_settings_btn = '''            <button class="btn" onclick="saveSettings()">${t.saveSettings}</button>'''
new_settings_btn = '''            <div class="eyebrow">Custom Expense Categories</div>
            <div class="row">
                <div class="form-group" style="flex:2;"><input type="text" id="set-new-expense" placeholder="e.g. Truck Hire, Tarp"></div>
                <div class="form-group" style="flex:1;"><button class="btn btn-outline" style="margin-top:0;" onclick="addExpenseCategory()">Add</button></div>
            </div>
            <button class="btn" onclick="saveSettings()">${t.saveSettings}</button>'''
html = html.replace(old_settings_btn, new_settings_btn)

# 3. Add function to handle adding category
add_exp_func = '''
    function addExpenseCategory() {
        const val = document.getElementById('set-new-expense').value.trim();
        if (!val) return;
        if (!settings.customExpenses.includes(val)) {
            settings.customExpenses.push(val);
            saveData('settings', settings);
            showToast('Category added', 'success');
            document.getElementById('set-new-expense').value = '';
        } else {
            showToast('Category already exists', 'err');
        }
    }
'''
html = html.replace('// --- Clear Cache ---', add_exp_func + '\n// --- Clear Cache ---')

# 4. Update Expense Form to include custom categories
old_exp_select = '''<select id="e-category"><option value="wages">${t.wages}</option><option value="repairs">${t.repairs}</option><option value="generator_fuel">${t.generator_fuel}</option><option value="rent">${t.rent}</option><option value="transport">${t.transport}</option><option value="loaders">${t.loaders}</option><option value="phone_data">${t.phone_data}</option><option value="other">${t.other}</option></select>'''
new_exp_select = '''<select id="e-category">
                        <option value="wages">${t.wages}</option><option value="repairs">${t.repairs}</option><option value="generator_fuel">${t.generator_fuel}</option><option value="rent">${t.rent}</option><option value="transport">${t.transport}</option><option value="loaders">${t.loaders}</option><option value="phone_data">${t.phone_data}</option><option value="other">${t.other}</option>
                        ${settings.customExpenses.map(c => `<option value="${c}">${c}</option>`).join('')}
                    </select>'''
html = html.replace(old_exp_select, new_exp_select)

# 5. Add Quick Add + Autofill UI to Sales Form
old_sales_cust = '''<div class="form-group"><label>${t.customer}</label><input type="text" id="s-customer" placeholder="Name"></div>'''
new_sales_cust = '''<div class="form-group"><label>${t.customer}</label><input type="text" id="s-customer" list="customer-names" placeholder="Name" oninput="autofillPhone(this.value)"><datalist id="customer-names"></datalist></div>'''
html = html.replace(old_sales_cust, new_sales_cust)

old_sales_qty = '''<div class="form-group"><label>${t.qty}</label><input type="number" id="s-qty" value="1" min="1" oninput="calcSale()"></div>'''
new_sales_qty = '''<div class="form-group"><label>${t.qty}</label><input type="number" id="s-qty" value="1" min="1" oninput="calcSale()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 50, 'calcSale')">+50</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 100, 'calcSale')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 500, 'calcSale')">+500</button></div></div>'''
html = html.replace(old_sales_qty, new_sales_qty)

# 6. Populate Datalist in renderSales
html = html.replace(
    "        calcSale();\n    }\n\n    function calcSale() {",
    '''        const uniqueCustomers = {};
        sales.forEach(s => { if(s.customerName && s.customerPhone) uniqueCustomers[s.customerName] = s.customerPhone; });
        document.getElementById('customer-names').innerHTML = Object.keys(uniqueCustomers).map(name => `<option value="${name}"></option>`).join('');

        calcSale();
    }

    function autofillPhone(name) {
        const match = sales.slice().reverse().find(s => s.customerName.toLowerCase() === name.toLowerCase());
        if (match && match.customerPhone) {
            document.getElementById('s-phone').value = match.customerPhone;
        }
    }

    function quickAdd(id, amount, calcFn) {
        const el = document.getElementById(id);
        el.value = (parseInt(el.value) || 0) + amount;
        if (typeof window[calcFn] === 'function') window[calcFn]();
    }

    function calcSale() {'''
)

# 7. Add Quick Add to Production Form
old_prod_qty = '''<div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="0" oninput="calcBatchCost()"></div>'''
new_prod_qty = '''<div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="0" oninput="calcBatchCost()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 100, 'calcBatchCost')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 500, 'calcBatchCost')">+500</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 1000, 'calcBatchCost')">+1000</button></div></div>'''
html = html.replace(old_prod_qty, new_prod_qty)

# 8. Add Supplier Autofill to Purchase Form
old_pur_supp = '''<input type="text" id="pur-supplier" placeholder="e.g. Dangote, Local Vendor">'''
new_pur_supp = '''<input type="text" id="pur-supplier" list="supplier-names" placeholder="e.g. Dangote, Local Vendor"><datalist id="supplier-names"></datalist>'''
html = html.replace(old_pur_supp, new_pur_supp)

# Populate Supplier Datalist when opening Purchase modal
html = html.replace(
    "        document.getElementById('modal').classList.add('active');\n    }\n\n    function savePurchase()",
    '''        const uniqueSuppliers = [...new Set(purchases.map(p => p.supplierName).filter(n => n && n !== 'Unknown'))];
        document.getElementById('supplier-names').innerHTML = uniqueSuppliers.map(name => `<option value="${name}"></option>`).join('');
        document.getElementById('modal').classList.add('active');
    }

    function savePurchase()'''
)

with open('index.html', 'w') as f: f.write(html)

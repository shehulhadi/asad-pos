import re
with open('index.html', 'r') as f: html = f.read()

# ==========================================
# 1. REMOVE FUEL & ADD LABOUR (TRANSLATIONS)
# ==========================================
html = html.replace('fuelCost: "Fuel/Diesel Cost (₦)", fuelQty: "Fuel Qty (Litres)"', 'labourCost: "Labour Cost (₦)"')
html = html.replace('fuelCost: "Kudin Man Fetur (₦)", fuelQty: "Yawan Man Fetur"', 'labourCost: "Kudin Ma\'aikata (₦)"')
html = html.replace('fuel: "Fuel"', '')
html = html.replace('fuel: "Man Fetur"', '')

# ==========================================
# 2. REMOVE FUEL FROM INVENTORY
# ==========================================
# Remove fuel calculation
html = re.sub(r'const fuelPurchased = purchases.*?\n\s*const fuelStock = .*?;', '', html, flags=re.DOTALL)

# Remove fuel tile from HTML
html = re.sub(r'<div style="background:\$\{fuelStock.*?</div>\s*</div>', '', html, flags=re.DOTALL)

# Update stock-grid from 3 columns to 2 columns (Cement and Sand)
html = html.replace(
    '<div class="stock-grid">',
    '<div class="stock-grid" style="grid-template-columns: 1fr 1fr;">'
)

# Remove fuel option from Purchase Modal
html = html.replace('<option value="fuel">${t.fuel}</option>', '')
html = html.replace('<option value="fuel">Fuel</option>', '')

# ==========================================
# 3. REMOVE FUEL & ADD LABOUR TO PRODUCTION
# ==========================================
# Update Production Form HTML
old_prod_form = '''                <div class="row">
                    <div class="form-group"><label>${t.fuelCost}</label><input type="number" id="p-fuel-cost" value="0" oninput="calcBatchCost()"></div>
                    <div class="form-group"><label>${t.fuelQty}</label><input type="number" id="p-fuel-qty" value="0"></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>${t.otherCost}</label><input type="number" id="p-other-cost" value="0" oninput="calcBatchCost()"></div>
                    <div class="form-group"><label>${t.breakages}</label><input type="number" id="p-breakages" value="0"></div>
                </div>'''
new_prod_form = '''                <div class="row">
                    <div class="form-group"><label>${t.labourCost}</label><input type="number" id="p-labour-cost" value="0" oninput="calcBatchCost()"></div>
                    <div class="form-group"><label>${t.otherCost}</label><input type="number" id="p-other-cost" value="0" oninput="calcBatchCost()"></div>
                </div>
                <div class="form-group">
                    <label>${t.breakages}</label><input type="number" id="p-breakages" value="0">
                </div>'''
html = html.replace(old_prod_form, new_prod_form)

# Update calcBatchCost
old_calc = '''        const fc = parseFloat(document.getElementById('p-fuel-cost').value) || 0;
        const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
        const total = cb + sc + fc + oc;'''
new_calc = '''        const lc = parseFloat(document.getElementById('p-labour-cost').value) || 0;
        const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
        const total = cb + sc + lc + oc;'''
html = html.replace(old_calc, new_calc)

# Update saveBatch
old_save_batch = '''        const fc = parseFloat(document.getElementById('p-fuel-cost').value) || 0;
        const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
        const totalCost = cb + sc + fc + oc;
        const batch = { id: Date.now().toString(), date: document.getElementById('p-date').value, size: document.getElementById('p-size').value, worker: document.getElementById('p-worker').value || 'Unknown', blocksProduced: blocks, breakages: parseInt(document.getElementById('p-breakages').value) || 0, curingLoss: parseInt(document.getElementById('p-curing-loss').value) || 0, cementBags: parseFloat(document.getElementById('p-cement-bags').value) || 0, sandQty: parseFloat(document.getElementById('p-sand-qty').value) || 0, fuelQty: parseFloat(document.getElementById('p-fuel-qty').value) || 0, totalCost: totalCost, costPerBlock: totalCost / blocks, status: 'curing' };'''
new_save_batch = '''        const lc = parseFloat(document.getElementById('p-labour-cost').value) || 0;
        const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
        const totalCost = cb + sc + lc + oc;
        const batch = { id: Date.now().toString(), date: document.getElementById('p-date').value, size: document.getElementById('p-size').value, worker: document.getElementById('p-worker').value || 'Unknown', blocksProduced: blocks, breakages: parseInt(document.getElementById('p-breakages').value) || 0, curingLoss: parseInt(document.getElementById('p-curing-loss').value) || 0, cementBags: parseFloat(document.getElementById('p-cement-bags').value) || 0, sandQty: parseFloat(document.getElementById('p-sand-qty').value) || 0, labourCost: lc, totalCost: totalCost, costPerBlock: totalCost / blocks, status: 'curing' };'''
html = html.replace(old_save_batch, new_save_batch)

# Remove fuel from Dashboard Low Stock Alerts
html = re.sub(r'if \(fuelStock <= settings\.lowFuel\) lowStockHtml \+= .*?;\n', '', html)
html = re.sub(r'const fuelPurchased = purchases.*?\n\s*const fuelAdj = .*?;', '', html)
html = re.sub(r'const fuelStock = .*?;', '', html)

# ==========================================
# 4. CUSTOMER DIRECTORY SHORTCUT
# ==========================================
# Add + New Sale button to Customer Directory
old_dir_cust = '''<div class="actions" style="margin-top:8px;">
                    <a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a>
                    <a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a>
                </div>'''
new_dir_cust = '''<div class="actions" style="margin-top:8px;">
                    <a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a>
                    <a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a>
                    <button class="btn" style="flex:1; padding:6px; font-size:12px;" onclick="startSaleForCustomer('${c.replace(/'/g, "\\'")}', '${uniqueCustomers[c].replace(/'/g, "\\'")}')">+ Sale</button>
                </div>'''
html = html.replace(old_dir_cust, new_dir_cust)

# Add startSaleForCustomer function
new_js = '''
    function startSaleForCustomer(name, phone) {
        closeModal();
        nav('sales');
        setTimeout(() => {
            if(document.getElementById('s-customer')) {
                document.getElementById('s-customer').value = name;
                document.getElementById('s-phone').value = phone || '';
                updateDefaultPrice(); // Trigger calc
            }
        }, 100);
    }
    
    // --- Debts Module ---
'''
html = html.replace('// --- Debts Module ---', new_js)

with open('index.html', 'w') as f: f.write(html)

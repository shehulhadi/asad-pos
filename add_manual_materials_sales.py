import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add the inputs to the Sales Form (right after Quantity/Price)
old_form = '''                <div class="row">
                    <div class="form-group"><label>${t.price}</label><input type="number" id="s-price" value="0" oninput="calcSale()"></div>
                    <div class="form-group"><label>${t.delivery}</label><input type="number" id="s-delivery" value="0" oninput="calcSale()"></div>
                </div>'''
new_form = '''                <div class="row">
                    <div class="form-group"><label>${t.price}</label><input type="number" id="s-price" value="0" oninput="calcSale()"></div>
                    <div class="form-group"><label>${t.delivery}</label><input type="number" id="s-delivery" value="0" oninput="calcSale()"></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>Cement Used (Bags)</label><input type="number" id="s-cement-used" placeholder="Auto-calc" style="background:#fff;"></div>
                    <div class="form-group"><label>Sand Used (Bags)</label><input type="number" id="s-sand-used" placeholder="Auto-calc" style="background:#fff;"></div>
                </div>'''
html = html.replace(old_form, new_form)

# 2. Update executeSaveSale to read these inputs and save them
old_save = '''            const sale = { 
                id: Date.now().toString(), 
                createdAt: getWATDate().toISOString(), 
                invoiceNo: nextInv, 
                date: saleDate, 
                customerName: custName, 
                customerPhone: document.getElementById('s-phone').value || '', 
                size: document.getElementById('s-size').value, 
                quantity: qty, 
                pricePerBlock: price, 
                deliveryCharge: delivery, 
                totalAmount: total, 
                amountPaidAtSale: paid, 
                balanceOwing: balance, 
                deliveryStatus: 'pending' 
            };'''
new_save = '''            const manualCement = parseInt(document.getElementById('s-cement-used').value) || 0;
            const manualSand = parseInt(document.getElementById('s-sand-used').value) || 0;

            const sale = { 
                id: Date.now().toString(), 
                createdAt: getWATDate().toISOString(), 
                invoiceNo: nextInv, 
                date: saleDate, 
                customerName: custName, 
                customerPhone: document.getElementById('s-phone').value || '', 
                size: document.getElementById('s-size').value, 
                quantity: qty, 
                pricePerBlock: price, 
                deliveryCharge: delivery, 
                totalAmount: total, 
                amountPaidAtSale: paid, 
                balanceOwing: balance, 
                deliveryStatus: 'pending',
                cementUsed: manualCement > 0 ? manualCement : Math.ceil(qty / (settings.mixCement || 50)),
                sandUsed: manualSand > 0 ? manualSand : Math.ceil(qty / (settings.mixSand || 500))
            };'''
html = html.replace(old_save, new_save)

# 3. Update the HTML Receipt (Save & Details)
html = html.replace(
    '<div class="kv"><span>Est. Materials Used</span><strong>${Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand</strong></div>',
    '<div class="kv"><span>Materials Used</span><strong>${sale.cementUsed || Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${sale.sandUsed || Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand</strong></div>'
)
html = html.replace(
    '<div class="kv"><span>Est. Materials Used</span><strong>${Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand</strong></div>',
    '<div class="kv"><span>Materials Used</span><strong>${s.cementUsed || Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${s.sandUsed || Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand</strong></div>'
)

# 4. Update WhatsApp Receipt
html = html.replace(
    '`Est. Mix: ${Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand\\n` +',
    '`Materials: ${sale.cementUsed || Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${sale.sandUsed || Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand\\n` +'
)

# 5. Update Canvas Image Receipt
html = html.replace(
    'ctx.fillText(`Est. Mix: ${Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand`, 40, 440);',
    'ctx.fillText(`Materials: ${s.cementUsed || Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${s.sandUsed || Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand`, 40, 440);'
)

with open('index.html', 'w') as f: f.write(html)

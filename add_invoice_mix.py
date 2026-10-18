import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add mix ratio defaults to settings
html = html.replace(
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0",
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500"
)
if "if(settings.mixCement === undefined)" in html:
    html = html.replace(
        "if(settings.reminderInterval === undefined) settings.reminderInterval = 0;",
        "if(settings.reminderInterval === undefined) settings.reminderInterval = 0;\n    if(settings.mixCement === undefined) settings.mixCement = 50;\n    if(settings.mixSand === undefined) settings.mixSand = 500;"
    )

# 2. Add Mix Ratio fields to Settings UI
old_settings_ui = '''            <div class="form-group" style="margin-top:16px;">
                <label>Sales Reminder Notification</label>
                <select id="set-reminder">'''
new_settings_ui = '''            <div class="eyebrow">Standard Mix Ratios</div>
            <div class="row">
                <div class="form-group"><label>Blocks per Cement Bag</label><input type="number" id="set-mix-cement" value="${settings.mixCement}"></div>
                <div class="form-group"><label>Blocks per Sand Trip</label><input type="number" id="set-mix-sand" value="${settings.mixSand}"></div>
            </div>
            <div class="form-group" style="margin-top:16px;">
                <label>Sales Reminder Notification</label>
                <select id="set-reminder">'''
html = html.replace(old_settings_ui, new_settings_ui)

# 3. Save mix ratios in saveSettings
old_save_settings = '''        settings.marginAlertPct = parseFloat(document.getElementById('set-margin').value) || 0;'''
new_save_settings = '''        settings.mixCement = parseInt(document.getElementById('set-mix-cement').value) || 50;
        settings.mixSand = parseInt(document.getElementById('set-mix-sand').value) || 500;
        settings.marginAlertPct = parseFloat(document.getElementById('set-margin').value) || 0;'''
html = html.replace(old_save_settings, new_save_settings)

# 4. Add Auto-Fill Button to Production Form
old_prod_qty = '''<div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="0" oninput="calcBatchCost()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 100, 'calcBatchCost')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 500, 'calcBatchCost')">+500</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 1000, 'calcBatchCost')">+1000</button></div></div>'''
new_prod_qty = '''<div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="0" oninput="calcBatchCost()"><div style="display:flex; gap:6px; margin-top:6px; flex-wrap:wrap;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 100, 'calcBatchCost')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 500, 'calcBatchCost')">+500</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 1000, 'calcBatchCost')">+1000</button><button type="button" class="btn" style="padding:6px; font-size:12px; margin:0; background:var(--accent); color:#fff; border:none;" onclick="autoFillMaterials()">⚡ Auto-Fill Mix</button></div></div>'''
html = html.replace(old_prod_qty, new_prod_qty)

# 5. Add Auto-Fill JS Logic
auto_fill_js = '''
    function autoFillMaterials() {
        const blocks = parseInt(document.getElementById('p-blocks').value) || 0;
        if(blocks <= 0) return showToast('Enter blocks produced first', 'err');
        
        const mixCement = settings.mixCement || 50;
        const mixSand = settings.mixSand || 500;
        
        document.getElementById('p-cement-bags').value = Math.ceil(blocks / mixCement);
        document.getElementById('p-sand-qty').value = Math.ceil(blocks / mixSand);
        
        calcBatchCost();
        showToast('Quantities auto-filled based on mix', 'success');
    }
'''
html = html.replace('    function calcBatchCost() {', auto_fill_js + '\n    function calcBatchCost() {')

# 6. Generate Invoice Number in saveSale
old_invoice_gen = '''        const sale = { id: Date.now().toString(), date: saleDate, customerName: document.getElementById('s-customer').value || 'Walk-in', customerPhone: document.getElementById('s-phone').value, size: document.getElementById('s-size').value, quantity: qty, pricePerBlock: price, deliveryCharge: delivery, totalAmount: total, amountPaidAtSale: paid, balanceOwing: balance, deliveryStatus: 'pending' };'''
new_invoice_gen = '''        let maxInv = 0;
        sales.forEach(s => {
            if(s.invoiceNo) {
                const num = parseInt(s.invoiceNo.replace('INV-', ''));
                if(num > maxInv) maxInv = num;
            }
        });
        const nextInv = 'INV-' + (maxInv + 1).toString().padStart(4, '0');

        const sale = { id: Date.now().toString(), invoiceNo: nextInv, date: saleDate, customerName: document.getElementById('s-customer').value || 'Walk-in', customerPhone: document.getElementById('s-phone').value, size: document.getElementById('s-size').value, quantity: qty, pricePerBlock: price, deliveryCharge: delivery, totalAmount: total, amountPaidAtSale: paid, balanceOwing: balance, deliveryStatus: 'pending' };'''
html = html.replace(old_invoice_gen, new_invoice_gen)

# 7. Add Invoice No to WhatsApp Receipt
old_wa_rcpt = '''`*INVOICE / RECEIPT*\\n` +
            `Date: ${sale.date}\\n` +'''
new_wa_rcpt = '''`*INVOICE / RECEIPT*\\n` +
            `Invoice No: ${sale.invoiceNo || 'N/A'}\\n` +
            `Date: ${sale.date}\\n` +'''
html = html.replace(old_wa_rcpt, new_wa_rcpt)

# 8. Add Invoice No to Sale Details Modal
old_details_kv = '''<div class="kv"><span>Price per Block</span><strong>${formatNaira(s.pricePerBlock)}</strong></div>'''
new_details_kv = '''<div class="kv"><span>Invoice No.</span><strong>${s.invoiceNo || 'N/A'}</strong></div>
            <div class="kv"><span>Price per Block</span><strong>${formatNaira(s.pricePerBlock)}</strong></div>'''
html = html.replace(old_details_kv, new_details_kv)

# 9. Add Invoice No to Initial Receipt Modal
old_receipt_kv = '''<div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>'''
new_receipt_kv = '''<div class="kv"><span>Invoice No.</span><strong>${sale.invoiceNo}</strong></div>
            <div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>'''
html = html.replace(old_receipt_kv, new_receipt_kv)

with open('index.html', 'w') as f: f.write(html)

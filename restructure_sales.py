import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace renderSales
start = js.find('function renderSales(main) {')
end = js.find('function updateDefaultPrice() {')
if start != -1 and end != -1:
    new_sales = '''function renderSales(main) { 
    const t = i18n[settings.lang];
    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 15);
    recentSales.forEach(s => {
        historyHtml += `<div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')"><div class="list-header"><span>${s.customerName}</span><strong class="pos">${formatNaira(s.totalAmount)}</strong></div><div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div><div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending</span>`}</div></div>`;
    });

    main.innerHTML = `
        <div class="card">
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
                    <div class="form-group" style="flex:1.5;"><label>${t.size}</label><select id="s-size" onchange="updateDefaultPrice()"><option value="4">4"</option><option value="6">6"</option><option value="9">9"</option></select></div>
                    <div class="form-group" style="flex:1;"><label>Qty</label><input type="number" id="s-qty" value="" placeholder="0" oninput="calcSale()"></div>
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
        </div>
        <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;"><span>${ico('sales')} ${t.salesHistory}</span><button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn || 'Log Return'}</button></div>
        <div class="form-group" style="margin-bottom:12px;"><input type="text" id="search-sales" placeholder="Search by customer name or date..." oninput="filterSales(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;"></div>
        <div id="sales-history-list">${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}</div>
    `;
    const uniqueCustomers = {};
    sales.forEach(s => { if(s.customerName && s.customerPhone) uniqueCustomers[s.customerName] = s.customerPhone; });
    document.getElementById('customer-names').innerHTML = Object.keys(uniqueCustomers).map(name => `<option value="${name}"></option>`).join('');
    calcSale();
}

'''
    js = js[:start] + new_sales + js[end:]

# 2. Update calcSale
start_calc = js.find('function calcSale() {')
end_calc = js.find('function saveSale() {')
if start_calc != -1 and end_calc != -1:
    new_calc = '''function calcSale() {
    const bQty = parseFloat(document.getElementById('s-qty').value) || 0;
    const bPrice = parseFloat(document.getElementById('s-price').value) || 0;
    const cQty = parseFloat(document.getElementById('s-cement-qty').value) || 0;
    const cPrice = parseFloat(document.getElementById('s-cement-price').value) || 0;
    const sQty = parseFloat(document.getElementById('s-sand-qty').value) || 0;
    const sPrice = parseFloat(document.getElementById('s-sand-price').value) || 0;
    const delivery = parseFloat(document.getElementById('s-delivery').value) || 0;
    const paid = parseFloat(document.getElementById('s-paid').value) || 0;
    
    const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + delivery;
    const balance = total - paid;
    
    document.getElementById('s-total-display').textContent = total.toLocaleString();
    document.getElementById('s-balance-display').textContent = balance.toLocaleString();
}

'''
    js = js[:start_calc] + new_calc + js[end_calc:]

# 3. Update executeSaveSale (handling the math and receipt)
start_save = js.find('function executeSaveSale(')
end_save = js.find('function openSaleDetails(')
if start_save != -1 and end_save != -1:
    new_exec = '''function executeSaveSale(qty, price, delivery, paid, saleDate, custName) {
    try {
        const cQty = parseInt(document.getElementById('s-cement-qty').value) || 0;
        const cPrice = parseFloat(document.getElementById('s-cement-price').value) || 0;
        const sQty = parseInt(document.getElementById('s-sand-qty').value) || 0;
        const sPrice = parseFloat(document.getElementById('s-sand-price').value) || 0;
        
        const total = (qty * price) + (cQty * cPrice) + (sQty * sPrice) + delivery;
        const balance = total - paid;

        let maxInv = 0;
        sales.forEach(s => { if(s.invoiceNo && typeof s.invoiceNo === 'string') { const num = parseInt(s.invoiceNo.replace('INV-', '')); if(!isNaN(num) && num > maxInv) maxInv = num; } });
        const nextInv = 'INV-' + (maxInv + 1).toString().padStart(4, '0');
        
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
            cementQty: cQty,
            cementPrice: cPrice,
            sandQty: sQty,
            sandPrice: sPrice,
            deliveryCharge: delivery, 
            totalAmount: total, 
            amountPaidAtSale: paid, 
            balanceOwing: balance, 
            deliveryStatus: 'pending'
        };
        
        sales.push(sale); saveData('sales', sales);
        
        if (navigator.vibrate) navigator.vibrate(50);
        
        const todayStr = getTodayStr();
        const todayTotal = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
        if (todayTotal > (settings.bestDayAmount || 0)) { 
            settings.bestDayAmount = todayTotal; saveData('settings', settings); triggerConfetti(); showToast(`🏆 NEW BEST DAY! ${formatNaira(todayTotal)}`, 'success'); 
        }

        const waText = buildWhatsAppReceipt(sale);
        const waPhone = (sale.customerPhone || '').replace(/^0/, '234');
        const waLink = `https://wa.me/${waPhone}?text=${waText}`;

        let itemsHtml = '';
        if (qty > 0) itemsHtml += `<div class="kv"><span>${qty} pcs of ${sale.size}" Blocks</span><strong>${formatNaira(qty * price)}</strong></div>`;
        if (cQty > 0) itemsHtml += `<div class="kv"><span>${cQty} bags of Cement</span><strong>${formatNaira(cQty * cPrice)}</strong></div>`;
        if (sQty > 0) itemsHtml += `<div class="kv"><span>${sQty} bags of Sand</span><strong>${formatNaira(sQty * sPrice)}</strong></div>`;
        if (delivery > 0) itemsHtml += `<div class="kv"><span>Delivery Charge</span><strong>${formatNaira(delivery)}</strong></div>`;

        document.getElementById('modal-body').innerHTML = `
            <div style="text-align:center; margin-bottom:20px;">
                <div style="width:48px; height:48px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 10px;"><svg class="ic" style="width:24px;height:24px;stroke-width:2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                <h3 style="margin-bottom:2px;">Sale Recorded</h3>
                <p style="font-size:12px; color:var(--muted);">${new Date().toLocaleString()}</p>
            </div>
            <div class="kv"><span>Invoice No.</span><strong>${sale.invoiceNo}</strong></div>
            <div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>
            
            <div class="eyebrow" style="margin-top:8px;">Items</div>
            ${itemsHtml || '<p style="font-size:13px; color:var(--muted);">No items logged.</p>'}
            
            <div class="kv" style="border-bottom:2px solid var(--line); padding-bottom:12px; margin-bottom:12px; margin-top:12px;">
                <span style="font-size:16px; font-weight:800;">Total Amount</span>
                <strong style="font-size:20px; color:var(--brand); font-weight:800;">${formatNaira(total)}</strong>
            </div>
            
            <div class="kv"><span>Amount Paid</span><strong>${formatNaira(sale.amountPaidAtSale)}</strong></div>
            <div class="kv" style="border-bottom:none;"><span>Outstanding Balance</span><strong style="color:${balance > 0 ? 'var(--danger)' : 'var(--brand)'}; font-size:16px;">${formatNaira(balance)}</strong></div>
            
            <div class="actions" style="margin-top:24px; margin-bottom:10px;">
                <a href="${waLink}" target="_blank"><button class="wa" style="padding:14px; font-size:15px;">WhatsApp</button></a>
                <button onclick="shareReceiptImage('${sale.id}')" style="padding:14px; font-size:15px; background:var(--accent); color:#fff; border:none;">📸 Image</button>
            </div>
            <div class="row"><button class="btn btn-outline" onclick="printDocument()">Print</button><button class="btn btn-outline" onclick="closeModal(); nav('sales')">Close</button></div>`;
        document.getElementById('modal').classList.add('active');
    } catch (e) { showToast("Error: " + e.message, "err"); }
}

'''
    js = js[:start_save] + new_exec + js[end_save:]

# 4. Update buildWhatsAppReceipt to itemize
start_wa = js.find('function buildWhatsAppReceipt(sale) {')
end_wa = js.find('function shareReceiptImage(saleId) {')
if start_wa != -1 and end_wa != -1:
    new_wa = '''function buildWhatsAppReceipt(sale) {
    let itemsText = "";
    if (sale.quantity > 0) itemsText += `- ${sale.quantity} pcs of ${sale.size}" Blocks @ ₦${sale.pricePerBlock.toLocaleString()}\\n`;
    if (sale.cementQty > 0) itemsText += `- ${sale.cementQty} bags of Cement @ ₦${sale.cementPrice.toLocaleString()}\\n`;
    if (sale.sandQty > 0) itemsText += `- ${sale.sandQty} bags of Sand @ ₦${sale.sandPrice.toLocaleString()}\\n`;
    if (sale.deliveryCharge > 0) itemsText += `- Delivery Charge: ₦${sale.deliveryCharge.toLocaleString()}\\n`;

    const text = "*🧱 " + settings.businessName.toUpperCase() + "*\\n" +
        "📞 " + (settings.businessPhone || 'N/A') + "\\n" +
        "--------------------------------\\n" +
        "*INVOICE / RECEIPT*\\n" +
        "Invoice No: " + (sale.invoiceNo || 'N/A') + "\\n" +
        "Date: " + sale.date + " " + (sale.createdAt ? new Date(sale.createdAt).toLocaleTimeString() : '') + "\\n" +
        "Customer: " + sale.customerName + "\\n" +
        "--------------------------------\\n" +
        "*ITEMS BOUGHT:*\\n" + itemsText + "\\n" +
        "*Total Amount: ₦" + sale.totalAmount.toLocaleString() + "*\\n" +
        "Amount Paid: ₦" + sale.amountPaidAtSale.toLocaleString() + "\\n" +
        "*Outstanding Balance: ₦" + sale.balanceOwing.toLocaleString() + "*\\n" +
        "--------------------------------\\n" +
        "Thank you for your patronage! 🙏";
    return encodeURIComponent(text);
}

'''
    js = js[:start_wa] + new_wa + js[end_wa:]

with open('app.js', 'w') as f: f.write(js)

import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace openSaleDetails to itemize Cement & Sand
start_details = js.find('function openSaleDetails(saleId) {')
end_details = js.find('function editSale(saleId) {')
if start_details != -1 and end_details != -1:
    new_details = '''function openSaleDetails(saleId) {
    const s = sales.find(x => x.id === saleId);
    if (!s) return;
    
    let itemsHtml = '';
    if (s.quantity > 0) itemsHtml += `<div class="kv"><span>${s.quantity} pcs of ${s.size}" Blocks</span><strong>${formatNaira(s.quantity * s.pricePerBlock)}</strong></div>`;
    if (s.cementQty > 0) itemsHtml += `<div class="kv"><span>${s.cementQty} bags of Cement</span><strong>${formatNaira(s.cementQty * s.cementPrice)}</strong></div>`;
    if (s.sandQty > 0) itemsHtml += `<div class="kv"><span>${s.sandQty} bags of Sand</span><strong>${formatNaira(s.sandQty * s.sandPrice)}</strong></div>`;
    if (s.deliveryCharge > 0) itemsHtml += `<div class="kv"><span>Delivery Charge</span><strong>${formatNaira(s.deliveryCharge)}</strong></div>`;

    document.getElementById('modal-body').innerHTML = `
        <h3>Receipt · ${s.customerName}</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted);">${s.date} ${s.createdAt ? new Date(s.createdAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : ''}</p>
            <p style="font-size:28px; font-weight:800; color:var(--brand); margin-top:8px;">${formatNaira(s.totalAmount)}</p>
            ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Owing ${formatNaira(s.balanceOwing)}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
        </div>
        <div class="kv"><span>Invoice No.</span><strong>${s.invoiceNo || 'N/A'}</strong></div>
        <div class="kv"><span>Phone</span><strong>${s.customerPhone || 'N/A'}</strong></div>
        
        <div class="eyebrow">Items Bought</div>
        ${itemsHtml || '<p style="font-size:13px; color:var(--muted);">No items logged.</p>'}
        
        <div class="eyebrow">Payment</div>
        <div class="kv"><span>Amount Paid</span><strong>${formatNaira(s.amountPaidAtSale)}</strong></div>
        
        <div class="actions" style="margin-top:24px; margin-bottom:12px;">
            <a href="https://wa.me/${(s.customerPhone || '').replace(/^0/, '234')}?text=${buildWhatsAppReceipt(s)}" target="_blank"><button class="wa">WhatsApp</button></a>
            <button onclick="shareReceiptImage('${s.id}')">📸 Image</button>
        </div>
        <div class="row">
            <button class="btn btn-outline" onclick="closeModal()">Close</button>
            <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
        </div>
        <button class="btn ${s.deliveryStatus === 'delivered' ? 'btn-outline' : 'btn-dark'}" style="margin-top:8px; ${s.deliveryStatus === 'delivered' ? 'border-color:var(--brand); color:var(--brand);' : ''}" onclick="toggleDelivery('${s.id}')">
            ${s.deliveryStatus === 'delivered' ? '✅ Mark as Pending' : '🚚 Mark as Delivered'}
        </button>
        <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteSale('${s.id}')">Delete Sale</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start_details] + new_details + js[end_details:]

# 2. Replace editSale and calcEditSale
start_edit = js.find('function editSale(saleId) {')
end_edit = js.find('function saveEditedSale(saleId) {')
if start_edit != -1 and end_edit != -1:
    new_edit = '''function editSale(saleId) {
    const s = sales.find(x => x.id === saleId);
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Sale</h3>
        
        <div class="eyebrow">Customer Info</div>
        <div class="form-group"><label>Customer</label><input type="text" id="edit-s-customer" value="${s.customerName}"></div>
        <div class="row">
            <div class="form-group"><label>Date</label><input type="date" id="edit-s-date" value="${s.date}"></div>
            <div class="form-group"><label>Phone</label><input type="tel" id="edit-s-phone" value="${s.customerPhone || ''}"></div>
        </div>

        <div class="eyebrow">Items Bought</div>
        <div style="background:var(--bg); padding:12px; border-radius:8px; margin-bottom:12px;">
            <div style="font-weight:700; font-size:13px; margin-bottom:8px;">Blocks</div>
            <div class="row">
                <div class="form-group" style="flex:1.5;"><label>Size</label><select id="edit-s-size"><option value="4" ${s.size==='4'?'selected':''}>4"</option><option value="6" ${s.size==='6'?'selected':''}>6"</option><option value="9" ${s.size==='9'?'selected':''}>9"</option></select></div>
                <div class="form-group" style="flex:1;"><label>Qty</label><input type="number" id="edit-s-qty" value="${s.quantity || ''}" placeholder="0" oninput="calcEditSale()"></div>
                <div class="form-group" style="flex:1.5;"><label>Price (₦)</label><input type="number" id="edit-s-price" value="${s.pricePerBlock || ''}" placeholder="0" oninput="calcEditSale()"></div>
            </div>
        </div>

        <div class="row">
            <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="edit-s-cement-qty" value="${s.cementQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="edit-s-cement-price" value="${s.cementPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>

        <div class="eyebrow">Payment</div>
        <div class="row">
            <div class="form-group"><label>Delivery Charge (₦)</label><input type="number" id="edit-s-delivery" value="${s.deliveryCharge || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Amount Paid (₦)</label><input type="number" id="edit-s-paid" value="${s.amountPaidAtSale || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        
        <div class="calc-box">
            <div class="line"><span>Total Amount</span> <span>₦<span id="edit-s-total">0</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="edit-s-balance">0</span></span></div>
        </div>
        
        <div class="row">
            <button class="btn btn-outline" onclick="openSaleDetails('${s.id}')">Back</button>
            <button class="btn" onclick="saveEditedSale('${s.id}')">Save Changes</button>
        </div>
    `;
    calcEditSale();
}

function calcEditSale() {
    const bQty = parseFloat(document.getElementById('edit-s-qty').value) || 0;
    const bPrice = parseFloat(document.getElementById('edit-s-price').value) || 0;
    const cQty = parseFloat(document.getElementById('edit-s-cement-qty').value) || 0;
    const cPrice = parseFloat(document.getElementById('edit-s-cement-price').value) || 0;
    const sQty = parseFloat(document.getElementById('edit-s-sand-qty').value) || 0;
    const sPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;
    const delivery = parseFloat(document.getElementById('edit-s-delivery').value) || 0;
    const paid = parseFloat(document.getElementById('edit-s-paid').value) || 0;
    
    const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + delivery;
    const balance = total - paid;
    
    document.getElementById('edit-s-total').textContent = total.toLocaleString();
    document.getElementById('edit-s-balance').textContent = balance.toLocaleString();
}

'''
    js = js[:start_edit] + new_edit + js[end_edit:]

# 3. Replace saveEditedSale
start_save = js.find('function saveEditedSale(saleId) {')
end_save = js.find('function toggleDelivery(id) {')
if start_save != -1 and end_save != -1:
    new_save = '''function saveEditedSale(saleId) {
    const s = sales.find(x => x.id === saleId);
    s.customerName = document.getElementById('edit-s-customer').value || 'Walk-in';
    s.date = document.getElementById('edit-s-date').value;
    s.customerPhone = document.getElementById('edit-s-phone').value;
    s.size = document.getElementById('edit-s-size').value;
    
    s.quantity = parseInt(document.getElementById('edit-s-qty').value) || 0;
    s.pricePerBlock = parseInt(document.getElementById('edit-s-price').value) || 0;
    s.cementQty = parseInt(document.getElementById('edit-s-cement-qty').value) || 0;
    s.cementPrice = parseFloat(document.getElementById('edit-s-cement-price').value) || 0;
    s.sandQty = parseInt(document.getElementById('edit-s-sand-qty').value) || 0;
    s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;
    
    s.deliveryCharge = parseInt(document.getElementById('edit-s-delivery').value) || 0;
    s.amountPaidAtSale = parseInt(document.getElementById('edit-s-paid').value) || 0;
    
    s.totalAmount = (s.quantity * s.pricePerBlock) + (s.cementQty * s.cementPrice) + (s.sandQty * s.sandPrice) + s.deliveryCharge;
    s.balanceOwing = s.totalAmount - s.amountPaidAtSale;
    
    saveData('sales', sales); closeModal(); nav('sales'); showToast('Sale updated successfully', 'success');
}

'''
    js = js[:start_save] + new_save + js[end_save:]

with open('app.js', 'w') as f: f.write(js)

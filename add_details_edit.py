with open('index.html', 'r') as f: html = f.read()

# 1. Make Sales History clickable
html = html.replace(
    '<div class="list-item">\n                    <div class="list-header">\n                        <span>${s.customerName}</span>',
    '<div class="list-item" style="cursor:pointer;" onclick="openSaleDetails(\'${s.id}\')">\n                    <div class="list-header">\n                        <span>${s.customerName}</span>'
)

# 2. Make Production History clickable
html = html.replace(
    '<div class="list-item ${isCuring ? \'curing\' : \'\'}">\n                <div class="list-header">',
    '<div class="list-item ${isCuring ? \'curing\' : \'\'}" style="cursor:pointer;" onclick="openBatchDetails(\'${b.id}\')">\n                <div class="list-header">'
)

# 3. Inject the new functions before the Debts module
new_functions = '''
    // --- Details & Edit Modals ---
    function openSaleDetails(saleId) {
        const s = sales.find(x => x.id === saleId);
        if (!s) return;
        const t = i18n[settings.lang];
        document.getElementById('modal-body').innerHTML = `
            <h3>Receipt · ${s.customerName}</h3>
            <div style="text-align:center; margin-bottom:20px;">
                <p style="font-size:13px; color:var(--muted);">${s.date} · ${s.size}" × ${s.quantity}</p>
                <p style="font-size:28px; font-weight:800; color:var(--brand); margin-top:8px;">${formatNaira(s.totalAmount)}</p>
                ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Owing ${formatNaira(s.balanceOwing)}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
            </div>
            <div class="kv"><span>Price per Block</span><strong>${formatNaira(s.pricePerBlock)}</strong></div>
            <div class="kv"><span>Delivery Charge</span><strong>${formatNaira(s.deliveryCharge)}</strong></div>
            <div class="kv"><span>Amount Paid</span><strong>${formatNaira(s.amountPaidAtSale)}</strong></div>
            <div class="kv"><span>Phone</span><strong>${s.customerPhone || 'N/A'}</strong></div>
            <div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
            </div>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function editSale(saleId) {
        const s = sales.find(x => x.id === saleId);
        document.getElementById('modal-body').innerHTML = `
            <h3>Edit Sale</h3>
            <div class="form-group"><label>Customer</label><input type="text" id="edit-s-customer" value="${s.customerName}"></div>
            <div class="row">
                <div class="form-group"><label>Date</label><input type="date" id="edit-s-date" value="${s.date}"></div>
                <div class="form-group"><label>Phone</label><input type="tel" id="edit-s-phone" value="${s.customerPhone || ''}"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Size</label><select id="edit-s-size"><option value="4" ${s.size==='4'?'selected':''}>4"</option><option value="6" ${s.size==='6'?'selected':''}>6"</option><option value="9" ${s.size==='9'?'selected':''}>9"</option></select></div>
                <div class="form-group"><label>Qty</label><input type="number" id="edit-s-qty" value="${s.quantity}" oninput="calcEditSale()"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Price</label><input type="number" id="edit-s-price" value="${s.pricePerBlock}" oninput="calcEditSale()"></div>
                <div class="form-group"><label>Delivery</label><input type="number" id="edit-s-delivery" value="${s.deliveryCharge}" oninput="calcEditSale()"></div>
            </div>
            <div class="form-group"><label>Paid</label><input type="number" id="edit-s-paid" value="${s.amountPaidAtSale}" oninput="calcEditSale()"></div>
            <div class="calc-box">
                <div class="line"><span>Total</span> <span>₦<span id="edit-s-total">0</span></span></div>
                <div class="line" style="color:var(--danger);"><span>Balance</span> <span>₦<span id="edit-s-balance">0</span></span></div>
            </div>
            <div class="row">
                <button class="btn btn-outline" onclick="openSaleDetails('${s.id}')">Back</button>
                <button class="btn" onclick="saveEditedSale('${s.id}')">Save Changes</button>
            </div>
        `;
        calcEditSale();
    }

    function calcEditSale() {
        const qty = parseFloat(document.getElementById('edit-s-qty').value) || 0;
        const price = parseFloat(document.getElementById('edit-s-price').value) || 0;
        const delivery = parseFloat(document.getElementById('edit-s-delivery').value) || 0;
        const paid = parseFloat(document.getElementById('edit-s-paid').value) || 0;
        const total = (qty * price) + delivery;
        const balance = total - paid;
        document.getElementById('edit-s-total').textContent = total.toLocaleString();
        document.getElementById('edit-s-balance').textContent = balance.toLocaleString();
    }

    function saveEditedSale(saleId) {
        const s = sales.find(x => x.id === saleId);
        s.customerName = document.getElementById('edit-s-customer').value || 'Walk-in';
        s.date = document.getElementById('edit-s-date').value;
        s.customerPhone = document.getElementById('edit-s-phone').value;
        s.size = document.getElementById('edit-s-size').value;
        s.quantity = parseInt(document.getElementById('edit-s-qty').value) || 0;
        s.pricePerBlock = parseInt(document.getElementById('edit-s-price').value) || 0;
        s.deliveryCharge = parseInt(document.getElementById('edit-s-delivery').value) || 0;
        s.amountPaidAtSale = parseInt(document.getElementById('edit-s-paid').value) || 0;
        s.totalAmount = (s.quantity * s.pricePerBlock) + s.deliveryCharge;
        s.balanceOwing = s.totalAmount - s.amountPaidAtSale;
        
        saveData('sales', sales);
        closeModal();
        nav('sales');
        showToast('Sale updated successfully', 'success');
    }

    function openBatchDetails(batchId) {
        const b = batches.find(x => x.id === batchId);
        if (!b) return;
        document.getElementById('modal-body').innerHTML = `
            <h3>Batch Details · ${b.size}"</h3>
            <div class="kv"><span>Date</span><strong>${b.date}</strong></div>
            <div class="kv"><span>Worker</span><strong>${b.worker}</strong></div>
            <div class="kv"><span>Produced</span><strong>${b.blocksProduced} pcs</strong></div>
            <div class="kv"><span>Breakages</span><strong class="neg">${b.breakages} pcs</strong></div>
            <div class="kv"><span>Curing Loss</span><strong class="neg">${b.curingLoss} pcs</strong></div>
            <div class="eyebrow">Financials</div>
            <div class="kv"><span>Total Cost</span><strong>${formatNaira(b.totalCost)}</strong></div>
            <div class="kv"><span>Cost per Block</span><strong class="pos">${formatNaira(b.costPerBlock)}</strong></div>
            <div class="kv"><span>Status</span><span class="tag ${b.status==='curing'?'blue':'green'}">${b.status.toUpperCase()}</span></div>
            <div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editBatch('${b.id}')">Edit Batch</button>
            </div>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function editBatch(batchId) {
        const b = batches.find(x => x.id === batchId);
        document.getElementById('modal-body').innerHTML = `
            <h3>Edit Batch</h3>
            <div class="row">
                <div class="form-group"><label>Date</label><input type="date" id="edit-b-date" value="${b.date}"></div>
                <div class="form-group"><label>Size</label><select id="edit-b-size"><option value="4" ${b.size==='4'?'selected':''}>4"</option><option value="6" ${b.size==='6'?'selected':''}>6"</option><option value="9" ${b.size==='9'?'selected':''}>9"</option></select></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Worker</label><input type="text" id="edit-b-worker" value="${b.worker}"></div>
                <div class="form-group"><label>Blocks Produced</label><input type="number" id="edit-b-blocks" value="${b.blocksProduced}" oninput="calcEditBatch()"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Total Batch Cost (₦)</label><input type="number" id="edit-b-totalcost" value="${b.totalCost}" oninput="calcEditBatch()"></div>
                <div class="form-group"><label>Breakages</label><input type="number" id="edit-b-breakages" value="${b.breakages}"></div>
            </div>
            <div class="form-group"><label>Curing Loss</label><input type="number" id="edit-b-curing-loss" value="${b.curingLoss}"></div>
            
            <div class="calc-box">
                <div class="line pos"><span>Cost per Block</span> <span>₦<span id="edit-b-cpb">0.00</span></span></div>
            </div>
            <div class="row">
                <button class="btn btn-outline" onclick="openBatchDetails('${b.id}')">Back</button>
                <button class="btn" onclick="saveEditedBatch('${b.id}')">Save Changes</button>
            </div>
        `;
        calcEditBatch();
    }

    function calcEditBatch() {
        const totalCost = parseFloat(document.getElementById('edit-b-totalcost').value) || 0;
        const blocks = parseFloat(document.getElementById('edit-b-blocks').value) || 0;
        const cpb = blocks > 0 ? (totalCost / blocks) : 0;
        document.getElementById('edit-b-cpb').textContent = cpb.toFixed(2);
    }

    function saveEditedBatch(batchId) {
        const b = batches.find(x => x.id === batchId);
        b.date = document.getElementById('edit-b-date').value;
        b.size = document.getElementById('edit-b-size').value;
        b.worker = document.getElementById('edit-b-worker').value || 'Unknown';
        b.blocksProduced = parseInt(document.getElementById('edit-b-blocks').value) || 0;
        b.breakages = parseInt(document.getElementById('edit-b-breakages').value) || 0;
        b.curingLoss = parseInt(document.getElementById('edit-b-curing-loss').value) || 0;
        b.totalCost = parseFloat(document.getElementById('edit-b-totalcost').value) || 0;
        b.costPerBlock = b.blocksProduced > 0 ? (b.totalCost / b.blocksProduced) : 0;
        
        saveData('batches', batches);
        closeModal();
        nav('production');
        showToast('Batch updated successfully', 'success');
    }

    // --- Debts Module ---
'''
html = html.replace('// --- Debts Module ---', new_functions)

with open('index.html', 'w') as f: f.write(html)

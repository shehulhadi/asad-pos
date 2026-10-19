import re
with open('index.html', 'r') as f: html = f.read()

# 1. Completely replace renderSales
start_render = html.find('    function renderSales(main) {')
end_render = html.find('    function calcSale() {')
if start_render != -1 and end_render != -1:
    new_render = '''    function renderSales(main) { 
        const t = i18n[settings.lang];
        let historyHtml = '';
        const recentSales = [...sales].reverse().slice(0, 15);
        recentSales.forEach(s => {
            historyHtml += `
                <div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')">
                    <div class="list-header">
                        <span>${s.customerName}</span>
                        <strong class="pos">${formatNaira(s.totalAmount)}</strong>
                    </div>
                    <div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div>
                    <div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">
                        ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}
                        ${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending Delivery</span>`}
                    </div>
                </div>
            `;
        });

        main.innerHTML = `
            <div class="card">
                <h3>${ico('plus')} ${t.newSale}</h3>
                <div class="form-group"><label>${t.customer}</label><input type="text" id="s-customer" list="customer-names" placeholder="Name" oninput="autofillPhone(this.value)"><datalist id="customer-names"></datalist></div>
                <div class="row">
                    <div class="form-group"><label>${t.date}</label><input type="date" id="s-date" value="${getTodayStr()}"></div>
                    <div class="form-group"><label>${t.phone}</label><input type="tel" id="s-phone" placeholder="e.g. 08012345678"></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>${t.size}</label><select id="s-size" onchange="updateDefaultPrice()"><option value="4">4"</option><option value="6">6"</option><option value="9">9"</option></select></div>
                    <div class="form-group"><label>${t.qty}</label><input type="number" id="s-qty" value="1" min="1" oninput="calcSale()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 50, 'calcSale')">+50</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 100, 'calcSale')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('s-qty', 500, 'calcSale')">+500</button></div></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>${t.price}</label><input type="number" id="s-price" value="0" oninput="calcSale()"></div>
                    <div class="form-group"><label>${t.delivery}</label><input type="number" id="s-delivery" value="0" oninput="calcSale()"></div>
                </div>
                
                <div class="eyebrow">Materials Used (Optional)</div>
                <div class="row">
                    <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="s-cement-qty" placeholder="0"></div>
                    <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="s-cement-price" placeholder="0"></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" placeholder="0"></div>
                    <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" placeholder="0"></div>
                </div>

                <div class="form-group"><label>${t.paid}</label><input type="number" id="s-paid" value="0" oninput="calcSale()"></div>
                
                <div class="calc-box">
                    <div class="line"><span>${t.total}</span> <span>₦<span id="s-total-display">0</span></span></div>
                    <div class="line" style="color:var(--danger);"><span>${t.balance}</span> <span>₦<span id="s-balance-display">0</span></span></div>
                </div>

                <button class="btn" style="margin-top:0;" onclick="saveSale()">${t.save}</button>
            </div>

            <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;">
                <span>${ico('sales')} ${t.salesHistory}</span>
                <button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn || 'Log Return'}</button>
            </div>
            <div class="form-group" style="margin-bottom:12px;">
                <input type="text" id="search-sales" placeholder="Search by customer name or date..." oninput="filterSales(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;">
            </div>
            <div id="sales-history-list">
                ${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}
            </div>
        `;
        
        const uniqueCustomers = {};
        sales.forEach(s => { if(s.customerName && s.customerPhone) uniqueCustomers[s.customerName] = s.customerPhone; });
        document.getElementById('customer-names').innerHTML = Object.keys(uniqueCustomers).map(name => `<option value="${name}"></option>`).join('');
        calcSale();
    }

'''
    html = html[:start_render] + new_render + html[end_render:]

# 2. Completely replace saveSale and executeSaveSale
start_save = html.find('    function saveSale() {')
end_save = html.find('    function openReturn() {')
if start_save != -1 and end_save != -1:
    new_save = '''    function saveSale() {
        try {
            const qty = parseInt(document.getElementById('s-qty').value) || 0;
            const price = parseInt(document.getElementById('s-price').value) || 0;
            const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
            const paid = parseInt(document.getElementById('s-paid').value) || 0;
            const saleDate = document.getElementById('s-date').value || getTodayStr();
            const custName = document.getElementById('s-customer').value || 'Walk-in';
            
            if(qty <= 0) return showToast('Enter valid quantity', 'err');

            const total = (qty * price) + delivery;
            const balance = total - paid;

            // Credit Limit Check
            const limit = (settings.creditLimits && settings.creditLimits[custName]) ? settings.creditLimits[custName] : 0;
            if (limit > 0) {
                const existingOwed = sales.filter(s => s.customerName === custName).reduce((sum, s) => sum + (s.balanceOwing || 0), 0);
                if (existingOwed + balance > limit) {
                    showDialog("Credit Limit Exceeded", `Total debt for <strong>${custName}</strong> will be <strong>${formatNaira(existingOwed + balance)}</strong>, exceeding their limit of <strong>${formatNaira(limit)}</strong>.<br><br>Proceed anyway?`, () => {
                        executeSaveSale(qty, price, delivery, paid, saleDate, custName);
                    });
                    return;
                }
            }
            executeSaveSale(qty, price, delivery, paid, saleDate, custName);
        } catch (e) {
            console.error(e);
            showToast("Error saving sale: " + e.message, "err");
        }
    }

    function executeSaveSale(qty, price, delivery, paid, saleDate, custName) {
        try {
            const total = (qty * price) + delivery;
            const balance = total - paid;

            const manCementQty = parseInt(document.getElementById('s-cement-qty').value) || 0;
            const manCementPrice = parseFloat(document.getElementById('s-cement-price').value) || 0;
            const manSandQty = parseInt(document.getElementById('s-sand-qty').value) || 0;
            const manSandPrice = parseFloat(document.getElementById('s-sand-price').value) || 0;

            let maxInv = 0;
            sales.forEach(s => {
                if(s.invoiceNo && typeof s.invoiceNo === 'string') {
                    const num = parseInt(s.invoiceNo.replace('INV-', ''));
                    if(!isNaN(num) && num > maxInv) maxInv = num;
                }
            });
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
                deliveryCharge: delivery, 
                totalAmount: total, 
                amountPaidAtSale: paid, 
                balanceOwing: balance, 
                deliveryStatus: 'pending',
                cementQty: manCementQty,
                cementPrice: manCementPrice,
                sandQty: manSandQty,
                sandPrice: manSandPrice
            };
            
            sales.push(sale); 
            saveData('sales', sales);
            
            if (navigator.vibrate) navigator.vibrate(50);
            
            const todayStr = getTodayStr();
            const todayTotal = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
            if (todayTotal > (settings.bestDayAmount || 0)) {
                settings.bestDayAmount = todayTotal;
                saveData('settings', settings);
                triggerConfetti();
                showToast(`🏆 NEW BEST DAY! ${formatNaira(todayTotal)}`, 'success');
            }

            const waText = buildWhatsAppReceipt(sale);
            const waPhone = (sale.customerPhone || '').replace(/^0/, '234');
            const waLink = `https://wa.me/${waPhone}?text=${waText}`;

            const matString = `${sale.cementQty > 0 ? sale.cementQty + ' bags cement (₦' + sale.cementPrice + ')' : Math.ceil(sale.quantity / (settings.mixCement || 50)) + ' bags cement (est)'}${sale.sandQty > 0 ? ', ' + sale.sandQty + ' bags sand (₦' + sale.sandPrice + ')' : ', ' + Math.ceil(sale.quantity / (settings.mixSand || 500)) + ' bags sand (est)'}`;

            document.getElementById('modal-body').innerHTML = `
                <div style="text-align:center; margin-bottom:20px;">
                    <div style="width:48px; height:48px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 10px;"><svg class="ic" style="width:24px;height:24px;stroke-width:2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                    <h3 style="margin-bottom:2px;">Sale Recorded</h3>
                    <p style="font-size:12px; color:var(--muted);">${new Date().toLocaleString()}</p>
                </div>

                <div class="kv"><span>Invoice No.</span><strong>${sale.invoiceNo}</strong></div>
                <div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>
                <div class="kv"><span>Item</span><strong>${sale.quantity} pcs of ${sale.size}" Blocks</strong></div>
                <div class="kv"><span>Materials</span><strong>${matString}</strong></div>
                <div class="kv"><span>Price per Block</span><strong>${formatNaira(sale.pricePerBlock)}</strong></div>
                <div class="kv"><span>Delivery Charge</span><strong>${formatNaira(sale.deliveryCharge)}</strong></div>
                
                <div class="kv" style="border-bottom:2px solid var(--line); padding-bottom:12px; margin-bottom:12px; margin-top:8px;">
                    <span style="font-size:16px; font-weight:800;">Total Amount</span>
                    <strong style="font-size:20px; color:var(--brand); font-weight:800;">${formatNaira(total)}</strong>
                </div>
                
                <div class="kv"><span>Amount Paid</span><strong>${formatNaira(sale.amountPaidAtSale)}</strong></div>
                <div class="kv" style="border-bottom:none;"><span>Outstanding Balance</span><strong style="color:${balance > 0 ? 'var(--danger)' : 'var(--brand)'}; font-size:16px;">${formatNaira(balance)}</strong></div>
                
                <div class="actions" style="margin-top:24px; margin-bottom:10px;">
                    <a href="${waLink}" target="_blank"><button class="wa" style="padding:14px; font-size:15px;">WhatsApp</button></a>
                    <button onclick="shareReceiptImage('${sale.id}')" style="padding:14px; font-size:15px; background:var(--accent); color:#fff; border:none;">📸 Image</button>
                </div>
                <div class="row">
                    <button class="btn btn-outline" onclick="printDocument()">Print</button>
                    <button class="btn btn-outline" onclick="closeModal(); nav('sales')">Close</button>
                </div>`;
            document.getElementById('modal').classList.add('active');
        } catch (e) {
            console.error(e);
            showToast("Error: " + e.message, "err");
        }
    }

'''
    html = html[:start_save] + new_save + html[end_save:]

# 3. Completely replace editSale and saveEditedSale
start_edit = html.find('    function editSale(saleId) {')
end_edit = html.find('    function openBatchDetails(batchId) {')
if start_edit != -1 and end_edit != -1:
    new_edit = '''    function editSale(saleId) {
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
            
            <div class="eyebrow">Materials Used</div>
            <div class="row">
                <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="edit-s-cement-qty" value="${s.cementQty || ''}" placeholder="0"></div>
                <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="edit-s-cement-price" value="${s.cementPrice || ''}" placeholder="0"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0"></div>
                <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0"></div>
            </div>

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
        
        s.cementQty = parseInt(document.getElementById('edit-s-cement-qty').value) || 0;
        s.cementPrice = parseFloat(document.getElementById('edit-s-cement-price').value) || 0;
        s.sandQty = parseInt(document.getElementById('edit-s-sand-qty').value) || 0;
        s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;

        s.totalAmount = (s.quantity * s.pricePerBlock) + s.deliveryCharge;
        s.balanceOwing = s.totalAmount - s.amountPaidAtSale;
        
        saveData('sales', sales);
        closeModal();
        nav('sales');
        showToast('Sale updated successfully', 'success');
    }

'''
    html = html[:start_edit] + new_edit + html[end_edit:]

# 4. Update buildWhatsAppReceipt to use the new logic safely
old_wa_func = re.search(r'    function buildWhatsAppReceipt\(sale\) \{.*?\n    \}', html, re.DOTALL).group(0)
new_wa_func = '''    function buildWhatsAppReceipt(sale) {
        const matString = `${sale.cementQty > 0 ? sale.cementQty + ' bags cement (₦' + sale.cementPrice + ')' : Math.ceil(sale.quantity / (settings.mixCement || 50)) + ' bags cement (est)'}${sale.sandQty > 0 ? ', ' + sale.sandQty + ' bags sand (₦' + sale.sandPrice + ')' : ', ' + Math.ceil(sale.quantity / (settings.mixSand || 500)) + ' bags sand (est)'}`;
        return encodeURIComponent(
            `*🧱 ${settings.businessName.toUpperCase()}*\\n` +
            `📞 ${settings.businessPhone || 'N/A'}\\n` +
            `--------------------------------\\n` +
            `*INVOICE / RECEIPT*\\n` +
            `Invoice No: ${sale.invoiceNo || 'N/A'}\\n` +
            `Date: ${sale.date} ${sale.createdAt ? new Date(sale.createdAt).toLocaleTimeString() : ''}\\n` +
            `Customer: ${sale.customerName}\\n` +
            `--------------------------------\\n` +
            `Item: ${sale.quantity} pcs of ${sale.size}" Blocks\\n` +
            `Materials: ${matString}\\n` +
            `Price/Block: ₦${sale.pricePerBlock.toLocaleString()}\\n` +
            `Delivery: ₦${sale.deliveryCharge.toLocaleString()}\\n` +
            `*Total Amount: ₦${sale.totalAmount.toLocaleString()}*\\n` +
            `Amount Paid: ₦${sale.amountPaidAtSale.toLocaleString()}\\n` +
            `*Outstanding Balance: ₦${sale.balanceOwing.toLocaleString()}*\\n` +
            `--------------------------------\\n` +
            `Thank you for your patronage! 🙏`
        );
    }'''
html = html.replace(old_wa_func, new_wa_func)

# 5. Update Canvas Receipt safely
old_canvas = re.search(r'            // Materials Used.*?ctx\.fillText\(`Materials: .*?`, 40, 440\);', html, re.DOTALL)
if old_canvas:
    new_canvas = '''            // Materials Used
            const matString = `${s.cementQty > 0 ? s.cementQty + ' bags cement (₦' + s.cementPrice + ')' : Math.ceil(s.quantity / (settings.mixCement || 50)) + ' bags cement (est)'}${s.sandQty > 0 ? ', ' + s.sandQty + ' bags sand (₦' + s.sandPrice + ')' : ', ' + Math.ceil(s.quantity / (settings.mixSand || 500)) + ' bags sand (est)'}`;
            ctx.textAlign = 'left';
            ctx.fillStyle = '#64748b';
            ctx.font = '14px Arial';
            ctx.fillText(`Materials: ${matString}`, 40, 440);'''
    html = html.replace(old_canvas.group(0), new_canvas)

with open('index.html', 'w') as f: f.write(html)

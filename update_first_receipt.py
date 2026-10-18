import re
with open('index.html', 'r') as f: html = f.read()

# Find the exact modal injection inside saveSale()
old_modal = '''        document.getElementById('modal-body').innerHTML = `
            <div style="text-align:center; padding:6px 0 18px;">
                <div style="width:56px; height:56px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 14px;"><svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                <h3 style="margin-bottom:4px;">Sale Recorded</h3>
                <p style="font-size:13px; color:var(--muted);">${sale.customerName} · ${sale.size}" × ${sale.quantity}</p>
                <p style="font-size:32px; font-weight:800; letter-spacing:-1px; margin-top:12px;">₦${total.toLocaleString()}</p>
                ${balance > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Balance ₦${balance.toLocaleString()}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
            </div>
            <div class="actions">
                <a href="${waLink}" target="_blank"><button class="wa" style="padding:14px; font-size:15px;">WhatsApp</button></a>
                <button onclick="printDocument()" style="padding:14px; font-size:15px;">Print</button>
            </div>
            <button class="btn btn-outline" style="margin-top:14px;" onclick="closeModal(); nav('sales')">Close</button>`;'''

new_modal = '''        document.getElementById('modal-body').innerHTML = `
            <div style="text-align:center; margin-bottom:20px;">
                <div style="width:48px; height:48px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 10px;"><svg class="ic" style="width:24px;height:24px;stroke-width:2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                <h3 style="margin-bottom:2px;">Sale Recorded</h3>
                <p style="font-size:12px; color:var(--muted);">${new Date().toLocaleString()}</p>
            </div>

            <div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>
            <div class="kv"><span>Item</span><strong>${sale.quantity} pcs of ${sale.size}" Blocks</strong></div>
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
                <button onclick="printDocument()" style="padding:14px; font-size:15px;">Print</button>
            </div>
            <button class="btn btn-outline" onclick="closeModal(); nav('sales')">Close</button>`;'''

html = html.replace(old_modal, new_modal)

with open('index.html', 'w') as f: f.write(html)

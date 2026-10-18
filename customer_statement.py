import re
with open('index.html', 'r') as f: html = f.read()

# 1. Make Customer Debt items clickable in renderDebts
old_cust_list = '''<div class="list-item owing">
                        <div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div>'''
new_cust_list = '''<div class="list-item owing" style="cursor:pointer;" onclick="openCustomerStatement('${s.customerName.replace(/'/g, "\\'")}')">
                        <div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div>'''
html = html.replace(old_cust_list, new_cust_list)

# 2. Make sure filterDebts also gets the clickable behavior
old_filter_cust = '''<div class="list-item owing">
                        <div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div>'''
new_filter_cust = '''<div class="list-item owing" style="cursor:pointer;" onclick="openCustomerStatement('${s.customerName.replace(/'/g, "\\'")}')">
                        <div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div>'''
html = html.replace(old_filter_cust, new_filter_cust)

# 3. Inject the Ledger functions
ledger_functions = '''
    // --- Customer Statement / Ledger ---
    function openCustomerStatement(custName) {
        const custSales = sales.filter(s => s.customerName === custName);
        const saleIds = custSales.map(s => s.id);
        const custPayments = payments.filter(p => saleIds.includes(p.saleId));
        
        const totalBought = custSales.reduce((sum, s) => sum + s.totalAmount, 0);
        const totalPaidAtSale = custSales.reduce((sum, s) => sum + s.amountPaidAtSale, 0);
        const totalExtraPayments = custPayments.reduce((sum, p) => sum + p.amount, 0);
        const totalPaid = totalPaidAtSale + totalExtraPayments;
        const totalOwing = custSales.reduce((sum, s) => sum + s.balanceOwing, 0);
        
        const phone = custSales.find(s => s.customerPhone)?.customerPhone || '';

        // Build transaction history (Sales + Payments merged and sorted)
        let history = [];
        custSales.forEach(s => {
            history.push({ date: s.date, type: 'sale', desc: `${s.size}" Blocks × ${s.quantity}`, amt: s.totalAmount, color: 'var(--text)' });
            if (s.amountPaidAtSale > 0) {
                history.push({ date: s.date, type: 'payment', desc: `Paid at sale`, amt: s.amountPaidAtSale, color: 'var(--brand)' });
            }
        });
        custPayments.forEach(p => {
            history.push({ date: p.date, type: 'payment', desc: `Payment received`, amt: p.amount, color: 'var(--brand)' });
        });
        history.sort((a, b) => new Date(a.date) - new Date(b.date));

        let historyHtml = history.map(h => `
            <div class="kv" style="font-size:13px;">
                <span>${h.date} · ${h.desc}</span>
                <strong style="color:${h.color};">${h.type === 'sale' ? '+' : '-'}${formatNaira(h.amt)}</strong>
            </div>
        `).join('');

        document.getElementById('modal-body').innerHTML = `
            <h3>${custName}</h3>
            <p style="font-size:13px; color:var(--muted); margin-top:-10px; margin-bottom:16px;">📞 ${phone || 'No phone saved'}</p>
            
            <div class="calc-box" style="background:#f8fafc; border-color:var(--line);">
                <div class="line" style="color:var(--text);"><span>Total Purchases</span> <span>${formatNaira(totalBought)}</span></div>
                <div class="line" style="color:var(--brand);"><span>Total Paid</span> <span>${formatNaira(totalPaid)}</span></div>
                <div class="line" style="color:var(--danger); font-size:16px; border-top:1px solid var(--line); padding-top:6px; margin-top:6px;"><span>Outstanding</span> <span>${formatNaira(totalOwing)}</span></div>
            </div>

            <div class="eyebrow">Transaction History</div>
            <div style="max-height:200px; overflow-y:auto; margin-bottom:16px; border:1px solid var(--line); border-radius:8px; padding:0 12px;">
                ${historyHtml || '<p style="font-size:13px; color:var(--muted); padding:12px 0;">No transactions yet.</p>'}
            </div>

            <div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" style="background:#25D366; color:#fff;" onclick="shareStatement('${custName.replace(/'/g, "\\'")}', '${phone.replace(/'/g, "\\'")}', ${totalBought}, ${totalPaid}, ${totalOwing})">Send Statement</button>
            </div>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function shareStatement(custName, phone, bought, paid, owing) {
        const waPhone = phone.replace(/^0/, '234');
        const msg = encodeURIComponent(`*🧱 ${settings.businessName.toUpperCase()}*\\n📞 ${settings.businessPhone || 'N/A'}\\n--------------------------------\\n*STATEMENT OF ACCOUNT*\\nCustomer: ${custName}\\nDate: ${new Date().toISOString().split('T')[0]}\\n--------------------------------\\n*Total Purchases:* ₦${bought.toLocaleString()}\\n*Total Paid:* ₦${paid.toLocaleString()}\\n--------------------------------\\n*OUTSTANDING BALANCE: ₦${owing.toLocaleString()}*\\n--------------------------------\\nPlease kindly settle your outstanding balance.\\nThank you for your patronage! 🙏`);
        
        if (waPhone && waPhone.length > 5) {
            window.open(`https://wa.me/${waPhone}?text=${msg}`, '_blank');
        } else {
            navigator.clipboard.writeText(msg).then(() => showToast('No phone saved. Statement copied to clipboard!', 'success'));
        }
    }
'''
html = html.replace('// --- Details & Edit Modals ---', ledger_functions + '\n// --- Details & Edit Modals ---')

with open('index.html', 'w') as f: f.write(html)

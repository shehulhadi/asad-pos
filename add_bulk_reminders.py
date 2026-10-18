import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add the "Generate Bulk Reminder" button to the Customer Debts tab
old_cust_tab = '''        if (currentDebtTab === 'customer') {
            if (owingSales.length === 0) { 
                html += `<div class="empty">No outstanding customer debts.</div>`; 
            } else {'''
new_cust_tab = '''        if (currentDebtTab === 'customer') {
            if (owingSales.length > 0) {
                html += `<button class="btn btn-dark" style="margin-bottom: 16px;" onclick="generateBulkReminder()">📢 Generate Bulk Reminder List</button>`;
            }
            if (owingSales.length === 0) { 
                html += `<div class="empty">No outstanding customer debts.</div>`; 
            } else {'''
html = html.replace(old_cust_tab, new_cust_tab)

# 2. Inject the Bulk Reminder Logic
bulk_js = '''
    // --- Bulk Debt Reminders ---
    function generateBulkReminder() {
        const owingSales = sales.filter(s => s.balanceOwing > 0);
        if (owingSales.length === 0) return showToast('No outstanding debts to remind.', 'err');

        // Group debts by customer name
        const debtors = {};
        owingSales.forEach(s => {
            debtors[s.customerName] = (debtors[s.customerName] || 0) + s.balanceOwing;
        });

        let msg = `*🧱 ${settings.businessName.toUpperCase()}*\\n📞 ${settings.businessPhone || 'N/A'}\\n--------------------------------\\n*DEBT REMINDER LIST*\\nDate: ${new Date().toISOString().split('T')[0]}\\n--------------------------------\\n`;
        let total = 0;
        Object.keys(debtors).sort((a,b) => debtors[b] - debtors[a]).forEach(name => {
            msg += `- ${name}: ₦${debtors[name].toLocaleString()}\\n`;
            total += debtors[name];
        });
        msg += `--------------------------------\\n*Total Outstanding: ₦${total.toLocaleString()}*\\n\\nPlease kindly settle your outstanding balances. Thank you! 🙏`;

        document.getElementById('modal-body').innerHTML = `
            <h3>Bulk Reminder</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Copy this list to send in a WhatsApp group, or share it directly.</p>
            <textarea id="bulk-reminder-text" style="width:100%; height:220px; font-family:monospace; font-size:13px; padding:12px; border-radius:8px; border:1.5px solid var(--line); margin-bottom:16px; background:#f8fafc;" readonly>${msg}</textarea>
            <div class="row">
                <button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('bulk-reminder-text').value).then(()=>showToast('Copied to clipboard!','success'))">📋 Copy</button>
                <button class="btn" style="background:#25D366; color:#fff;" onclick="shareBulkReminder()">📤 Share</button>
            </div>
            <button class="btn btn-outline" style="margin-top:8px;" onclick="closeModal()">Close</button>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function shareBulkReminder() {
        const text = document.getElementById('bulk-reminder-text').value;
        if (navigator.share) {
            navigator.share({ title: 'Debt Reminders', text: text })
                .then(() => showToast('Shared successfully', 'success'))
                .catch(e => console.log(e));
        } else {
            navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard instead!', 'success'));
        }
    }

    // --- Debts Module ---
'''
html = html.replace('// --- Debts Module ---', bulk_js)

with open('index.html', 'w') as f: f.write(html)

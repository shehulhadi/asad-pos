import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add createdAt to new sales
html = html.replace(
    "const sale = { id: Date.now().toString(), invoiceNo: nextInv, date: saleDate,",
    "const sale = { id: Date.now().toString(), createdAt: new Date().toISOString(), invoiceNo: nextInv, date: saleDate,"
)

# 2. Add Time to the Sale Details Modal (History)
old_details = '''<div class="kv"><span>Invoice No.</span><strong>${s.invoiceNo || 'N/A'}</strong></div>
            <div class="kv"><span>Price per Block</span><strong>${formatNaira(s.pricePerBlock)}</strong></div>'''
new_details = '''<div class="kv"><span>Invoice No.</span><strong>${s.invoiceNo || 'N/A'}</strong></div>
            <div class="kv"><span>Time</span><strong>${s.createdAt ? new Date(s.createdAt).toLocaleTimeString() : 'N/A'}</strong></div>
            <div class="kv"><span>Price per Block</span><strong>${formatNaira(s.pricePerBlock)}</strong></div>'''
html = html.replace(old_details, new_details)

# 3. Add Time to WhatsApp Receipt
old_wa = '''`*INVOICE / RECEIPT*\\n` +
            `Invoice No: ${sale.invoiceNo || 'N/A'}\\n` +
            `Date: ${sale.date}\\n` +'''
new_wa = '''`*INVOICE / RECEIPT*\\n` +
            `Invoice No: ${sale.invoiceNo || 'N/A'}\\n` +
            `Date: ${sale.date} ${sale.createdAt ? new Date(sale.createdAt).toLocaleTimeString() : ''}\\n` +'''
html = html.replace(old_wa, new_wa)

# 4. Add Time to Image Receipt (Canvas)
old_canvas = '''        ctx.fillText(s.date, 160, 240);'''
new_canvas = '''        ctx.fillText(s.date + ' ' + (s.createdAt ? new Date(s.createdAt).toLocaleTimeString() : ''), 160, 240);'''
html = html.replace(old_canvas, new_canvas)

# 5. Update Manual Backup filename to include Time
old_manual_backup = '''        const jsonStr = JSON.stringify(data, null, 2);
        const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
        const filename = `${safeName}_Backup_${new Date().toISOString().split('T')[0]}.txt`;'''
new_manual_backup = '''        const jsonStr = JSON.stringify(data, null, 2);
        const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
        const filename = `${safeName}_Backup_${now.toISOString().split('T')[0]}_${timeStr}.txt`;'''
html = html.replace(old_manual_backup, new_manual_backup)

# 6. Update Auto Backup filename to include Time
old_auto_backup = '''                const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
                const a = document.createElement('a');
                a.href = url;
                a.download = `${safeName}_AutoBackup_${new Date().toISOString().split('T')[0]}.json`;'''
new_auto_backup = '''                const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
                const now = new Date();
                const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
                const a = document.createElement('a');
                a.href = url;
                a.download = `${safeName}_AutoBackup_${now.toISOString().split('T')[0]}_${timeStr}.json`;'''
html = html.replace(old_auto_backup, new_auto_backup)

with open('index.html', 'w') as f: f.write(html)

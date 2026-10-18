import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add default prices to settings
html = html.replace(
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500",
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500, defaultPrices: {'4': 0, '6': 0, '9': 0}"
)
if "if(!settings.defaultPrices)" in html:
    html = html.replace(
        "if(settings.mixSand === undefined) settings.mixSand = 500;",
        "if(settings.mixSand === undefined) settings.mixSand = 500;\n    if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};"
    )

# 2. Add Default Prices UI to Settings
old_settings_ui = '''            <div class="eyebrow">Standard Mix Ratios</div>'''
new_settings_ui = '''            <div class="eyebrow">Default Selling Prices (₦)</div>
            <div class="row">
                <div class="form-group"><label>4" Block</label><input type="number" id="set-price-4" value="${settings.defaultPrices['4'] || 0}"></div>
                <div class="form-group"><label>6" Block</label><input type="number" id="set-price-6" value="${settings.defaultPrices['6'] || 0}"></div>
                <div class="form-group"><label>9" Block</label><input type="number" id="set-price-9" value="${settings.defaultPrices['9'] || 0}"></div>
            </div>
            <div class="eyebrow">Standard Mix Ratios</div>'''
html = html.replace(old_settings_ui, new_settings_ui)

# 3. Save Default Prices in saveSettings
old_save = '''        settings.mixCement = parseInt(document.getElementById('set-mix-cement').value) || 50;'''
new_save = '''        settings.defaultPrices = {
            '4': parseFloat(document.getElementById('set-price-4').value) || 0,
            '6': parseFloat(document.getElementById('set-price-6').value) || 0,
            '9': parseFloat(document.getElementById('set-price-9').value) || 0
        };
        settings.mixCement = parseInt(document.getElementById('set-mix-cement').value) || 50;'''
html = html.replace(old_save, new_save)

# 4. Update Sales Form to auto-fill price on size change
old_sales_size = '''<div class="form-group"><label>${t.size}</label><select id="s-size"><option value="4">4"</option><option value="6">6"</option><option value="9">9"</option></select></div>'''
new_sales_size = '''<div class="form-group"><label>${t.size}</label><select id="s-size" onchange="updateDefaultPrice()"><option value="4">4"</option><option value="6">6"</option><option value="9">9"</option></select></div>'''
html = html.replace(old_sales_size, new_sales_size)

# 5. Add updateDefaultPrice JS
price_js = '''
    function updateDefaultPrice() {
        const size = document.getElementById('s-size').value;
        const price = settings.defaultPrices[size] || 0;
        document.getElementById('s-price').value = price;
        calcSale();
    }
'''
html = html.replace('    function calcSale() {', price_js + '\n    function calcSale() {')

# 6. Add "Share Image" buttons to the receipt modals
# In saveSale modal:
html = html.replace(
    '''<button onclick="printDocument()" style="padding:14px; font-size:15px;">Print</button>
            </div>''',
    '''<button onclick="shareReceiptImage('${sale.id}')" style="padding:14px; font-size:15px; background:var(--accent); color:#fff; border:none;">📸 Image</button>
            </div>'''
)
# In openSaleDetails modal:
html = html.replace(
    '''<button onclick="printDocument()">Print</button>
            </div>''',
    '''<button onclick="shareReceiptImage('${s.id}')">📸 Image</button>
            </div>'''
)

# 7. Inject the Canvas Receipt Logic
canvas_js = '''
    function shareReceiptImage(saleId) {
        const s = sales.find(x => x.id === saleId);
        if (!s) return;

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const width = 600;
        const height = 850;
        canvas.width = width;
        canvas.height = height;

        // Background
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = '#059669';
        ctx.fillRect(0, 0, width, 120);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 32px Arial';
        ctx.textAlign = 'center';
        ctx.fillText((settings.businessName || 'MY BUSINESS').toUpperCase(), width / 2, 50);
        ctx.font = '18px Arial';
        ctx.fillText('📞 ' + (settings.businessPhone || ''), width / 2, 85);

        // Details
        ctx.fillStyle = '#0f172a';
        ctx.textAlign = 'left';
        ctx.font = 'bold 24px Arial';
        ctx.fillText('INVOICE / RECEIPT', 40, 170);

        ctx.font = '16px Arial';
        ctx.fillStyle = '#64748b';
        ctx.fillText('Invoice No:', 40, 210);
        ctx.fillText('Date:', 40, 240);
        ctx.fillText('Customer:', 40, 270);

        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 16px Arial';
        ctx.fillText(s.invoiceNo || 'N/A', 160, 210);
        ctx.fillText(s.date, 160, 240);
        ctx.fillText(s.customerName, 160, 270);

        // Line
        ctx.beginPath(); ctx.moveTo(40, 300); ctx.lineTo(560, 300);
        ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 2; ctx.stroke();

        // Table Headers
        ctx.fillStyle = '#64748b';
        ctx.font = 'bold 16px Arial';
        ctx.fillText('Description', 40, 340);
        ctx.textAlign = 'right';
        ctx.fillText('Amount', 560, 340);

        // Item
        ctx.fillStyle = '#0f172a';
        ctx.font = '16px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`${s.quantity} pcs of ${s.size}" Blocks`, 40, 380);
        ctx.fillText(`(@ ₦${s.pricePerBlock.toLocaleString()})`, 40, 405);

        ctx.textAlign = 'right';
        ctx.fillText(`₦${(s.quantity * s.pricePerBlock).toLocaleString()}`, 560, 380);

        // Delivery
        if (s.deliveryCharge > 0) {
            ctx.textAlign = 'left';
            ctx.fillText(`Delivery Charge`, 40, 445);
            ctx.textAlign = 'right';
            ctx.fillText(`₦${s.deliveryCharge.toLocaleString()}`, 560, 445);
        }

        // Line
        ctx.beginPath(); ctx.moveTo(40, 480); ctx.lineTo(560, 480); ctx.stroke();

        // Totals
        ctx.textAlign = 'left';
        ctx.font = 'bold 20px Arial';
        ctx.fillText('Total Amount:', 40, 520);
        ctx.textAlign = 'right';
        ctx.fillStyle = '#059669';
        ctx.fillText(`₦${s.totalAmount.toLocaleString()}`, 560, 520);

        ctx.fillStyle = '#64748b';
        ctx.font = '16px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('Amount Paid:', 40, 560);
        ctx.textAlign = 'right';
        ctx.fillStyle = '#0f172a';
        ctx.fillText(`₦${s.amountPaidAtSale.toLocaleString()}`, 560, 560);

        ctx.fillStyle = '#64748b';
        ctx.textAlign = 'left';
        ctx.fillText('Outstanding Balance:', 40, 600);
        ctx.textAlign = 'right';
        ctx.fillStyle = s.balanceOwing > 0 ? '#dc2626' : '#059669';
        ctx.fillText(`₦${s.balanceOwing.toLocaleString()}`, 560, 600);

        // Footer
        ctx.fillStyle = '#64748b';
        ctx.font = 'italic 16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Thank you for your business!', width / 2, 700);
        ctx.font = '14px Arial';
        ctx.fillText('Powered by Asad Tech Concepts', width / 2, 730);

        // Convert & Share
        canvas.toBlob(function(blob) {
            const file = new File([blob], `Receipt_${s.invoiceNo || s.id}.png`, { type: 'image/png' });
            if (navigator.canShare && navigator.canShare({ files: [file] })) {
                navigator.share({
                    files: [file],
                    title: 'Receipt',
                    text: 'Here is your receipt.'
                }).catch(e => console.log('Share failed', e));
            } else {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Receipt_${s.invoiceNo || s.id}.png`;
                a.click();
                URL.revokeObjectURL(url);
                showToast('Receipt image downloaded', 'success');
            }
        }, 'image/png');
    }
'''
html = html.replace('// --- Details & Edit Modals ---', canvas_js + '\n// --- Details & Edit Modals ---')

with open('index.html', 'w') as f: f.write(html)

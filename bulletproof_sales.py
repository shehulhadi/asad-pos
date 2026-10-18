import re
with open('index.html', 'r') as f: html = f.read()

# Find the start of saveSale and the end of processSaveSale
start_idx = html.find('    function saveSale() {')
end_idx = html.find('    function renderProduction(main) {')

if start_idx != -1 and end_idx != -1:
    new_sales_js = '''    function saveSale() {
        try {
            const qty = parseInt(document.getElementById('s-qty').value) || 0;
            const price = parseInt(document.getElementById('s-price').value) || 0;
            const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
            const paid = parseInt(document.getElementById('s-paid').value) || 0;
            const saleDate = document.getElementById('s-date').value || new Date().toISOString().split('T')[0];
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
                createdAt: new Date().toISOString(), 
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
                deliveryStatus: 'pending' 
            };
            
            sales.push(sale); 
            saveData('sales', sales);
            
            if (navigator.vibrate) navigator.vibrate(50);
            
            const todayStr = new Date().toISOString().split('T')[0];
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

            document.getElementById('modal-body').innerHTML = `
                <div style="text-align:center; margin-bottom:20px;">
                    <div style="width:48px; height:48px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 10px;"><svg class="ic" style="width:24px;height:24px;stroke-width:2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                    <h3 style="margin-bottom:2px;">Sale Recorded</h3>
                    <p style="font-size:12px; color:var(--muted);">${new Date().toLocaleString()}</p>
                </div>

                <div class="kv"><span>Invoice No.</span><strong>${sale.invoiceNo}</strong></div>
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

    // --- Bulletproof Image Sharing ---
    function shareReceiptImage(saleId) {
        try {
            const s = sales.find(x => x.id === saleId);
            if (!s) return showToast('Sale not found', 'err');

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
            ctx.fillText(s.date + ' ' + (s.createdAt ? new Date(s.createdAt).toLocaleTimeString() : ''), 160, 240);
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
                try {
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
                } catch(err) {
                    console.error(err);
                    showToast('Image download error', 'err');
                }
            }, 'image/png');
        } catch (e) {
            console.error(e);
            showToast("Canvas Error: " + e.message, "err");
        }
    }

'''
    html = html[:start_idx] + new_sales_js + html[end_idx:]

with open('index.html', 'w') as f: f.write(html)

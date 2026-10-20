import re
with open('app.js', 'r') as f: js = f.read()

# Locate the shareReceiptImage function and replace it entirely
start = js.find('function shareReceiptImage(saleId) {')
end = js.find('function renderProduction(main) {')

if start != -1 and end != -1:
    new_func = '''function shareReceiptImage(saleId) {
    try {
        const s = sales.find(x => x.id === saleId);
        if (!s) return showToast('Sale not found', 'err');

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const width = 600, height = 900;
        canvas.width = width; canvas.height = height;

        // Background
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = '#059669'; ctx.fillRect(0, 0, width, 120);
        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 32px Arial'; ctx.textAlign = 'center';
        ctx.fillText((settings.businessName || 'MY BUSINESS').toUpperCase(), width / 2, 50);
        ctx.font = '18px Arial'; ctx.fillText('📞 ' + (settings.businessPhone || ''), width / 2, 85);

        // Invoice Info
        ctx.fillStyle = '#0f172a'; ctx.textAlign = 'left'; ctx.font = 'bold 24px Arial';
        ctx.fillText('INVOICE / RECEIPT', 40, 170);

        ctx.font = '16px Arial'; ctx.fillStyle = '#64748b';
        ctx.fillText('Invoice No:', 40, 210); ctx.fillText('Date:', 40, 240); ctx.fillText('Customer:', 40, 270);

        ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial';
        ctx.fillText(s.invoiceNo || 'N/A', 160, 210);
        ctx.fillText(s.date + ' ' + (s.createdAt ? new Date(s.createdAt).toLocaleTimeString() : ''), 160, 240);
        ctx.fillText(s.customerName, 160, 270);

        // Divider
        ctx.beginPath(); ctx.moveTo(40, 300); ctx.lineTo(560, 300); ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 2; ctx.stroke();

        // Table Headers
        ctx.fillStyle = '#64748b'; ctx.font = 'bold 16px Arial'; ctx.textAlign = 'left';
        ctx.fillText('Item Description', 40, 340);
        ctx.textAlign = 'right'; ctx.fillText('Subtotal', 560, 340);

        let yPos = 380;
        let hasItems = false;

        const drawLineItem = (title, qty, price) => {
            if (qty > 0) {
                hasItems = true;
                ctx.textAlign = 'left'; ctx.fillStyle = '#0f172a'; ctx.font = '16px Arial';
                ctx.fillText(`${title} (${qty} @ ₦${price.toLocaleString()})`, 40, yPos);
                ctx.textAlign = 'right'; ctx.font = 'bold 16px Arial';
                ctx.fillText(`₦${(qty * price).toLocaleString()}`, 560, yPos);
                yPos += 30;
            }
        };

        drawLineItem(`${s.size}" Blocks`, s.quantity, s.pricePerBlock);
        drawLineItem(`Cement Bags`, s.cementQty, s.cementPrice);
        drawLineItem(`Sand Bags`, s.sandQty, s.sandPrice);
        drawLineItem(`Empty Bags`, s.emptyBagQty, s.emptyBagPrice);

        if (s.deliveryCharge > 0) {
            hasItems = true;
            ctx.textAlign = 'left'; ctx.fillStyle = '#64748b'; ctx.font = '16px Arial';
            ctx.fillText(`Delivery Charge`, 40, yPos);
            ctx.textAlign = 'right'; ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial';
            ctx.fillText(`₦${s.deliveryCharge.toLocaleString()}`, 560, yPos);
            yPos += 30;
        }

        if (!hasItems) {
            ctx.textAlign = 'left'; ctx.fillStyle = '#64748b'; ctx.font = 'italic 16px Arial';
            ctx.fillText('No items logged.', 40, yPos);
            yPos += 30;
        }

        // Divider
        yPos += 10;
        ctx.beginPath(); ctx.moveTo(40, yPos); ctx.lineTo(560, yPos); ctx.stroke();

        // Totals
        yPos += 40;
        ctx.textAlign = 'left'; ctx.font = 'bold 20px Arial'; ctx.fillText('Total Amount:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = '#059669'; ctx.fillText(`₦${s.totalAmount.toLocaleString()}`, 560, yPos);

        yPos += 40;
        ctx.fillStyle = '#64748b'; ctx.font = '16px Arial'; ctx.textAlign = 'left'; ctx.fillText('Amount Paid:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial'; ctx.fillText(`₦${s.amountPaidAtSale.toLocaleString()}`, 560, yPos);

        yPos += 40;
        ctx.fillStyle = '#64748b'; ctx.textAlign = 'left'; ctx.font = '16px Arial'; ctx.fillText('Outstanding Balance:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = s.balanceOwing > 0 ? '#dc2626' : '#059669'; ctx.font = 'bold 18px Arial'; ctx.fillText(`₦${s.balanceOwing.toLocaleString()}`, 560, yPos);

        // Footer
        ctx.fillStyle = '#64748b'; ctx.font = 'italic 16px Arial'; ctx.textAlign = 'center';
        ctx.fillText('Thank you for your business!', width / 2, height - 80);
        ctx.font = '14px Arial';
        ctx.fillText('Powered by Asad Tech Concepts', width / 2, height - 50);

        canvas.toBlob(function(blob) {
            try {
                const file = new File([blob], 'Receipt_' + (s.invoiceNo || s.id) + '.png', { type: 'image/png' });
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    navigator.share({ files: [file], title: 'Receipt' }).catch(e => console.log(e));
                } else {
                    const url = URL.createObjectURL(blob); const a = document.createElement('a');
                    a.href = url; a.download = 'Receipt_' + (s.invoiceNo || s.id) + '.png'; a.click();
                    URL.revokeObjectURL(url); showToast('Receipt image downloaded', 'success');
                }
            } catch(err) { showToast('Image download error', 'err'); }
        }, 'image/png');
    } catch (e) { showToast("Canvas Error: " + e.message, "err"); }
}

'''
    js = js[:start] + new_func + js[end:]

with open('app.js', 'w') as f: f.write(js)

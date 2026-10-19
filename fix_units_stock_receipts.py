import re
with open('index.html', 'r') as f: html = f.read()

# ==========================================
# 1. Change Sand Qty to Bags
# ==========================================
html = html.replace('sandQty: "Sand Qty (Trips)"', 'sandQty: "Sand Qty (Bags)"')
html = html.replace('sandQty: "Yawan Yashi (Tirap)"', 'sandQty: "Yawan Yashi (Buhu)"')
# Also fix any UI labels
html = html.replace('Sand Qty (Trips)', 'Sand Qty (Bags)')
html = html.replace('trips left', 'bags left')

# ==========================================
# 2. Fix Dashboard Stock Value Calculation
# ==========================================
old_stock_val = "const unsoldValue = batches.filter(b => b.status === 'ready').reduce((sum, b) => sum + ((b.blocksProduced - b.breakages) * b.costPerBlock), 0);"
new_stock_val = '''let unsoldValue = 0;
        ['4', '6', '9'].forEach(sz => {
            const readyBatches = batches.filter(b => b.size === sz && b.status === 'ready');
            const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
            const sold = sales.filter(s => s.size === sz).reduce((s,v)=>s+v.quantity,0);
            const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);
            const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);
            const remaining = Math.max(0, produced - sold - broken + returned);
            unsoldValue += remaining * getAvgCost(sz);
        });'''
html = html.replace(old_stock_val, new_stock_val)

# ==========================================
# 3. Add Cement & Sand to WhatsApp Receipt
# ==========================================
old_wa = '''`Item: ${sale.quantity} pcs of ${sale.size}" Blocks\\n` +
            `Price/Block: ₦${sale.pricePerBlock.toLocaleString()}\\n` +'''
new_wa = '''`Item: ${sale.quantity} pcs of ${sale.size}" Blocks\\n` +
            `Est. Mix: ${Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand\\n` +
            `Price/Block: ₦${sale.pricePerBlock.toLocaleString()}\\n` +'''
html = html.replace(old_wa, new_wa)

# ==========================================
# 4. Add Cement & Sand to HTML Receipts (Save & Details)
# ==========================================
old_html_item = '''<div class="kv"><span>Item</span><strong>${sale.quantity} pcs of ${sale.size}" Blocks</strong></div>'''
new_html_item = '''<div class="kv"><span>Item</span><strong>${sale.quantity} pcs of ${sale.size}" Blocks</strong></div>
                <div class="kv"><span>Est. Materials Used</span><strong>${Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand</strong></div>'''
html = html.replace(old_html_item, new_html_item)

old_html_item_details = '''<div class="kv"><span>Item</span><strong>${s.quantity} pcs of ${s.size}" Blocks</strong></div>'''
new_html_item_details = '''<div class="kv"><span>Item</span><strong>${s.quantity} pcs of ${s.size}" Blocks</strong></div>
            <div class="kv"><span>Est. Materials Used</span><strong>${Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand</strong></div>'''
html = html.replace(old_html_item_details, new_html_item_details)

# ==========================================
# 5. Add Cement & Sand to Canvas Image Receipt
# ==========================================
# We need to shift everything down by 40 pixels to make room
old_canvas = '''            ctx.fillText(`${s.quantity} pcs of ${s.size}" Blocks`, 40, 380);
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
            ctx.fillText('Thank you for your business!', width / 2, 700);'''

new_canvas = '''            ctx.fillText(`${s.quantity} pcs of ${s.size}" Blocks`, 40, 380);
            ctx.fillText(`(@ ₦${s.pricePerBlock.toLocaleString()})`, 40, 405);

            ctx.textAlign = 'right';
            ctx.fillText(`₦${(s.quantity * s.pricePerBlock).toLocaleString()}`, 560, 380);

            // Materials Used
            ctx.textAlign = 'left';
            ctx.fillStyle = '#64748b';
            ctx.font = '14px Arial';
            ctx.fillText(`Est. Mix: ${Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand`, 40, 440);

            // Delivery
            ctx.fillStyle = '#0f172a';
            ctx.font = '16px Arial';
            if (s.deliveryCharge > 0) {
                ctx.textAlign = 'left';
                ctx.fillText(`Delivery Charge`, 40, 480);
                ctx.textAlign = 'right';
                ctx.fillText(`₦${s.deliveryCharge.toLocaleString()}`, 560, 480);
            }

            // Line
            ctx.beginPath(); ctx.moveTo(40, 515); ctx.lineTo(560, 515); ctx.stroke();

            // Totals
            ctx.textAlign = 'left';
            ctx.font = 'bold 20px Arial';
            ctx.fillText('Total Amount:', 40, 555);
            ctx.textAlign = 'right';
            ctx.fillStyle = '#059669';
            ctx.fillText(`₦${s.totalAmount.toLocaleString()}`, 560, 555);

            ctx.fillStyle = '#64748b';
            ctx.font = '16px Arial';
            ctx.textAlign = 'left';
            ctx.fillText('Amount Paid:', 40, 595);
            ctx.textAlign = 'right';
            ctx.fillStyle = '#0f172a';
            ctx.fillText(`₦${s.amountPaidAtSale.toLocaleString()}`, 560, 595);

            ctx.fillStyle = '#64748b';
            ctx.textAlign = 'left';
            ctx.fillText('Outstanding Balance:', 40, 635);
            ctx.textAlign = 'right';
            ctx.fillStyle = s.balanceOwing > 0 ? '#dc2626' : '#059669';
            ctx.fillText(`₦${s.balanceOwing.toLocaleString()}`, 560, 635);

            // Footer
            ctx.fillStyle = '#64748b';
            ctx.font = 'italic 16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Thank you for your business!', width / 2, 720);'''

html = html.replace(old_canvas, new_canvas)

with open('index.html', 'w') as f: f.write(html)

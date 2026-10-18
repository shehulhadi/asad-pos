import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add a single helper function to generate the WhatsApp text
helper_func = '''
    function buildWhatsAppReceipt(sale) {
        return encodeURIComponent(
            `*🧱 ${settings.businessName.toUpperCase()}*\\n` +
            `📞 ${settings.businessPhone || 'N/A'}\\n` +
            `--------------------------------\\n` +
            `*INVOICE / RECEIPT*\\n` +
            `Date: ${sale.date}\\n` +
            `Customer: ${sale.customerName}\\n` +
            `--------------------------------\\n` +
            `Item: ${sale.quantity} pcs of ${sale.size}" Blocks\\n` +
            `Price/Block: ₦${sale.pricePerBlock.toLocaleString()}\\n` +
            `Delivery: ₦${sale.deliveryCharge.toLocaleString()}\\n` +
            `*Total Amount: ₦${sale.totalAmount.toLocaleString()}*\\n` +
            `Amount Paid: ₦${sale.amountPaidAtSale.toLocaleString()}\\n` +
            `*Outstanding Balance: ₦${sale.balanceOwing.toLocaleString()}*\\n` +
            `--------------------------------\\n` +
            `Thank you for your patronage! 🙏`
        );
    }
'''
html = html.replace('    function saveSale() {', helper_func + '\n    function saveSale() {')

# 2. Update saveSale() to use the helper function
old_save_wa = re.search(r'        const waText = encodeURIComponent\(`\*🧱 \$\{settings\.businessName\.toUpperCase\(\)\}\*.*?`\);', html, re.DOTALL).group(0)
html = html.replace(old_save_wa, '        const waText = buildWhatsAppReceipt(sale);')

# 3. Update openSaleDetails() to use the helper function
old_details_wa = re.search(r'<a href="https://wa\.me/\$\{\(s\.customerPhone \|\| \'\'\)\.replace\(/\^0/, \'234\'\)\}\?text=\$\{encodeURIComponent\(`\*🧱.*?\)\}" target="_blank">', html, re.DOTALL).group(0)
new_details_wa = '''<a href="https://wa.me/${(s.customerPhone || '').replace(/^0/, '234')}?text=${buildWhatsAppReceipt(s)}" target="_blank">'''
html = html.replace(old_details_wa, new_details_wa)

with open('index.html', 'w') as f: f.write(html)

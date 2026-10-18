import re
with open('index.html', 'r') as f: html = f.read()

# 1. Ensure the helper function exists
if 'function buildWhatsAppReceipt(sale)' not in html:
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

# 2. Find the block for openSaleDetails and replace the <a> tag
start_idx = html.find('function openSaleDetails(')
end_idx = html.find('function editSale(')

if start_idx != -1 and end_idx != -1:
    details_block = html[start_idx:end_idx]
    # Replace the whole anchor tag
    details_block = re.sub(
        r'<a href="https://wa\.me/.*?target="_blank">', 
        '<a href="https://wa.me/${(s.customerPhone || \'\').replace(/^0/, \'234\')}?text=${buildWhatsAppReceipt(s)}" target="_blank">', 
        details_block, 
        flags=re.DOTALL
    )
    html = html[:start_idx] + details_block + html[end_idx:]

with open('index.html', 'w') as f: f.write(html)

import re
with open('index.html', 'r') as f: html = f.read()

# 1. Update the receipt in saveSale()
def fix_save_receipt(m):
    return "const waText = encodeURIComponent(`*🧱 ${settings.businessName.toUpperCase()}*\\n📞 ${settings.businessPhone || 'N/A'}\\n--------------------------------\\n*INVOICE / RECEIPT*\\nDate: ${sale.date}\\nCustomer: ${sale.customerName}\\n--------------------------------\\n${sale.quantity} pcs of ${sale.size}\\\" Blocks @ ₦${sale.pricePerBlock.toLocaleString()}\\nDelivery: ₦${sale.deliveryCharge.toLocaleString()}\\n*Total Amount: ₦${sale.totalAmount.toLocaleString()}*\\nAmount Paid: ₦${sale.amountPaidAtSale.toLocaleString()}\\n*Outstanding Balance: ₦${sale.balanceOwing.toLocaleString()}*\\n--------------------------------\\nThank you for your patronage! 🙏`);"

html = re.sub(r"const waText = encodeURIComponent\(`\*Receipt.*?`\);", fix_save_receipt, html, flags=re.DOTALL)

# 2. Update the receipt in openSaleDetails() (for past sales)
def fix_details_receipt(m):
    return "`*🧱 ${settings.businessName.toUpperCase()}*\\\\n📞 ${settings.businessPhone || 'N/A'}\\\\n--------------------------------\\\\n*INVOICE / RECEIPT*\\\\nDate: ${s.date}\\\\nCustomer: ${s.customerName}\\\\n--------------------------------\\\\n${s.quantity} pcs of ${s.size}\\\" Blocks @ ₦${s.pricePerBlock.toLocaleString()}\\\\nDelivery: ₦${s.deliveryCharge.toLocaleString()}\\\\n*Total Amount: ₦${s.totalAmount.toLocaleString()}*\\\\nAmount Paid: ₦${s.amountPaidAtSale.toLocaleString()}\\\\n*Outstanding Balance: ₦${s.balanceOwing.toLocaleString()}*\\\\n--------------------------------\\\\nThank you for your patronage! 🙏`"

html = re.sub(r"`\*Receipt - \$\{settings\.businessName\}\*\\\\n.*?Thank you.*?`", fix_details_receipt, html, flags=re.DOTALL)

with open('index.html', 'w') as f: f.write(html)

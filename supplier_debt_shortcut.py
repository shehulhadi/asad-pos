with open('index.html', 'r') as f: html = f.read()

# Inject the shortcut button inside the Supplier Debts tab rendering
old_render = '''        } else {
            if (owingPurchases.length === 0) { 
                html += `<div class="empty">${t.noSupplierDebts}</div>`; 
            } else {'''

new_render = '''        } else {
            html += `<button class="btn btn-dark" style="margin-bottom: 16px;" onclick="openPurchase()">+ ${t.logPurchase}</button>`;
            if (owingPurchases.length === 0) { 
                html += `<div class="empty">${t.noSupplierDebts}</div>`; 
            } else {'''

html = html.replace(old_render, new_render)

with open('index.html', 'w') as f: f.write(html)

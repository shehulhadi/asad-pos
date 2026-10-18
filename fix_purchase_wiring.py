import re
with open('index.html', 'r') as f: html = f.read()

# Replace the savePurchase function
old_save = '''    function savePurchase() {
        const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
        const cost = parseFloat(document.getElementById('pur-cost').value) || 0;
        const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
        if (qty <= 0) return showToast('Enter valid quantity', 'err');
        
        purchases.push({ id: Date.now().toString(), date: new Date().toISOString().split('T')[0], supplierName: document.getElementById('pur-supplier').value || 'Unknown', material: document.getElementById('pur-mat').value, qty: qty, cost: cost, amountPaid: paid });
        saveData('purchases', purchases);
        closeModal();
        nav('inventory');
        showToast('Purchase logged successfully', 'success');
    }'''

new_save = '''    function savePurchase() {
        const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
        const cost = parseFloat(document.getElementById('pur-cost').value) || 0;
        const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
        if (qty <= 0) return showToast('Enter valid quantity', 'err');
        
        purchases.push({ 
            id: Date.now().toString(), 
            date: new Date().toISOString().split('T')[0], 
            supplierName: document.getElementById('pur-supplier').value || 'Unknown', 
            material: document.getElementById('pur-mat').value, 
            qty: qty, 
            cost: cost, 
            amountPaid: paid 
        });
        saveData('purchases', purchases);
        closeModal();
        
        // Smart Navigation: Stay on Debts if that's where we are, otherwise go to Inventory
        if (currentView === 'debts') {
            currentDebtTab = 'supplier';
            nav('debts');
        } else {
            nav('inventory');
        }
        
        showToast('Purchase logged successfully', 'success');
    }'''
html = html.replace(old_save, new_save)

with open('index.html', 'w') as f: f.write(html)

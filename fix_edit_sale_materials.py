import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add the inputs to the editSale modal HTML
old_edit_form = '''            <div class="form-group"><label>Paid</label><input type="number" id="edit-s-paid" value="${s.amountPaidAtSale}" oninput="calcEditSale()"></div>
            <div class="calc-box">'''
new_edit_form = '''            <div class="form-group"><label>Paid</label><input type="number" id="edit-s-paid" value="${s.amountPaidAtSale}" oninput="calcEditSale()"></div>
            <div class="row">
                <div class="form-group"><label>Cement Used (Bags)</label><input type="number" id="edit-s-cement-used" value="${s.cementUsed || ''}" placeholder="Auto-calc"></div>
                <div class="form-group"><label>Sand Used (Bags)</label><input type="number" id="edit-s-sand-used" value="${s.sandUsed || ''}" placeholder="Auto-calc"></div>
            </div>
            <div class="calc-box">'''
html = html.replace(old_edit_form, new_edit_form)

# 2. Update saveEditedSale to read and save these inputs
old_save = '''        s.amountPaidAtSale = parseInt(document.getElementById('edit-s-paid').value) || 0;
        s.totalAmount = (s.quantity * s.pricePerBlock) + s.deliveryCharge;
        s.balanceOwing = s.totalAmount - s.amountPaidAtSale;'''
new_save = '''        s.amountPaidAtSale = parseInt(document.getElementById('edit-s-paid').value) || 0;
        
        const manCement = parseInt(document.getElementById('edit-s-cement-used').value) || 0;
        const manSand = parseInt(document.getElementById('edit-s-sand-used').value) || 0;
        s.cementUsed = manCement > 0 ? manCement : Math.ceil(s.quantity / (settings.mixCement || 50));
        s.sandUsed = manSand > 0 ? manSand : Math.ceil(s.quantity / (settings.mixSand || 500));

        s.totalAmount = (s.quantity * s.pricePerBlock) + s.deliveryCharge;
        s.balanceOwing = s.totalAmount - s.amountPaidAtSale;'''
html = html.replace(old_save, new_save)

with open('index.html', 'w') as f: f.write(html)

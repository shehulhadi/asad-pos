import re
with open('index.html', 'r') as f: html = f.read()

# ==========================================
# 1. Update New Sale Form
# ==========================================
old_form = '''                <div class="row">
                    <div class="form-group"><label>Cement Used (Bags)</label><input type="number" id="s-cement-used" placeholder="Auto-calc" style="background:#fff;"></div>
                    <div class="form-group"><label>Sand Used (Bags)</label><input type="number" id="s-sand-used" placeholder="Auto-calc" style="background:#fff;"></div>
                </div>'''
new_form = '''                <div class="row">
                    <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="s-cement-qty" placeholder="0" style="background:#fff;"></div>
                    <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="s-cement-price" placeholder="0" style="background:#fff;"></div>
                </div>
                <div class="row">
                    <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" placeholder="0" style="background:#fff;"></div>
                    <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" placeholder="0" style="background:#fff;"></div>
                </div>'''
html = html.replace(old_form, new_form)

# ==========================================
# 2. Update Edit Sale Form
# ==========================================
old_edit_form = '''            <div class="row">
                <div class="form-group"><label>Cement Used (Bags)</label><input type="number" id="edit-s-cement-used" value="${s.cementUsed || ''}" placeholder="Auto-calc"></div>
                <div class="form-group"><label>Sand Used (Bags)</label><input type="number" id="edit-s-sand-used" value="${s.sandUsed || ''}" placeholder="Auto-calc"></div>
            </div>'''
new_edit_form = '''            <div class="row">
                <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="edit-s-cement-qty" value="${s.cementQty || ''}" placeholder="0"></div>
                <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="edit-s-cement-price" value="${s.cementPrice || ''}" placeholder="0"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0"></div>
                <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0"></div>
            </div>'''
html = html.replace(old_edit_form, new_edit_form)

# ==========================================
# 3. Update executeSaveSale Logic
# ==========================================
old_save_vars = '''            const manualCement = parseInt(document.getElementById('s-cement-used').value) || 0;
            const manualSand = parseInt(document.getElementById('s-sand-used').value) || 0;'''
new_save_vars = '''            const manCementQty = parseInt(document.getElementById('s-cement-qty').value) || 0;
            const manCementPrice = parseFloat(document.getElementById('s-cement-price').value) || 0;
            const manSandQty = parseInt(document.getElementById('s-sand-qty').value) || 0;
            const manSandPrice = parseFloat(document.getElementById('s-sand-price').value) || 0;'''
html = html.replace(old_save_vars, new_save_vars)

old_sale_obj = '''                cementUsed: manualCement > 0 ? manualCement : Math.ceil(qty / (settings.mixCement || 50)),
                sandUsed: manualSand > 0 ? manualSand : Math.ceil(qty / (settings.mixSand || 500))'''
new_sale_obj = '''                cementQty: manCementQty,
                cementPrice: manCementPrice,
                sandQty: manSandQty,
                sandPrice: manSandPrice'''
html = html.replace(old_sale_obj, new_sale_obj)

# ==========================================
# 4. Update saveEditedSale Logic
# ==========================================
old_edit_save_vars = '''        const manCement = parseInt(document.getElementById('edit-s-cement-used').value) || 0;
        const manSand = parseInt(document.getElementById('edit-s-sand-used').value) || 0;
        s.cementUsed = manCement > 0 ? manCement : Math.ceil(s.quantity / (settings.mixCement || 50));
        s.sandUsed = manSand > 0 ? manSand : Math.ceil(s.quantity / (settings.mixSand || 500));'''
new_edit_save_vars = '''        s.cementQty = parseInt(document.getElementById('edit-s-cement-qty').value) || 0;
        s.cementPrice = parseFloat(document.getElementById('edit-s-cement-price').value) || 0;
        s.sandQty = parseInt(document.getElementById('edit-s-sand-qty').value) || 0;
        s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price').value) || 0;'''
html = html.replace(old_edit_save_vars, new_edit_save_vars)

# ==========================================
# 5. Update all Receipts to show Qty & Price
# ==========================================
# Helper string logic
mat_string = "${sale.cementQty > 0 ? sale.cementQty + ' bags cement (₦' + sale.cementPrice + ')' : Math.ceil(sale.quantity / (settings.mixCement || 50)) + ' bags cement (est)'}${sale.sandQty > 0 ? ', ' + sale.sandQty + ' bags sand (₦' + sale.sandPrice + ')' : ', ' + Math.ceil(sale.quantity / (settings.mixSand || 500)) + ' bags sand (est)'}"
mat_string_s = "${s.cementQty > 0 ? s.cementQty + ' bags cement (₦' + s.cementPrice + ')' : Math.ceil(s.quantity / (settings.mixCement || 50)) + ' bags cement (est)'}${s.sandQty > 0 ? ', ' + s.sandQty + ' bags sand (₦' + s.sandPrice + ')' : ', ' + Math.ceil(s.quantity / (settings.mixSand || 500)) + ' bags sand (est)'}"

# HTML Receipt (Save)
old_html_rcpt = '''<div class="kv"><span>Materials Used</span><strong>${sale.cementUsed || Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${sale.sandUsed || Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand</strong></div>'''
new_html_rcpt = f'''<div class="kv"><span>Materials</span><strong>{mat_string}</strong></div>'''
html = html.replace(old_html_rcpt, new_html_rcpt)

# HTML Receipt (Details)
old_html_details = '''<div class="kv"><span>Materials Used</span><strong>${s.cementUsed || Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${s.sandUsed || Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand</strong></div>'''
new_html_details = f'''<div class="kv"><span>Materials</span><strong>{mat_string_s}</strong></div>'''
html = html.replace(old_html_details, new_html_details)

# WhatsApp Receipt
old_wa = '''`Materials: ${sale.cementUsed || Math.ceil(sale.quantity / (settings.mixCement || 50))} bags cement, ${sale.sandUsed || Math.ceil(sale.quantity / (settings.mixSand || 500))} bags sand\\n` +'''
new_wa = f'''`Materials: {mat_string}\\n` +'''
html = html.replace(old_wa, new_wa)

# Canvas Receipt
old_canvas = '''            ctx.fillText(`Materials: ${s.cementUsed || Math.ceil(s.quantity / (settings.mixCement || 50))} bags cement, ${s.sandUsed || Math.ceil(s.quantity / (settings.mixSand || 500))} bags sand`, 40, 440);'''
new_canvas = f'''            ctx.fillText(`Materials: {mat_string_s}`, 40, 440);'''
html = html.replace(old_canvas, new_canvas)

with open('index.html', 'w') as f: f.write(html)

import re
with open('app.js', 'r') as f: js = f.read()

# 1. Update openAddDeviceModal
old_add_imei = '''        <div class="form-group"><label>IMEI / Serial Number</label><input type="text" id="p-imei" placeholder="Enter IMEI"></div>'''
new_add_imei = '''        <div class="row">
            <div class="form-group"><label>IMEI 1 / Serial</label><input type="text" id="p-imei" placeholder="Enter IMEI 1"></div>
            <div class="form-group"><label>IMEI 2</label><input type="text" id="p-imei2" placeholder="Enter IMEI 2 (Optional)"></div>
        </div>'''
js = js.replace(old_add_imei, new_add_imei)

# 2. Update savePhone to capture IMEI 2
old_save_imei = '''        imei: document.getElementById('p-imei').value || '','''
new_save_imei = '''        imei: document.getElementById('p-imei').value || '',
        imei2: document.getElementById('p-imei2').value || '','''
js = js.replace(old_save_imei, new_save_imei)

# 3. Update openDeviceDetails to display IMEI 2
old_details_imei = '''        <div class="kv"><span>IMEI / Serial</span><strong>${p.imei || 'N/A'}</strong></div>'''
new_details_imei = '''        <div class="kv"><span>IMEI 1</span><strong>${p.imei || 'N/A'}</strong></div>
        ${p.imei2 ? `<div class="kv"><span>IMEI 2</span><strong>${p.imei2}</strong></div>` : ''}'''
js = js.replace(old_details_imei, new_details_imei)

# 4. Update editDevice to include IMEI 2
old_edit_imei = '''        <div class="form-group"><label>IMEI</label><input type="text" id="edit-p-imei" value="${p.imei || ''}"></div>'''
new_edit_imei = '''        <div class="row">
            <div class="form-group"><label>IMEI 1</label><input type="text" id="edit-p-imei" value="${p.imei || ''}"></div>
            <div class="form-group"><label>IMEI 2</label><input type="text" id="edit-p-imei2" value="${p.imei2 || ''}"></div>
        </div>'''
js = js.replace(old_edit_imei, new_edit_imei)

# 5. Update saveEditedDevice to save IMEI 2
old_save_edit_imei = '''    p.imei = document.getElementById('edit-p-imei').value;'''
new_save_edit_imei = '''    p.imei = document.getElementById('edit-p-imei').value;
    p.imei2 = document.getElementById('edit-p-imei2').value;'''
js = js.replace(old_save_edit_imei, new_save_edit_imei)

# 6. Show IMEI 1 in the inventory list
old_list_imei = '''<div class="list-sub">${p.storage} · ${p.condition} · IMEI: ${p.imei || 'N/A'}</div>'''
new_list_imei = '''<div class="list-sub">${p.storage} · ${p.condition} · IMEI 1: ${p.imei || 'N/A'}</div>'''
js = js.replace(old_list_imei, new_list_imei)

with open('app.js', 'w') as f: f.write(js)
print("IMEI 2 added successfully.")

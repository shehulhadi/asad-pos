import re
with open('app.js', 'r') as f: js = f.read()

# 1. Update openAddDeviceModal (Change Storage to RAM/ROM)
old_add = '''        <div class="row">
            <div class="form-group"><label>Storage</label><input type="text" id="p-storage" placeholder="128GB"></div>
            <div class="form-group"><label>Condition</label><select id="p-condition">
                <option value="New">New</option>
                <option value="Used - Grade A">Used - Grade A</option>
                <option value="Used - Grade B">Used - Grade B</option>
                <option value="Needs Repair">Needs Repair</option>
            </select></div>
        </div>'''
new_add = '''        <div class="row">
            <div class="form-group"><label>RAM</label><input type="text" id="p-ram" placeholder="4GB"></div>
            <div class="form-group"><label>ROM (Storage)</label><input type="text" id="p-rom" placeholder="128GB"></div>
        </div>
        <div class="form-group">
            <label>Condition</label>
            <select id="p-condition">
                <option value="New">New</option>
                <option value="Used - Grade A">Used - Grade A</option>
                <option value="Used - Grade B">Used - Grade B</option>
                <option value="Needs Repair">Needs Repair</option>
            </select>
        </div>'''
js = js.replace(old_add, new_add)

# 2. Update savePhone (Save RAM/ROM + Add WhatsApp Status Modal)
old_save = '''    const phone = {
        id: Date.now().toString(),
        date: new Date().toISOString().split('T')[0],
        brand: brand,
        model: model,
        storage: document.getElementById('p-storage').value || 'N/A',
        condition: document.getElementById('p-condition').value,
        imei: document.getElementById('p-imei').value || '',
        imei2: document.getElementById('p-imei2').value || '',
        sellerName: document.getElementById('p-seller-name').value || '',
        sellerPhone: document.getElementById('p-seller-phone').value || '',
        sellerAddress: document.getElementById('p-seller-address').value || '',
        costPrice: cost,
        sellingPrice: sell,
        status: 'Available'
    };

    inventory.push(phone);
    saveData('inventory', inventory);
    closeModal();
    nav('inventory');'''

new_save = '''    const ram = document.getElementById('p-ram').value || '';
    const rom = document.getElementById('p-rom').value || '';

    const phone = {
        id: Date.now().toString(),
        date: new Date().toISOString().split('T')[0],
        brand: brand,
        model: model,
        ram: ram,
        rom: rom,
        storage: rom, // backward compatibility
        condition: document.getElementById('p-condition').value,
        imei: document.getElementById('p-imei').value || '',
        imei2: document.getElementById('p-imei2').value || '',
        sellerName: document.getElementById('p-seller-name').value || '',
        sellerPhone: document.getElementById('p-seller-phone').value || '',
        sellerAddress: document.getElementById('p-seller-address').value || '',
        costPrice: cost,
        sellingPrice: sell,
        status: 'Available'
    };

    inventory.push(phone);
    saveData('inventory', inventory);
    closeModal();

    // Show WhatsApp Status Share Popup
    const waStatusText = `📱 *${brand} ${model}*\\n` +
        `🔹 RAM: ${ram || 'N/A'}\\n` +
        `🔹 ROM: ${rom || 'N/A'}\\n` +
        `🔹 Condition: ${phone.condition}\\n` +
        `💰 Price: ${formatNaira(sell)}\\n\\n` +
        `📍 Available at Elbabs Communications!`;
    
    const waLink = `https://wa.me/?text=${encodeURIComponent(waStatusText)}`;

    document.getElementById('modal-body').innerHTML = `
        <div style="text-align:center; margin-bottom:20px;">
            <div style="width:56px; height:56px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 14px;">
                <svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg>
            </div>
            <h3 style="margin-bottom:4px;">Device Added!</h3>
            <p style="font-size:13px; color:var(--muted);">${brand} ${model} is now in stock.</p>
        </div>
        <a href="${waLink}" target="_blank" style="text-decoration:none;">
            <button class="btn wa" style="width:100%; padding:14px; font-size:15px; margin-bottom:10px; border:none;">📲 Share to WhatsApp Status</button>
        </a>
        <button class="btn btn-outline" onclick="nav('inventory')">Done</button>
    `;
    document.getElementById('modal').classList.add('active');'''
js = js.replace(old_save, new_save)

# 3. Update editDevice
old_edit = '''        <div class="row">
            <div class="form-group"><label>Storage</label><input type="text" id="edit-p-storage" value="${p.storage}"></div>
            <div class="form-group"><label>Condition</label><select id="edit-p-condition">'''
new_edit = '''        <div class="row">
            <div class="form-group"><label>RAM</label><input type="text" id="edit-p-ram" value="${p.ram || ''}"></div>
            <div class="form-group"><label>ROM (Storage)</label><input type="text" id="edit-p-rom" value="${p.rom || p.storage || ''}"></div>
        </div>
        <div class="form-group"><label>Condition</label><select id="edit-p-condition">'''
js = js.replace(old_edit, new_edit)

# 4. Update saveEditedDevice
old_save_edit = '''    p.storage = document.getElementById('edit-p-storage').value;'''
new_save_edit = '''    p.ram = document.getElementById('edit-p-ram').value;
    p.rom = document.getElementById('edit-p-rom').value;
    p.storage = p.rom;'''
js = js.replace(old_save_edit, new_save_edit)

# 5. Update openDeviceDetails
old_details = '''        <div class="kv"><span>Storage</span><strong>${p.storage}</strong></div>'''
new_details = '''        <div class="kv"><span>RAM</span><strong>${p.ram || 'N/A'}</strong></div>
        <div class="kv"><span>ROM (Storage)</span><strong>${p.rom || p.storage || 'N/A'}</strong></div>'''
js = js.replace(old_details, new_details)

# 6. Update renderInventory list item
js = js.replace("${p.storage} · ${p.condition} · IMEI 1: ${p.imei || 'N/A'}", "${p.ram || ''} ${p.rom || p.storage || ''} · ${p.condition} · IMEI 1: ${p.imei || 'N/A'}")

# 7. Update openSaleModal option text
js = js.replace("${p.brand} ${p.model} (${p.storage}) - ${formatNaira(p.sellingPrice)}", "${p.brand} ${p.model} (${p.ram || ''}/${p.rom || p.storage || ''}) - ${formatNaira(p.sellingPrice)}")

# 8. Update saveSale phoneName
js = js.replace("phoneName: `${device.brand} ${device.model} (${device.storage})`,", "phoneName: `${device.brand} ${device.model} (${device.ram || ''}/${device.rom || device.storage || ''})`,")

with open('app.js', 'w') as f: f.write(js)
print("RAM/ROM split and WhatsApp Status share added.")

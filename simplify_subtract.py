import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace openAdjustStock to only subtract
start = js.find('function openAdjustStock() {')
end = js.find('function saveAdjustStock() {')
if start != -1 and end != -1:
    new_open = '''function openAdjustStock() {
    document.getElementById('modal-body').innerHTML = `
        <h3>Subtract Stock / Log Loss</h3>
        <p style="font-size:13px; color:var(--muted); margin-bottom:16px;">Use this to subtract stock due to spoilage, damage, or manual correction.</p>
        <div class="form-group">
            <label>Material</label>
            <select id="adj-mat">
                <option value="cement">Cement</option>
                <option value="sand">Sand</option>
                <option value="empty_bag">Empty Bags</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity to Subtract</label>
            <input type="number" id="adj-qty" value="" placeholder="0" min="1">
        </div>
        <div class="form-group">
            <label>Reason</label>
            <input type="text" id="adj-reason" placeholder="e.g. Spoiled, Damaged">
        </div>
        <button class="btn btn-danger" onclick="saveAdjustStock()">Subtract Stock</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start] + new_open + js[end:]

# 2. Replace saveAdjustStock to always subtract
start = js.find('function saveAdjustStock() {')
end = js.find('function openPurchaseDetails(id) {')
if start != -1 and end != -1:
    new_save = '''function saveAdjustStock() {
    const qty = parseFloat(document.getElementById('adj-qty')?.value) || 0;
    if (qty <= 0) return showToast('Enter a valid quantity', 'err');

    stockAdjustments.push({ 
        id: Date.now().toString(), 
        date: getTodayStr(), 
        material: document.getElementById('adj-mat')?.value || 'cement', 
        qty: -Math.abs(qty), // Force negative
        reason: document.getElementById('adj-reason')?.value || 'Manual adjustment' 
    });
    
    saveData('stockAdjustments', stockAdjustments); 
    closeModal(); 
    nav('dashboard'); 
    showToast('Stock subtracted', 'success');
}

'''
    js = js[:start] + new_save + js[end:]

with open('app.js', 'w') as f: f.write(js)

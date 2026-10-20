import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace openAdjustStock
start = js.find('function openAdjustStock() {')
end = js.find('function saveAdjustStock() {')
if start != -1 and end != -1:
    new_open = '''let currentAdjType = 'add';

function setAdjType(type) {
    currentAdjType = type;
    document.getElementById('adj-btn-add').classList.toggle('on', type === 'add');
    document.getElementById('adj-btn-sub').classList.toggle('on', type === 'subtract');
}

function openAdjustStock() {
    currentAdjType = 'add';
    document.getElementById('modal-body').innerHTML = `
        <h3>Adjust Stock</h3>
        <div class="segmented" style="margin-bottom:16px;">
            <button id="adj-btn-add" class="on" onclick="setAdjType('add')">+ Add Stock</button>
            <button id="adj-btn-sub" onclick="setAdjType('subtract')">- Subtract Stock</button>
        </div>
        <div class="form-group">
            <label>Material</label>
            <select id="adj-mat">
                <option value="cement">Cement</option>
                <option value="sand">Sand</option>
                <option value="empty_bag">Empty Bags</option>
            </select>
        </div>
        <div class="form-group">
            <label>Quantity</label>
            <input type="number" id="adj-qty" value="" placeholder="0" min="0">
        </div>
        <div class="form-group">
            <label>Reason</label>
            <input type="text" id="adj-reason" placeholder="e.g. Spoiled, Extra found">
        </div>
        <button class="btn" onclick="saveAdjustStock()">Save Adjustment</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start] + new_open + js[end:]

# 2. Replace saveAdjustStock
start = js.find('function saveAdjustStock() {')
end = js.find('function openPurchaseDetails(id) {')
if start != -1 and end != -1:
    new_save = '''function saveAdjustStock() {
    let qty = parseFloat(document.getElementById('adj-qty')?.value) || 0;
    if (qty === 0) return showToast('Enter a valid quantity', 'err');
    
    // Apply the toggle
    if (currentAdjType === 'subtract') qty = -qty;

    stockAdjustments.push({ 
        id: Date.now().toString(), 
        date: getTodayStr(), 
        material: document.getElementById('adj-mat')?.value || 'cement', 
        qty: qty, 
        reason: document.getElementById('adj-reason')?.value || 'Manual adjustment' 
    });
    
    saveData('stockAdjustments', stockAdjustments); 
    closeModal(); 
    nav('dashboard'); 
    showToast(currentAdjType === 'add' ? 'Stock added' : 'Stock subtracted', 'success');
}

'''
    js = js[:start] + new_save + js[end:]

with open('app.js', 'w') as f: f.write(js)

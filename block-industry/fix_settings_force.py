import re
with open('app.js', 'r') as f: js = f.read()

# 1. Replace the entire openSettings function
start_open = js.find('function openSettings() {')
end_open = js.find('function addExpenseCategory() {')

if start_open != -1 and end_open != -1:
    new_open = '''function openSettings() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.settings}</h3>
        <div class="form-group">
            <label>${t.language} / Harshe</label>
            <select id="set-lang">
                <option value="en" ${settings.lang === 'en' ? 'selected' : ''}>English</option>
                <option value="ha" ${settings.lang === 'ha' ? 'selected' : ''}>Hausa</option>
            </select>
        </div>
        <div class="form-group" style="display:flex; justify-content:space-between; align-items:center; background:var(--bg); padding:12px; border-radius:8px;">
            <label style="margin:0; font-size:14px; font-weight:700;">Dark Mode</label>
            <input type="checkbox" id="set-dark-mode" style="width:20px; height:20px;" ${settings.darkMode ? 'checked' : ''}>
        </div>
        
        <div class="eyebrow">Default Selling Prices (₦)</div>
        <div class="row">
            <div class="form-group"><label>6" Block</label><input type="number" id="set-price-6" value="${settings.defaultPrices['6'] || ''}" placeholder="0"></div>
            <div class="form-group"><label>Cement (Bag)</label><input type="number" id="set-price-cement" value="${settings.defaultCementPrice || ''}" placeholder="0"></div>
            <div class="form-group"><label>Empty Bag (pc)</label><input type="number" id="set-price-emptybag" value="${settings.defaultEmptyBagPrice || ''}" placeholder="0"></div>
        </div>

        <div class="eyebrow">Standard Mix Ratios</div>
        <div class="row">
            <div class="form-group"><label>Blocks per Cement Bag</label><input type="number" id="set-mix-cement" value="${settings.mixCement || 50}"></div>
            <div class="form-group"><label>Blocks per Sand Bag</label><input type="number" id="set-mix-sand" value="${settings.mixSand || 500}"></div>
        </div>
        
        <div class="form-group" style="margin-top:16px;">
            <label>Sales Reminder</label>
            <select id="set-reminder">
                <option value="0" ${settings.reminderInterval == 0 ? 'selected' : ''}>Off</option>
                <option value="1" ${settings.reminderInterval == 1 ? 'selected' : ''}>Every 1 Hour</option>
                <option value="2" ${settings.reminderInterval == 2 ? 'selected' : ''}>Every 2 Hours</option>
                <option value="4" ${settings.reminderInterval == 4 ? 'selected' : ''}>Every 4 Hours</option>
            </select>
        </div>
        
        <div class="row">
            <div class="form-group"><label>${t.marginAlert}</label><input type="number" id="set-margin" value="${settings.marginAlertPct || ''}" placeholder="0"></div>
            <div class="form-group"><label>${t.fixedCosts}</label><input type="number" id="set-fixed" value="${settings.fixedCostsMonthly || ''}" placeholder="0"></div>
        </div>
        
        <div class="eyebrow">Low Stock Thresholds</div>
        <div class="row">
            <div class="form-group"><label>${t.cement}</label><input type="number" id="set-low-cement" value="${settings.lowCement || ''}" placeholder="0"></div>
            <div class="form-group"><label>${t.sand}</label><input type="number" id="set-low-sand" value="${settings.lowSand || ''}" placeholder="0"></div>
        </div>
        
        <div class="eyebrow">Custom Expense Categories</div>
        <div class="row">
            <div class="form-group" style="flex:2;"><input type="text" id="set-new-expense" placeholder="e.g. Truck Hire"></div>
            <div class="form-group" style="flex:1;"><button class="btn btn-outline" style="margin-top:0;" onclick="addExpenseCategory()">Add</button></div>
        </div>
        
        <div class="form-group" style="display:flex; justify-content:space-between; align-items:center;">
            <label style="margin:0; font-size:14px; font-weight:700;">Security PINs</label>
        </div>
        <div class="row">
            <div class="form-group"><label>Owner PIN</label><input type="password" id="set-owner-pin" maxlength="4" value="${settings.ownerPin}"></div>
            <div class="form-group"><label>Staff PIN</label><input type="password" id="set-staff-pin" maxlength="4" value="${settings.staffPin}"></div>
        </div>
        
        <button class="btn" onclick="saveSettings()">${t.saveSettings}</button>
        <button class="btn btn-outline" style="margin-top:10px;" onclick="openDirectory()">📂 Directory</button>
        <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>
        <button class="btn btn-danger" style="margin-top:22px;" onclick="clearAllData()">${t.clearData}</button>
    `;
    document.getElementById('modal').classList.add('active');
}

'''
    js = js[:start_open] + new_open + js[end_open:]

# 2. Replace saveSettings
start_save = js.find('function saveSettings() {')
end_save = js.find('function clearAllData() {')

if start_save != -1 and end_save != -1:
    new_save = '''function saveSettings() {
    const newLang = document.getElementById('set-lang').value;
    const langChanged = newLang !== settings.lang;
    settings.lang = newLang;
    
    settings.darkMode = document.getElementById('set-dark-mode').checked;
    if(settings.darkMode) document.body.classList.add('dark');
    else document.body.classList.remove('dark');
    
    settings.reminderInterval = parseInt(document.getElementById('set-reminder').value) || 0;
    if (settings.reminderInterval > 0 && Notification.permission !== 'granted') {
        Notification.requestPermission().then(perm => { if (perm === 'granted') setupReminders(); });
    } else { setupReminders(); }

    settings.mixCement = parseInt(document.getElementById('set-mix-cement').value) || 50;
    settings.mixSand = parseInt(document.getElementById('set-mix-sand').value) || 500;
    
    settings.defaultPrices = { '6': parseFloat(document.getElementById('set-price-6').value) || 0 };
    settings.defaultCementPrice = parseFloat(document.getElementById('set-price-cement').value) || 0;
    settings.defaultEmptyBagPrice = parseFloat(document.getElementById('set-price-emptybag').value) || 0;
    
    settings.marginAlertPct = parseFloat(document.getElementById('set-margin').value) || 0;
    settings.fixedCostsMonthly = parseFloat(document.getElementById('set-fixed').value) || 0;
    settings.lowCement = parseFloat(document.getElementById('set-low-cement').value) || 0;
    settings.lowSand = parseFloat(document.getElementById('set-low-sand').value) || 0;
    settings.ownerPin = document.getElementById('set-owner-pin').value || settings.ownerPin;
    settings.staffPin = document.getElementById('set-staff-pin').value || settings.staffPin;
    
    saveData('settings', settings);
    closeModal();
    if (langChanged) { buildNav(); }
    nav(currentView);
    showToast('Settings saved', 'success');
}

'''
    js = js[:start_save] + new_save + js[end_save:]

# 3. Ensure Analytics uses them correctly
old_stock_calc = '''    const blockValPrice = N(settings.defaultPrices['6']) || getAvgCost('6');
    unsoldValue += remainingBlocks * blockValPrice;
    
    // Raw Materials Value (Use Default Selling Price if set, else fallback to avg cost)
    const cementValPrice = N(settings.defaultCementPrice) || cementData.cost;
    const ebValPrice = N(settings.defaultEmptyBagPrice) || ebData.cost;

    unsoldValue += cementData.stock * cementValPrice;
    // Sand omitted as requested
    unsoldValue += ebData.stock * ebValPrice;'''
    
# Check if the previous failed script left the old version
if old_stock_calc not in js:
    fallback_old = '''    unsoldValue += remainingBlocks * getAvgCost('6');
    unsoldValue += cementData.stock * cementData.cost;
    unsoldValue += sandData.stock * sandData.cost;
    unsoldValue += ebData.stock * ebData.cost;'''
    js = js.replace(fallback_old, old_stock_calc)

with open('app.js', 'w') as f: f.write(js)
print("Settings forcefully fixed.")

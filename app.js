const ICONS = {
    dashboard: '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>', home: '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
    sales: '<path d="M8 5v14M16 5v14M8 5l8 14M5 9h14M5 14h14"/>',
    production: '<path d="M12 3l9 5v8l-9 5-9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/>', expenses: '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 15h2"/>',
    debts: '<path d="M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3z"/><path d="M5 17a3 3 0 013-3h11"/>', settings: '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    refresh: '<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/>', update: '<path d="M12 3v12m0 0l-4-4m4 4l4-4M4 20h16"/>', logout: '<path d="M9 4H5v16h4M16 8l4 4-4 4M20 12H9"/>',
    report: '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 13h6M9 17h6"/>', alert: '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
    users: '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5a3 3 0 010 6M21 20c0-2.5-1.5-4.6-3.5-5.5"/>',
    target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>', trend: '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
    bars: '<path d="M5 21V10M12 21V4M19 21v-8"/>', plus: '<path d="M12 5v14M5 12h14"/>', back: '<path d="M15 5l-7 7 7 7"/>',
    trophy: '<path d="M8 4h8v5a4 4 0 01-8 0z"/><path d="M8 6H5a3 3 0 003 4M16 6h3a3 3 0 01-3 4M12 13v4M8 20h8"/>',
    cash: '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>', arrowIn: '<path d="M12 4v12m0 0l-4-4m4 4l4-4M5 20h14"/>',
    arrowOut: '<path d="M12 20V8m0 0l-4 4m4-4l4 4M5 4h14"/>', box: '<path d="M3 8l9-5 9 5v8l-9 5-9-5z"/><path d="M3 8l9 5 9-5"/>', check: '<path d="M5 13l4 4L19 7"/>'
};
function ico(name, cls) { return `<svg class="ic ${cls||''}" viewBox="0 0 24 24">${ICONS[name]||''}</svg>`; }

const i18n = {
    en: { 
        home: "Home", dashboard: "Stock", analytics: "Analytics", sales: "Sales", debts: "Debts", expenses: "Expenses", production: "Production",
        newSale: "New Sale", customer: "Customer Name", date: "Date", phone: "Phone Number", size: "Block Size", qty: "Quantity", price: "Price per Block (₦)", 
        delivery: "Delivery Charge (₦)", paid: "Amount Paid (₦)", save: "Save Sale", receipt: "Receipt", remind: "Remind on WhatsApp", pay: "Record Payment", 
        amount: "Amount (₦)", balance: "Balance Owing", total: "Total Amount", labourCost: "Labour Cost (₦)",
        newExpense: "New Expense", category: "Category", note: "Note", saveExpense: "Save Expense",
        wages: "Wages", repairs: "Machine Repairs", generator_fuel: "Generator Fuel", rent: "Rent", transport: "Transport", loaders: "Loaders", phone_data: "Phone/Data", other: "Other",
        newBatch: "Log Production Batch", worker: "Worker Name", blocksProduced: "Blocks Produced",
        cementBags: "Cement Bags Used", costPerBag: "Cost per Bag (₦)", sandCost: "Sand Cost (₦)", sandQty: "Sand Qty (Bags)",
        otherCost: "Water/Other Cost (₦)", breakages: "Breakages (Qty)",
        curingLoss: "Curing Loss (Qty)", totalCost: "Total Batch Cost", costPerBlock: "Cost per Block",
        saveBatch: "Save Batch", markReady: "Mark as Ready", curing: "Curing", ready: "Ready",
        settings: "Settings", marginAlert: "Margin Alert (%)", fixedCosts: "Monthly Fixed Costs (₦)",
        saveSettings: "Save Settings", turnover: "Turnover", grossProfit: "Gross Profit", netProfit: "Net Profit",
        cashInHand: "Cash in Hand", moneyOwed: "Owed to You", stockValue: "Stock Value", moneyYouOwe: "You Owe",
        topCustomers: "Top Customers", bestSizes: "Best Selling Sizes", marginWarning: "MARGIN WARNING: Selling below cost!",
        inventory: "Inventory", reports: "Reports & Backup", rawMaterials: "Raw Materials", finishedBlocks: "Finished Blocks",
        cement: "Cement", sand: "Sand", empty_bag: "Empty Bags", logPurchase: "Log Purchase", supplierName: "Supplier Name",
        lowStock: "LOW STOCK", varianceWarning: "VARIANCE WARNING: Expected vs Counted mismatch!",
        expected: "Expected", physicalCount: "Physical Count", stockCheck: "Stock Check",
        plReport: "Profit & Loss Report", month: "Month", revenue: "Revenue", cogs: "Cost of Goods Sold",
        exportCSV: "Export CSV", exportJSON: "Share Backup", importJSON: "Restore JSON",
        clearData: "Clear All Data", confirmClear: "Enter Owner PIN to clear ALL data:", wrongPin: "Incorrect PIN",
        profitMargins: "Profit per Block", logBreakage: "Log Breakage", breakageReason: "Reason/Notes", 
        salesHistory: "Sales History", noSalesYet: "No sales recorded yet.", broken: "Broken",
        customerDebts: "Customer Debts", supplierDebts: "Supplier Debts", paySupplier: "Pay Supplier", noSupplierDebts: "No outstanding supplier debts.",
        daysAgo: "days ago", acceptCount: "Accept Count & Update System", language: "Language"
    },
    ha: { 
        home: "Gida", dashboard: "Kaya", analytics: "Analytics", sales: "Tallace", debts: "Bashi", expenses: "Kashe-kashe", production: "Samarwa",
        newSale: "Sabuwar Sayarwa", customer: "Sunan Abokin Ciniki", date: "Kwanan Wata", phone: "Lambar Waya", size: "Girman Bulo", qty: "Yawa", price: "Farashin Bulo (₦)", 
        delivery: "Kudin Jigila (₦)", paid: "Kudin da aka Biya (₦)", save: "Ajiye", receipt: "Rasit", remind: "Tuna a WhatsApp", pay: "Yi Biyan Bashi", 
        amount: "Kudi (₦)", balance: "Sauran Bashi", total: "Jimillar Kudi", labourCost: "Kudin Ma'aikata (₦)",
        newExpense: "Sabbin Kashe-kashe", category: "Rukuni", note: "Bayani", saveExpense: "Ajiye Kashewa",
        wages: "Albashi", repairs: "Gyaran Injin", generator_fuel: "Man Fetur", rent: "Kudin Gida", transport: "Jigila", loaders: "Loda", phone_data: "Waya/Data", other: "Sauran",
        newBatch: "Ajiye Yawan Bulo", worker: "Sunan Ma'aikaci", blocksProduced: "Yawan Bulo",
        cementBags: "Buhun Siminti", costPerBag: "Kudin Buhu (₦)", sandCost: "Kudin Yashi (₦)", sandQty: "Yawan Yashi (Buhu)",
        otherCost: "Kudin Ruwa/Sauran (₦)", breakages: "Karye",
        curingLoss: "Asarar Jiyya", totalCost: "Jimlar Kudin Batch", costPerBlock: "Kudin Bulo Daya",
        saveBatch: "Ajiye Bulo", markReady: "Sanya a Shirye", curing: "Jiyya", ready: "Shirye",
        settings: "Saituna", marginAlert: "Gargadin Riba (%)", fixedCosts: "Kudin Watan Nan (₦)",
        saveSettings: "Ajiye Saituna", turnover: "Kudin Shiga", grossProfit: "Ribar Farko", netProfit: "Ribar Karshe",
        cashInHand: "Kudi a Hannu", moneyOwed: "Bashin da ake bin ka", stockValue: "Darajar Kaya", moneyYouOwe: "Bashin da kake bi",
        topCustomers: "Manyan Abokan Ciniki", bestSizes: "Mafi Sayar da Bulo", marginWarning: "GARGAJIYA: Ana sayarwa kasa da kudin da aka kashe!",
        inventory: "Ajiya", reports: "Rahoto & Ajiya", rawMaterials: "Kayan Gini", finishedBlocks: "Bulon da aka gama",
        cement: "Siminti", sand: "Yashi", empty_bag: "Buhu Wofi", logPurchase: "Yi Rikodin Siyan Kaya", supplierName: "Sunan Mai Sayarwa",
        lowStock: "KARANCIN KAYA", varianceWarning: "GARGAJIYA: Bambanci tsakanin lissafi da kidaya!",
        expected: "Wanda ake tsammani", physicalCount: "Kidaya ta Hannu", stockCheck: "Duba Ajiya",
        plReport: "Rahoton Riba da Asara", month: "Wata", revenue: "Kudin Shiga", cogs: "Kudin Kayan Sayarwa",
        exportCSV: "Fitar da CSV", exportJSON: "Ajiye Backup", importJSON: "Dawo da JSON",
        clearData: "Goge Duk Bayanai", confirmClear: "Shigar da PIN na Mai Gida don goge DUK bayanai:", wrongPin: "PIN ba daidai ba",
        profitMargins: "Ribar Kowane Bulo", logBreakage: "Yi Rikodin Karye", breakageReason: "Dalili/Bayani",
        salesHistory: "Tarihin Sayarwa", noSalesYet: "Babu wata sayarwa da aka yi.", broken: "Ya karye",
        customerDebts: "Bashin Abokan Ciniki", supplierDebts: "Bashin Masu Sayarwa", paySupplier: "Biya Mai Sayarwa", noSupplierDebts: "Babu bashin mai sayarwa.",
        daysAgo: "kwanaki da suka wuce", acceptCount: "Yarda da Kidaya & Gyara Lissafi", language: "Harshe"
    }
};

let settings = JSON.parse(localStorage.getItem('asad:settings')) || {
    ownerPin: '1234', staffPin: '0000', lang: 'en', businessName: 'A. Jibrialla Construction Ltd.', businessPhone: '0906 634 4956',
    marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0, mixCement: 50, mixSand: 500, defaultPrices: {'4': 0, '6': 0, '9': 0}, creditLimits: {}
};
if(!settings.customExpenses) settings.customExpenses = [];
if(settings.streak === undefined) settings.streak = 0;
if(settings.lastOpenDate === undefined) settings.lastOpenDate = '';
if(settings.bestDayAmount === undefined) settings.bestDayAmount = 0;
if(settings.reminderInterval === undefined) settings.reminderInterval = 0;
if(settings.mixCement === undefined) settings.mixCement = 50;
if(settings.mixSand === undefined) settings.mixSand = 500;
if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};
if(!settings.creditLimits) settings.creditLimits = {};

let sales = JSON.parse(localStorage.getItem('asad:sales')) || [];
let payments = JSON.parse(localStorage.getItem('asad:customerPayments')) || [];
let expenses = JSON.parse(localStorage.getItem('asad:expenses')) || [];
let batches = JSON.parse(localStorage.getItem('asad:batches')) || [];
let purchases = JSON.parse(localStorage.getItem('asad:purchases')) || [];
let breakagesLog = JSON.parse(localStorage.getItem('asad:breakages')) || [];
let returns = JSON.parse(localStorage.getItem('asad:returns')) || [];
let stockCounts = JSON.parse(localStorage.getItem('asad:stockCounts')) || {}; 
let stockAdjustments = JSON.parse(localStorage.getItem('asad:stockAdjustments')) || [];

let currentUser = null; 
let currentView = 'dashboard';
let currentDebtTab = 'customer'; 
let currentRating = 0;

function getWATDate() {
    const now = new Date();
    return new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (1 * 3600000));
}
function getTodayStr() {
    return getWATDate().toISOString().split('T')[0];
}
function saveData(key, data) { localStorage.setItem('asad:' + key, JSON.stringify(data)); }
function formatNaira(num) { return '₦' + Number(num).toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 2}); }
function backBtn(to) { return `<button class="back-link" onclick="nav('${to}')">${ico('back')} ${i18n[settings.lang][to] || 'Back'}</button>`; }

function showToast(msg, type = 'default') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    let icon = type === 'success' ? ico('check') : (type === 'err' ? ico('alert') : ico('update'));
    toast.innerHTML = `${icon} <span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

function showDialog(title, msg, onConfirm, isPrompt = false) {
    const overlay = document.getElementById('dialog-overlay');
    if (!overlay) {
        if (isPrompt) { const val = prompt(title + "\n\n" + msg); if (val !== null && onConfirm) onConfirm(val); } 
        else { if (confirm(title + "\n\n" + msg)) { if (onConfirm) onConfirm(true); } }
        return;
    }
    document.getElementById('dialog-title').textContent = title;
    if (isPrompt) {
        document.getElementById('dialog-msg').innerHTML = `<input type="password" id="dialog-input" style="width:100%; padding:12px; border:1.5px solid var(--line); border-radius:8px; font-size:16px; text-align:center; margin-top:10px;" placeholder="••••">`;
        setTimeout(() => document.getElementById('dialog-input').focus(), 100);
    } else {
        document.getElementById('dialog-msg').innerHTML = msg;
    }
    const confirmBtn = document.getElementById('dialog-confirm-btn');
    const newBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);
    newBtn.onclick = () => {
        let val = isPrompt ? document.getElementById('dialog-input').value : true;
        closeDialog();
        if (onConfirm) onConfirm(val);
    };
    overlay.classList.add('active');
}
function closeDialog() { const overlay = document.getElementById('dialog-overlay'); if(overlay) overlay.classList.remove('active'); }
window.alert = (msg) => showToast(msg, 'default');

function checkStreak() {
    const today = getTodayStr();
    if (!settings.lastOpenDate) {
        settings.lastOpenDate = today;
        settings.streak = 1;
        saveData('settings', settings);
        return;
    }
    if (settings.lastOpenDate === today) return;
    const last = new Date(settings.lastOpenDate);
    const now = new Date(today);
    const diffDays = Math.round((now - last) / (1000 * 60 * 60 * 24));
    if (diffDays === 1) {
        settings.streak += 1;
        setTimeout(() => showToast(`🔥 ${settings.streak} Day Streak! Keep it up!`, 'success'), 1500);
    } else if (diffDays > 1) {
        settings.streak = 1; 
    }
    settings.lastOpenDate = today;
    saveData('settings', settings);
}

let reminderTimer = null;
function setupReminders() {
    if (reminderTimer) clearInterval(reminderTimer);
    if (settings.reminderInterval && settings.reminderInterval > 0) {
        if (Notification.permission === 'granted') {
            reminderTimer = setInterval(() => {
                const now = new Date();
                if (now.getHours() >= 22 || now.getHours() < 6) return;
                if (document.visibilityState === 'hidden') {
                    new Notification("🧱 Sales Reminder", { body: "Don't forget to log your recent block sales!" });
                } else {
                    showToast("⏰ Reminder: Don't forget to log your sales!", "success");
                }
            }, settings.reminderInterval * 60 * 60 * 1000);
        }
    }
}

function triggerConfetti() {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed'; canvas.style.top = '0'; canvas.style.left = '0';
    canvas.style.width = '100vw'; canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none'; canvas.style.zIndex = '99999';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    let particles = [];
    for(let i = 0; i < 120; i++) {
        particles.push({ x: canvas.width / 2, y: canvas.height / 2, vx: (Math.random() - 0.5) * 20, vy: (Math.random() - 0.5) * 20 - 5, color: `hsl(${Math.random() * 360}, 100%, 60%)`, size: Math.random() * 8 + 4, life: 100 });
    }
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.vy += 0.4; p.life -= 1; ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, p.size, p.size); });
        particles = particles.filter(p => p.life > 0);
        if(particles.length > 0) requestAnimationFrame(draw); else canvas.remove();
    }
    draw();
    if (navigator.vibrate) navigator.vibrate([100, 50, 100, 50, 200]);
}

async function forceUpdate() {
    showDialog("Update App?", "This will download the latest version.\nYOUR STOCK, SALES, AND DEBTS WILL NOT BE DELETED.", async () => {
        showToast('Clearing cache and updating...', 'success');
        try {
            if ('serviceWorker' in navigator) {
                const registrations = await navigator.serviceWorker.getRegistrations();
                for (let registration of registrations) { await registration.unregister(); }
            }
            const keys = await caches.keys();
            for (let key of keys) { await caches.delete(key); }
        } catch(e) { console.log('Cache clear error', e); }
        setTimeout(() => { window.location.href = window.location.href.split('?')[0] + '?v=' + Date.now(); }, 1000);
    });
}

function openRating() {
    const bizName = settings.businessName || 'My Business';
    document.getElementById('rating-app-title').textContent = bizName;
    document.getElementById('rating-app-footer').textContent = bizName + ' (v1.0.0)';
    document.getElementById('rating-modal').classList.add('active');
}
function setStars(stars) {
    currentRating = stars;
    const starsEl = document.getElementById('rating-stars-main');
    let display = '';
    for (let i = 1; i <= 5; i++) {
        display += `<span onclick="setStars(${i})" style="color:${i <= stars ? 'var(--accent)' : 'var(--muted)'}">${i <= stars ? '★' : '☆'}</span>`;
    }
    starsEl.innerHTML = display;
}
function sendFeedback() {
    if (currentRating === 0) return showToast('Please select a star rating first', 'err');
    const text = document.getElementById('feedback-text').value;
    const devPhone = "2347082762606"; 
    const msg = encodeURIComponent(`Hello Asad Tech Concepts!\n\nApp Rating: ${currentRating} out of 5 stars ⭐\n\nFeedback: ${text || 'No extra text.'}\n\nBusiness: ${settings.businessName || 'N/A'}`);
    closeRating();
    showToast('Thank you for your feedback!', 'success');
    setTimeout(() => { window.open(`https://wa.me/${devPhone}?text=${msg}`, '_blank'); }, 500);
}
function closeRating() { document.getElementById('rating-modal').classList.remove('active'); }

function login() {
    const pin = document.getElementById('pin-input').value;
    const err = document.getElementById('login-error');
    if (pin === settings.ownerPin) { currentUser = 'owner'; err.style.display = 'none'; }
    else if (pin === settings.staffPin) { currentUser = 'staff'; err.style.display = 'none'; }
    else { err.style.display = 'block'; return; }
    sessionStorage.setItem('asad:auth', currentUser);
    loadApp();
}
function restoreSession() {
    const savedUser = sessionStorage.getItem('asad:auth');
    if (savedUser) { currentUser = savedUser; loadApp(); }
}
function loadApp() {
    document.getElementById('login-view').classList.remove('active');
    document.getElementById('app-view').classList.add('active');
    document.getElementById('role-badge').textContent = currentUser === 'owner' ? 'Owner' : 'Staff';
    
    const ibUpdate = document.getElementById('ib-update');
    if (ibUpdate) ibUpdate.innerHTML = ico('refresh');
    const ibBackup = document.getElementById('ib-backup');
    if (ibBackup) ibBackup.innerHTML = ico('update');
    const ibLogout = document.getElementById('ib-logout');
    if (ibLogout) ibLogout.innerHTML = ico('logout');

    document.getElementById('pin-input').value = '';
    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    document.getElementById('app-title').textContent = bizName;
    
    buildNav();
    nav('dashboard');
}

function logout() {
    currentUser = null;
    sessionStorage.removeItem('asad:auth');
    document.getElementById('app-view').classList.remove('active');
    document.getElementById('login-view').classList.add('active');
}
function buildNav() {
    const navEl = document.getElementById('bottom-nav');
    const t = i18n[settings.lang];
    const item = (v, icon, isLarge = false) => `<button class="nav-btn ${isLarge ? 'nav-btn-large' : ''}" data-view="${v}" onclick="nav('${v}')"><span class="pill">${ico(icon)}</span>${t[v] || v}</button>`;
    
    let html = '';
    html += item('dashboard', 'box');       // 1. Stock
    html += item('expenses', 'expenses');   // 2. Expenses
    
    html += item('sales', 'sales', true);   // 3. Sales (Large Middle)
    
    if (currentUser === 'owner') { 
        html += item('analytics', 'dashboard'); // 4. Analytics
    } else { 
        html += item('debts', 'debts');         // 4. Debts
    }
    
    // 5. Settings
    html += `<button class="nav-btn" onclick="openSettings()"><span class="pill">${ico('settings')}</span>${t.settings || 'Settings'}</button>`;
    
    navEl.innerHTML = html;
}

function nav(view) {
    currentView = view;
    if (view === 'inventory') view = 'dashboard';
    
    document.querySelectorAll('.nav-btn').forEach(b => {
        if (b.dataset.view) {
            b.classList.toggle('active', b.dataset.view === view);
        }
    });
    
    const main = document.getElementById('main-content');
    main.innerHTML = '';
    main.scrollTop = 0;
    
    try {
        if (view === 'dashboard') renderDashboard(main);
        else if (view === 'analytics') renderAnalytics(main);
        else if (view === 'sales') renderSales(main);
        else if (view === 'production') renderProduction(main);
        else if (view === 'expenses') renderExpenses(main);
        else if (view === 'debts') renderDebts(main);
        else if (view === 'reports') renderReports(main);
    } catch (e) {
        console.error(e);
        main.innerHTML = `<div style="padding:20px;text-align:center;color:var(--danger);">Error loading page: ${e.message}</div>`;
    }
}

function openSettings() {
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
            <div class="form-group"><label>4" Block</label><input type="number" id="set-price-4" value="${settings.defaultPrices['4'] || ''}" placeholder="0"></div>
            <div class="form-group"><label>6" Block</label><input type="number" id="set-price-6" value="${settings.defaultPrices['6'] || ''}" placeholder="0"></div>
            <div class="form-group"><label>9" Block</label><input type="number" id="set-price-9" value="${settings.defaultPrices['9'] || ''}" placeholder="0"></div>
        </div>
        <div class="eyebrow">Standard Mix Ratios</div>
        <div class="row">
            <div class="form-group"><label>Blocks per Cement Bag</label><input type="number" id="set-mix-cement" value="${settings.mixCement || ''}" placeholder="0"></div>
            <div class="form-group"><label>Blocks per Sand Bag</label><input type="number" id="set-mix-sand" value="${settings.mixSand || ''}" placeholder="0"></div>
        </div>
        <div class="form-group" style="margin-top:16px;">
            <label>Sales Reminder</label>
            <select id="set-reminder">
                <option value="" placeholder="0" ${settings.reminderInterval == 0 ? 'selected' : ''}>Off</option>
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
        <button class="btn btn-outline" style="margin-top:10px;" onclick="openDirectory()">📂 Customer & Supplier Directory</button>
        <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>
        <button class="btn btn-danger" style="margin-top:22px;" onclick="clearAllData()">${t.clearData}</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function addExpenseCategory() {
    const val = document.getElementById('set-new-expense').value.trim();
    if (!val) return;
    if (!settings.customExpenses.includes(val)) {
        settings.customExpenses.push(val);
        saveData('settings', settings);
        showToast('Category added', 'success');
        document.getElementById('set-new-expense').value = '';
    } else {
        showToast('Category already exists', 'err');
    }
}

function saveSettings() {
    const newLang = document.getElementById('set-lang').value;
    const langChanged = newLang !== settings.lang;
    settings.lang = newLang;
    settings.darkMode = document.getElementById('set-dark-mode').checked;
    if(settings.darkMode) document.body.classList.add('dark');
    else document.body.classList.remove('dark');
    
    settings.reminderInterval = parseInt(document.getElementById('set-reminder').value);
    if (settings.reminderInterval > 0 && Notification.permission !== 'granted') {
        Notification.requestPermission().then(perm => { if (perm === 'granted') setupReminders(); });
    } else { setupReminders(); }

    settings.mixCement = parseInt(document.getElementById('set-mix-cement').value) || 50;
    settings.mixSand = parseInt(document.getElementById('set-mix-sand').value) || 500;
    settings.defaultPrices = {
        '4': parseFloat(document.getElementById('set-price-4').value) || 0,
        '6': parseFloat(document.getElementById('set-price-6').value) || 0,
        '9': parseFloat(document.getElementById('set-price-9').value) || 0
    };
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

function clearAllData() {
    const t = i18n[settings.lang];
    showDialog("Enter Owner PIN", t.confirmClear, (pin) => {
        if (pin === settings.ownerPin) {
            showDialog("WARNING!", "This will permanently delete all sales, expenses, and production data. Are you sure?", () => {
                localStorage.clear();
                location.reload();
            });
        } else if (pin !== null) {
            showToast(t.wrongPin, 'err');
        }
    }, true);
}

function renderDashboard(main) {
    const t = i18n[settings.lang];
    const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
    const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const cementAdj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
    const cementStock = cementPurchased - cementUsed + cementAdj;

    const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
    const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
    const sandAdj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
    const sandStock = sandPurchased - sandUsed + sandAdj;

    const emptyBagsProduced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const emptyBagsSold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
    const emptyBagsAdj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
    const emptyBagsStock = emptyBagsProduced - emptyBagsSold + emptyBagsAdj;

    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
    const sold = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
    const broken = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
    const returned = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
    const blockStock = produced - sold - broken + returned;

    const tile = (title, stock, type, size) => `
        <div class="stock-tile" style="cursor:pointer; padding: 16px; display: flex; flex-direction: column; justify-content: center; align-items: center; transition: 0.2s;" onclick="openStockItem('${type}', '${size}')">
            <div class="k" style="font-size: 11px; font-weight:700; text-align:center;">${title}</div>
            <div class="n" style="font-size: 24px; margin: 8px 0;">${stock}</div>
            <div style="font-size: 10px; color: var(--brand); font-weight: 700;">View Details ›</div>
        </div>
    `;

    main.innerHTML = `
        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="nav('production')" style="flex: 1 1 30%;">${ico('production')} Prod</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>
        <div class="page-title">Stock & Inventory</div>
        <div class="page-sub">Tap any item to manage stock and view history</div>

        <div class="card">
            <h3>${ico('box')} Raw Materials</h3>
            <div class="stock-grid" style="grid-template-columns: repeat(3, 1fr);">
                ${tile('Cement', cementStock, 'cement', '')}
                ${tile('Sand', sandStock, 'sand', '')}
                ${tile('Empty Bags', emptyBagsStock, 'empty_bag', '')}
            </div>
        </div>

        <div class="card">
            <h3>${ico('production')} Finished Blocks</h3>
            <div class="stock-grid">
                ${tile('6" Blocks', blockStock, 'block', '6')}
            </div>
        </div>
    `;
}

function openStockItem(type, size) {
    let title = '';
    let currentStock = 0;
    let historyHtml = '';
    let hist = [];

    if (type === 'cement' || type === 'sand' || type === 'empty_bag') {
        title = type === 'cement' ? 'Cement' : (type === 'sand' ? 'Sand' : 'Empty Bags');
        if (type === 'cement') {
            const purchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        } else if (type === 'sand') {
            const purchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
            const used = batches.reduce((s,b)=>s+(b.sandQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased - used + adj;
        } else {
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const sold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
            currentStock = produced - sold + adj;
        }

        purchases.filter(p=>p.material===type).forEach(p => hist.push({ id: p.id, clickType: 'pur', date: p.date, desc: `Purchase from ${p.supplierName}`, qty: `+${p.qty}`, color: 'var(--brand)' }));
        stockAdjustments.filter(a=>a.material===type).forEach(a => hist.push({ date: a.date, desc: `Adjustment: ${a.reason}`, qty: a.qty > 0 ? `+${a.qty}` : `${a.qty}`, color: a.qty > 0 ? 'var(--brand)' : 'var(--danger)' }));
        
        if(type === 'empty_bag') {
            batches.forEach(b => { if(b.cementBags > 0) hist.push({ date: b.date, desc: `Generated from cement usage`, qty: `+${b.cementBags}`, color: 'var(--brand)' }); });
            sales.forEach(s => { if(s.emptyBagQty > 0) hist.push({ id: s.id, clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.emptyBagQty}`, color: 'var(--danger)' }); });
        } else {
            batches.forEach(b => {
                if(type === 'cement' && b.cementBags > 0) hist.push({ date: b.date, desc: `Used in 6" batch`, qty: `-${b.cementBags}`, color: 'var(--danger)' });
                if(type === 'sand' && b.sandQty > 0) hist.push({ date: b.date, desc: `Used in 6" batch`, qty: `-${b.sandQty}`, color: 'var(--danger)' });
            });
        }
    } else {
        title = '6" Blocks';
        const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === '6').reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === '6').reduce((s, r) => s + r.quantity, 0);
        currentStock = produced - sold - broken + returned;

        readyBatches.forEach(b => hist.push({ date: b.date, desc: `Produced (${b.worker})`, qty: `+${b.blocksProduced}`, color: 'var(--brand)' }));
        sales.filter(s=>s.size==='6').forEach(s => hist.push({ id: s.id, clickType: 'sale', date: s.date, desc: `Sold to ${s.customerName}`, qty: `-${s.quantity}`, color: 'var(--danger)' }));
        breakagesLog.filter(b=>b.size==='6').forEach(b => hist.push({ date: b.date, desc: `Breakage: ${b.reason}`, qty: `-${b.blocks}`, color: 'var(--danger)' }));
    }

    hist.sort((a,b) => new Date(b.date) - new Date(a.date));
    
    historyHtml = hist.slice(0, 20).map(h => {
        let clickAttr = '';
        if (h.clickType === 'pur') clickAttr = `onclick="openPurchaseDetails('${h.id}')" style="cursor:pointer;"`;
        if (h.clickType === 'sale') clickAttr = `onclick="openSaleDetails('${h.id}')" style="cursor:pointer;"`;
        return `<div class="kv" ${clickAttr}><span>${h.date} · ${h.desc}</span><strong style="color:${h.color};">${h.qty}</strong></div>`;
    }).join('');

    document.getElementById('modal-body').innerHTML = `
        <h3>${title}</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted);">Current Stock</p>
            <p style="font-size:36px; font-weight:800; color:var(--brand);">${currentStock}</p>
        </div>
        
        <div class="row" style="margin-bottom:16px;">
            <button class="btn" style="margin-top:0; background:var(--brand);" onclick="openAddStock('${type}', '${size}')">+ Add Stock</button>
            <button class="btn" style="margin-top:0; background:var(--danger);" onclick="openSubtractStock('${type}', '${size}')">- Subtract</button>
        </div>
        
        <div class="eyebrow">Recent History</div>
        <div style="max-height: 250px; overflow-y:auto; border:1px solid var(--line); border-radius:8px; padding:0 12px; margin-bottom:16px;">
            ${historyHtml || '<p style="font-size:13px; color:var(--muted); padding:12px 0;">No history yet.</p>'}
        </div>
        
        <button class="btn btn-outline" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function openAddStock(type, size) {
    closeModal();
    if (type === 'cement' || type === 'sand' || type === 'empty_bag') {
        openPurchase();
        setTimeout(() => {
            if(document.getElementById('pur-mat')) {
                document.getElementById('pur-mat').value = type;
                document.getElementById('pur-qty').focus();
            }
        }, 100);
    } else {
        nav('production');
        setTimeout(() => {
            if(document.getElementById('p-size')) {
                document.getElementById('p-size').value = size;
                document.getElementById('p-blocks').focus();
            }
        }, 100);
    }
}

function openSubtractStock(type, size) {
    closeModal();
    if (type === 'cement' || type === 'sand' || type === 'empty_bag') {
        openAdjustStock();
        setTimeout(() => {
            if(document.getElementById('adj-mat')) {
                document.getElementById('adj-mat').value = type;
                document.getElementById('adj-qty').focus();
            }
        }, 100);
    } else {
        openBreakage(size);
    }
}

function toggleSection(id) {
    const container = document.getElementById(id);
    const icon = document.getElementById(id + '-icon');
    if (!container) return;
    const isNowHidden = container.style.display === 'none';
    container.style.display = isNowHidden ? 'block' : 'none';
    if (icon) icon.textContent = isNowHidden ? '▲' : '▼';
    localStorage.setItem('asad:' + id + 'Collapsed', isNowHidden ? 'false' : 'true');
}

function renderAnalytics(main) {
    if (currentUser !== 'owner') return nav('dashboard');
    const t = i18n[settings.lang];
    const today = getWATDate();
    const todayStr = getTodayStr();
    const weekAgo = new Date(today.getTime() - 7*24*60*60*1000).toISOString().split('T')[0];
    const monthAgo = new Date(today.getTime() - 30*24*60*60*1000).toISOString().split('T')[0];

    const totalReturnsAmount = returns.reduce((sum, r) => sum + (r.refundAmount || 0), 0);
    const allRevenue = sales.reduce((sum, s) => sum + s.totalAmount, 0) - totalReturnsAmount;
    const allCOGS = sales.reduce((sum, s) => sum + (s.quantity * getAvgCost(s.size)), 0);
    const allExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
    const netProfit = allRevenue - allCOGS - allExpenses;
    
    const cashIn = sales.reduce((sum, s) => sum + s.amountPaidAtSale, 0) + payments.reduce((sum, p) => sum + p.amount, 0);
    const cashInHand = cashIn - allExpenses;
    const moneyOwedToOwner = sales.filter(s => !s.writtenOff).reduce((sum, s) => sum + s.balanceOwing, 0);
    const moneyYouOwe = purchases.reduce((sum, p) => sum + Math.max(0, p.cost - (p.amountPaid || 0)), 0);
    
    let unsoldValue = 0;
    ['6'].forEach(sz => {
        const readyBatches = batches.filter(b => b.size === sz && b.status === 'ready');
        const produced = readyBatches.reduce((s,b)=>s+(b.blocksProduced - b.breakages),0);
        const sold = sales.filter(s => s.size === sz).reduce((s,v)=>s+v.quantity,0);
        const broken = breakagesLog.filter(b => b.size === sz).reduce((s,v)=>s+v.blocks,0);
        const returned = returns.filter(r => r.size === sz).reduce((s, r) => s + r.quantity, 0);
        const remaining = Math.max(0, produced - sold - broken + returned);
        unsoldValue += remaining * getAvgCost(sz);
    });

    const dayRev = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
    const weekRev = sales.filter(s => s.date >= weekAgo).reduce((sum, s) => sum + s.totalAmount, 0);
    const monthRev = sales.filter(s => s.date >= monthAgo).reduce((sum, s) => sum + s.totalAmount, 0);

    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const thisMonthRev = sales.filter(s => { const d = new Date(s.date); return d.getMonth() === currentMonth && d.getFullYear() === currentYear; }).reduce((sum, s) => sum + s.totalAmount, 0);
    const lastMonthDate = new Date(currentYear, currentMonth - 1, 1);
    const lastMonth = lastMonthDate.getMonth();
    const lastMonthYear = lastMonthDate.getFullYear();
    const lastMonthRev = sales.filter(s => { const d = new Date(s.date); return d.getMonth() === lastMonth && d.getFullYear() === lastMonthYear; }).reduce((sum, s) => sum + s.totalAmount, 0);

    let momChangeHtml = '';
    if (lastMonthRev > 0) {
        const diff = thisMonthRev - lastMonthRev;
        const pct = (diff / lastMonthRev) * 100;
        const isUp = diff >= 0;
        momChangeHtml = `<div style="display:flex; align-items:center; justify-content:center; gap:4px; font-size:11px; font-weight:800; color:${isUp ? 'var(--brand-dark)' : 'var(--danger)'}; margin-top:4px;">${isUp ? '↑' : '↓'} ${Math.abs(pct).toFixed(1)}% vs last month</div>`;
    } else if (thisMonthRev > 0) {
        momChangeHtml = `<div style="font-size:11px; font-weight:800; color:var(--brand-dark); margin-top:4px;">↑ New sales this month</div>`;
    }

    let chartHtml = ''; let maxDayRev = 0; const days = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date(today.getTime() - i*24*60*60*1000);
        const dStr = d.toISOString().split('T')[0];
        const rev = sales.filter(s => s.date === dStr).reduce((sum, s) => sum + s.totalAmount, 0);
        if (rev > maxDayRev) maxDayRev = rev;
        days.push({ date: dStr, day: d.toLocaleDateString('en-US', {weekday:'short'}), rev: rev });
    }
    days.forEach(d => {
        const pct = maxDayRev > 0 ? (d.rev / maxDayRev) * 100 : 0;
        chartHtml += `<div class="chart-bar" style="height:${pct}%;" title="${formatNaira(d.rev)}"><div class="chart-label">${d.day}</div></div>`;
    });

    const sizeTotals = { '6': 0 };
    sales.forEach(s => { if(sizeTotals[s.size] !== undefined) sizeTotals[s.size] += s.quantity; });
    let bestSizeHtml = '';
    Object.keys(sizeTotals).sort((a,b)=>sizeTotals[b]-sizeTotals[a]).forEach(size => {
        if (sizeTotals[size] > 0) bestSizeHtml += `<div class="kv"><span>${size}" Blocks</span><strong>${sizeTotals[size].toLocaleString()} pcs</strong></div>`;
    });

    const custTotals = {};
    sales.forEach(s => { custTotals[s.customerName] = (custTotals[s.customerName] || 0) + s.totalAmount; });
    let topCustHtml = ''; let rk = 0;
    Object.entries(custTotals).sort((a,b)=>b[1]-a[1]).slice(0,3).forEach(([name, amt]) => {
        rk++;
        topCustHtml += `<div class="kv"><span><span class="rank">${rk}</span>${name}</span><strong>${formatNaira(amt)}</strong></div>`;
    });

    let profitHtml = '';
    ['4','6','9'].forEach(sz => {
        const szSales = sales.filter(s => s.size === sz);
        const totalQty = szSales.reduce((sum, s) => sum + s.quantity, 0);
        const totalAmt = szSales.reduce((sum, s) => sum + s.totalAmount, 0);
        const avgSellPrice = totalQty > 0 ? (totalAmt / totalQty) : 0;
        const avgCost = getAvgCost(sz);
        const profit = avgSellPrice - avgCost;
        if (avgSellPrice > 0) profitHtml += `<div class="kv"><span><strong>${sz}"</strong> <span style="color:var(--muted); font-size:12px;">Sell ${formatNaira(avgSellPrice)}</span></span><strong class="${profit >= 0 ? 'pos' : 'neg'}">${formatNaira(profit)}</strong></div>`;
    });

    let marginAlertHtml = '';
    sales.forEach(s => {
        const avgCost = getAvgCost(s.size);
        const minPrice = avgCost * (1 + (settings.marginAlertPct/100));
        if (s.pricePerBlock < minPrice && avgCost > 0) marginAlertHtml += `<div class="list-item alert"><div class="list-header"><span>${s.customerName}</span><span>${formatNaira(s.pricePerBlock)}/block</span></div><div class="list-sub">${t.marginWarning} (Cost: ${formatNaira(avgCost)})</div></div>`;
    });

    const totalQtySold = sales.reduce((sum, s) => sum + s.quantity, 0);
    const profitPerBlock = totalQtySold > 0 ? (allRevenue - allCOGS) / totalQtySold : 0;
    let breakEvenText = "Set fixed costs in Settings";
    if (settings.fixedCostsMonthly > 0) breakEvenText = profitPerBlock > 0 ? Math.ceil(settings.fixedCostsMonthly / profitPerBlock).toLocaleString() + " blocks/month" : "Log sales to calculate";

    const cementPurchased = purchases.filter(p=>p.material==='cement').reduce((s,p)=>s+p.qty,0);
    const cementUsed = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const cementAdj = stockAdjustments.filter(a=>a.material==='cement').reduce((s,a)=>s+a.qty,0);
    const cementStock = cementPurchased - cementUsed + cementAdj;
    const sandPurchased = purchases.filter(p=>p.material==='sand').reduce((s,p)=>s+p.qty,0);
    const sandUsed = batches.reduce((s,b)=>s+(b.sandQty||0),0);
    const sandAdj = stockAdjustments.filter(a=>a.material==='sand').reduce((s,a)=>s+a.qty,0);
    const sandStock = sandPurchased - sandUsed + sandAdj;

    let lowStockHtml = '';
    if (cementStock <= settings.lowCement) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🪨 Cement</span><span>${cementStock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;
    if (sandStock <= settings.lowSand) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🏖️ Sand</span><span>${sandStock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;

    let alertWrapper = '';
    if (lowStockHtml) {
        const isCollapsed = localStorage.getItem('asad:alertsCollapsed') === 'true';
        alertWrapper = `
            <div style="margin-bottom:16px;">
                <div class="section-title neg" onclick="toggleAlerts()" style="margin-top:0; margin-bottom:0; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:var(--danger-soft); padding:12px 16px; border-radius:12px; border:1px solid #f7bcbc;">
                    <span style="display:flex; align-items:center; gap:8px;">${ico('alert')} Low Stock Alerts</span>
                    <span id="alert-toggle-icon" style="font-size:12px;">${isCollapsed ? '▼' : '▲'}</span>
                </div>
                <div id="alert-list-container" style="display:${isCollapsed ? 'none' : 'block'}; margin-top:12px;">${lowStockHtml}</div>
            </div>
        `;
    }

    const currentMonthExp = expenses.filter(e => e.date.startsWith(todayStr.substring(0,7)));
    const totalExpAmt = currentMonthExp.reduce((sum, e) => sum + e.amount, 0);
    const expByCat = {};
    currentMonthExp.forEach(e => { expByCat[e.category] = (expByCat[e.category] || 0) + e.amount; });
    let expChartHtml = '';
    if (totalExpAmt > 0) {
        Object.keys(expByCat).sort((a,b)=>expByCat[b]-expByCat[a]).forEach(cat => {
            const pct = (expByCat[cat] / totalExpAmt) * 100;
            const catName = i18n[settings.lang][cat] || cat;
            expChartHtml += `<div style="margin-bottom:12px;"><div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; margin-bottom:4px;"><span style="text-transform:capitalize;">${catName}</span><span>${formatNaira(expByCat[cat])} (${pct.toFixed(0)}%)</span></div><div style="height:8px; background:var(--line); border-radius:4px; overflow:hidden;"><div style="height:100%; width:${pct}%; background:var(--danger); border-radius:4px;"></div></div></div>`;
        });
    } else expChartHtml = '<p style="font-size:13px; color:var(--muted);">No expenses logged this month.</p>';

    main.innerHTML = `
        <div class="quick" style="flex-wrap: wrap;">
            <button onclick="nav('dashboard')" style="flex: 1 1 30%;">${ico('box')} Stock</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>
        ${alertWrapper}
        <div class="hero">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="lbl">${t.netProfit}</div>
                    <div class="big ${netProfit < 0 ? 'neg' : ''}">${formatNaira(netProfit)}</div>
                </div>
                <div style="background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:20px; font-size:12px; font-weight:800; color:#f59e0b; display:flex; align-items:center; gap:4px;">🔥 ${settings.streak} Day Streak</div>
            </div>
            <div class="meta">
                <div>${t.revenue}<strong>${formatNaira(allRevenue)}</strong></div>
                <div>${t.expenses}<strong>${formatNaira(allExpenses)}</strong></div>
                <div>Best Day<strong>${formatNaira(settings.bestDayAmount)}</strong></div>
            </div>
        </div>
        <div class="dash-grid">
            <div class="stat"><div class="top"><span class="dot g">${ico('cash')}</span><h4>${t.cashInHand}</h4></div><div class="val">${formatNaira(cashInHand)}</div></div>
            <div class="stat"><div class="top"><span class="dot a">${ico('arrowIn')}</span><h4>${t.moneyOwed}</h4></div><div class="val">${formatNaira(moneyOwedToOwner)}</div></div>
            <div class="stat"><div class="top"><span class="dot r">${ico('arrowOut')}</span><h4>${t.moneyYouOwe}</h4></div><div class="val ${moneyYouOwe > 0 ? 'neg' : ''}">${formatNaira(moneyYouOwe)}</div></div>
            <div class="stat"><div class="top"><span class="dot b">${ico('box')}</span><h4>${t.stockValue}</h4></div><div class="val">${formatNaira(unsoldValue)}</div></div>
        </div>
        ${marginAlertHtml ? `<div class="section-title neg" style="margin-top:8px;">${ico('alert')} Alerts</div>${marginAlertHtml}` : ''}
        <div class="card">
            <h3>${ico('bars')} ${t.turnover}</h3>
            <div class="periods">
                <div><small>Today</small><strong>${formatNaira(dayRev)}</strong></div>
                <div><small>This Week</small><strong>${formatNaira(weekRev)}</strong></div>
                <div><small>This Month</small><strong>${formatNaira(monthRev)}</strong>${momChangeHtml}</div>
            </div>
            <div class="chart-container">${maxDayRev > 0 ? chartHtml : '<p style="font-size:13px; color:var(--muted); width:100%; text-align:center; align-self:center;">No sales data yet.</p>'}</div>
        </div>
        <div class="card">
            <h3>${ico('expenses')} Expense Breakdown</h3>
            ${expChartHtml}
        </div>
        <div class="card">
            <h3>${ico('trend')} ${t.profitMargins}</h3>
            ${profitHtml || '<p style="font-size:13px; color:var(--muted);">Log sales to see profit margins.</p>'}
        </div>
        <div class="card"><h3>${ico('trophy')} ${t.bestSizes}</h3>${bestSizeHtml || '<p style="font-size:13px; color:var(--muted);">No data</p>'}</div>
        <div class="card"><h3>${ico('users')} ${t.topCustomers}</h3>${topCustHtml || '<p style="font-size:13px; color:var(--muted);">No data</p>'}</div>
        <div class="card breakeven">
            <h3>${ico('target')} Break-even (Monthly)</h3>
            <p style="font-size:13px; color:#94a3b8;">Based on fixed costs of <strong style="color:#fff;">${formatNaira(settings.fixedCostsMonthly)}</strong></p>
            <div style="font-size:24px; font-weight:800; margin-top:8px; color:#34d399; letter-spacing:-.5px;">${breakEvenText}</div>
        </div>
    `;
}

function toggleAlerts() {
    const container = document.getElementById('alert-list-container');
    const icon = document.getElementById('alert-toggle-icon');
    if (!container) return;
    if (container.style.display === 'none') { container.style.display = 'block'; icon.textContent = '▲'; localStorage.setItem('asad:alertsCollapsed', 'false'); }
    else { container.style.display = 'none'; icon.textContent = '▼'; localStorage.setItem('asad:alertsCollapsed', 'true'); }
}

function getAvgCost(size) {
    const sizeBatches = batches.filter(b => b.size === size);
    if (sizeBatches.length === 0) return 0;
    const totalCost = sizeBatches.reduce((sum, b) => sum + b.totalCost, 0);
    const totalBlocks = sizeBatches.reduce((sum, b) => sum + b.blocksProduced, 0);
    return totalBlocks > 0 ? (totalCost / totalBlocks) : 0;
}

function renderInventory(main) { renderDashboard(main); } // Fallback for old links

function acceptVariance(size, expected, physical) {
    const diff = expected - physical;
    if (diff > 0) { breakagesLog.push({ id: Date.now().toString(), date: getTodayStr(), size: size, blocks: diff, reason: 'Stock Variance Adjustment' }); saveData('breakages', breakagesLog); }
    else if (diff < 0) { batches.push({ id: Date.now().toString(), date: getTodayStr(), size: size, worker: 'System Adjustment', blocksProduced: Math.abs(diff), breakages: 0, curingLoss: 0, totalCost: 0, costPerBlock: 0, status: 'ready' }); saveData('batches', batches); }
    delete stockCounts[size]; saveData('stockCounts', stockCounts); nav('dashboard'); showToast('System adjusted to match physical count', 'success');
}

function openBreakage(size) {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.logBreakage} · ${size}"</h3>
        <div class="form-group"><label>${t.qty}</label><input type="number" id="break-qty" value="1" min="1"></div>
        <div class="form-group"><label>${t.breakageReason}</label><input type="text" id="break-reason" placeholder="e.g. Transport, Storage"></div>
        <button class="btn" onclick="saveBreakage('${size}')">Save</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function saveBreakage(size) {
    const qty = parseInt(document.getElementById('break-qty').value) || 0;
    if (qty <= 0) return showToast('Enter valid quantity', 'err');
    breakagesLog.push({ id: Date.now().toString(), date: getTodayStr(), size: size, blocks: qty, reason: document.getElementById('break-reason').value || 'Unknown' });
    saveData('breakages', breakagesLog); closeModal(); nav('dashboard'); showToast('Breakage logged', 'success');
}

function openPurchase() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.logPurchase}</h3>
        <div class="form-group"><label>${t.supplierName}</label><input type="text" id="pur-supplier" list="supplier-names" placeholder="e.g. Dangote"><datalist id="supplier-names"></datalist></div>
        <div class="form-group"><label>Material</label><select id="pur-mat"><option value="cement">${t.cement}</option><option value="sand">${t.sand}</option><option value="empty_bag">${t.empty_bag}</option></select></div>
        <div class="row">
            <div class="form-group"><label>Qty</label><input type="number" id="pur-qty" value="" placeholder="0" oninput="calcPurchase()"></div>
            <div class="form-group"><label>Cost per Unit (₦)</label><input type="number" id="pur-unit-cost" value="" placeholder="0" oninput="calcPurchase()"></div>
        </div>
        <div class="calc-box">
            <div class="line"><span>Total Cost</span> <span>₦<span id="pur-total-display">0</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="pur-balance-display">0</span></span></div>
        </div>
        <div class="form-group"><label>${t.paid}</label><input type="number" id="pur-paid" value="" placeholder="0" oninput="calcPurchase()"></div>
        <button class="btn" onclick="savePurchase()">Save</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    const uniqueSuppliers = [...new Set(purchases.map(p => p.supplierName).filter(n => n && n !== 'Unknown'))];
    document.getElementById('supplier-names').innerHTML = uniqueSuppliers.map(name => `<option value="${name}"></option>`).join('');
    document.getElementById('modal').classList.add('active');
    calcPurchase();
}

function calcPurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    
    const total = qty * unitCost;
    const balance = total - paid;
    
    document.getElementById('pur-total-display').textContent = total.toLocaleString();
    document.getElementById('pur-balance-display').textContent = balance.toLocaleString();
}

function savePurchase() {
    const qty = parseFloat(document.getElementById('pur-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('pur-unit-cost').value) || 0;
    const cost = qty * unitCost;
    const paid = parseFloat(document.getElementById('pur-paid').value) || 0;
    
    if (qty <= 0) return showToast('Enter valid quantity', 'err');
    
    purchases.push({ id: Date.now().toString(), date: getTodayStr(), supplierName: document.getElementById('pur-supplier').value || 'Unknown', material: document.getElementById('pur-mat').value, qty: qty, cost: cost, amountPaid: paid });
    saveData('purchases', purchases); closeModal();
    if (currentView === 'debts') { currentDebtTab = 'supplier'; nav('debts'); } else { nav('dashboard'); }
    showToast('Purchase logged', 'success');
}

let currentAdjType = 'add';

function setAdjType(type) {
    currentAdjType = type;
    document.getElementById('adj-btn-add').classList.toggle('on', type === 'add');
    document.getElementById('adj-btn-sub').classList.toggle('on', type === 'subtract');
}

function openAdjustStock() {
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

function saveAdjustStock() {
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

function openPurchaseDetails(id) {
    const p = purchases.find(x => x.id === id);
    if (!p) return;
    document.getElementById('modal-body').innerHTML = `
        <h3>Purchase Details</h3>
        <div class="kv"><span>Supplier</span><strong>${p.supplierName}</strong></div>
        <div class="kv"><span>Material</span><strong>${p.material.toUpperCase()}</strong></div>
        <div class="kv"><span>Quantity</span><strong>${p.qty}</strong></div>
        <div class="kv"><span>Total Cost</span><strong>₦${p.cost.toLocaleString()}</strong></div>
        <div class="kv"><span>Amount Paid</span><strong>₦${(p.amountPaid || 0).toLocaleString()}</strong></div>
        <div class="row" style="margin-top:24px;"><button class="btn btn-outline" onclick="closeModal()">Close</button><button class="btn" onclick="editPurchase('${p.id}')">Edit Purchase</button></div>
    `;
    document.getElementById('modal').classList.add('active');
}
function editPurchase(id) {
    const p = purchases.find(x => x.id === id);
    const unitCost = p.qty > 0 ? (p.cost / p.qty) : 0;
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Purchase</h3>
        <div class="form-group"><label>Supplier Name</label><input type="text" id="edit-p-supplier" value="${p.supplierName}"></div>
        <div class="form-group"><label>Material</label><select id="edit-p-mat"><option value="cement" ${p.material==='cement'?'selected':''}>Cement</option><option value="sand" ${p.material==='sand'?'selected':''}>Sand</option><option value="empty_bag" ${p.material==='empty_bag'?'selected':''}>Empty Bags</option></select></div>
        <div class="row">
            <div class="form-group"><label>Quantity</label><input type="number" id="edit-p-qty" value="${p.qty || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
            <div class="form-group"><label>Cost per Unit</label><input type="number" id="edit-p-unit-cost" value="${unitCost || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
        </div>
        <div class="calc-box">
            <div class="line"><span>Total Cost</span> <span>₦<span id="edit-p-total-display">${p.cost.toLocaleString()}</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="edit-p-balance-display">${(p.cost - (p.amountPaid || 0)).toLocaleString()}</span></span></div>
        </div>
        <div class="form-group"><label>Amount Paid</label><input type="number" id="edit-p-paid" value="${p.amountPaid || ''}" placeholder="0" oninput="calcEditPurchase()"></div>
        <div class="row"><button class="btn btn-outline" onclick="openPurchaseDetails('${p.id}')">Back</button><button class="btn" onclick="saveEditedPurchase('${p.id}')">Save Changes</button></div>
    `;
}

function calcEditPurchase() {
    const qty = parseFloat(document.getElementById('edit-p-qty').value) || 0;
    const unitCost = parseFloat(document.getElementById('edit-p-unit-cost').value) || 0;
    const paid = parseFloat(document.getElementById('edit-p-paid').value) || 0;
    
    const total = qty * unitCost;
    const balance = total - paid;
    
    document.getElementById('edit-p-total-display').textContent = total.toLocaleString();
    document.getElementById('edit-p-balance-display').textContent = balance.toLocaleString();
}

function saveEditedPurchase(id) {
    const p = purchases.find(x => x.id === id);
    p.supplierName = document.getElementById('edit-p-supplier').value || 'Unknown';
    p.material = document.getElementById('edit-p-mat').value;
    p.qty = parseFloat(document.getElementById('edit-p-qty').value) || 0;
    p.cost = p.qty * (parseFloat(document.getElementById('edit-p-unit-cost').value) || 0);
    p.amountPaid = parseFloat(document.getElementById('edit-p-paid').value) || 0;
    saveData('purchases', purchases); closeModal(); nav('dashboard'); showToast('Purchase updated', 'success');
}

function openStockCheck(size, expected) {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.stockCheck} · ${size}"</h3>
        <div class="calc-box"><div class="line"><span>${t.expected}</span><span>${expected} pcs</span></div></div>
        <div class="form-group"><label>${t.physicalCount}</label><input type="number" id="check-count" value="${expected}"></div>
        <button class="btn" onclick="verifyStock('${size}', ${expected})">Verify</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function verifyStock(size, expected) {
    const counted = parseInt(document.getElementById('check-count').value) || 0;
    if (counted === expected) { showToast('Stock matches perfectly!', 'success'); delete stockCounts[size]; saveData('stockCounts', stockCounts); }
    else { stockCounts[size] = counted; saveData('stockCounts', stockCounts); }
    closeModal(); nav('dashboard');
}

function renderReports(main) {
    const t = i18n[settings.lang];
    const currentMonth = getTodayStr().slice(0, 7);
    main.innerHTML = `
        ${backBtn('analytics')}
        <div class="page-title">${t.reports}</div>
        <div class="page-sub">Monthly performance and data backup</div>
        <div class="card">
            <h3>${ico('report')} ${t.plReport}</h3>
            <div class="form-group"><label>${t.month}</label><input type="month" id="rep-month" value="${currentMonth}" onchange="calcPL()"></div>
            <div id="pl-results"></div>
            <button class="btn btn-dark" onclick="exportCSV()" style="margin-top:0;">${t.exportCSV}</button>
            <button class="btn btn-outline" onclick="printDocument()">Print / PDF</button>
        </div>
        <div class="card">
            <h3>${ico('update')} Backup & Restore</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom:14px;">Save your data to a file or restore from a previous backup.<br><br><strong style="color:var(--warning);">Recommendation:</strong> Always save your backup to Google Drive, WhatsApp, or email. If you lose this phone, this file is the <strong>only</strong> way to recover your data.</p>
            <button class="btn btn-blue" style="margin-top:0;" onclick="exportJSON()">📤 Share Backup File</button>
            <input type="file" id="import-file" accept=".json,.txt" style="display:none;" onchange="importJSON(event)">
            <button class="btn btn-outline" onclick="document.getElementById('import-file').click()">${t.importJSON}</button>
        </div>
    `;
    calcPL();
}
function calcPL() {
    const t = i18n[settings.lang];
    const month = document.getElementById('rep-month').value;
    if(!month) return;
    const mSales = sales.filter(s => s.date.startsWith(month));
    const mExp = expenses.filter(e => e.date.startsWith(month));
    const rev = mSales.reduce((s,v)=>s+v.totalAmount, 0);
    const cogs = mSales.reduce((s,v)=>s+(v.quantity * getAvgCost(v.size)), 0);
    const exp = mExp.reduce((s,v)=>s+v.amount, 0);
    const net = rev - cogs - exp;
    document.getElementById('pl-results').innerHTML = `<div style="margin-bottom:16px; font-size:14px; background:#f8fafc; border:1px solid var(--line); padding:6px 16px; border-radius:12px;"><div class="kv"><span>${t.revenue}</span> <strong>${formatNaira(rev)}</strong></div><div class="kv"><span>${t.cogs}</span> <strong>-${formatNaira(cogs)}</strong></div><div class="kv"><span>${t.grossProfit}</span> <strong>${formatNaira(rev-cogs)}</strong></div><div class="kv"><span>${t.expenses}</span> <strong>-${formatNaira(exp)}</strong></div><div class="kv" style="font-size:16px; font-weight:800;"><span>${t.netProfit}</span> <span class="${net>=0?'pos':'neg'}">${formatNaira(net)}</span></div></div>`;
}
function exportCSV() {
    let csv = "Type,Date,Description,Amount(NGN)\n";
    sales.forEach(s => { csv += `Sale,${s.date},${s.customerName} - ${s.size}" x${s.quantity},${s.totalAmount}\n`; });
    expenses.forEach(e => { csv += `Expense,${e.date},${e.category},${e.amount}\n`; });
    batches.forEach(b => { csv += `Production,${b.date},${b.size}" Blocks - ${b.blocksProduced} pcs,${b.totalCost}\n`; });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = `AsadTech_Report_${getTodayStr()}.csv`; a.click(); showToast('CSV Exported', 'success');
}
async function exportJSON() {
    const data = {};
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('asad:')) { try { data[key] = JSON.parse(localStorage.getItem(key)); } catch(e) { data[key] = localStorage.getItem(key); } }
    }
    const jsonStr = JSON.stringify(data, null, 2);
    const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_₦/g, '');
    const now = new Date(); const timeStr = now.toTimeString().split(' ')[0].replace(/:/g, '-');
    const filename = `${safeName}_Backup_${getTodayStr()}_${timeStr}.txt`;
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const file = new File([blob], filename, { type: 'application/json' });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try { await navigator.share({ files: [file], title: 'Business Backup' }); showToast('Backup shared', 'success'); return; } 
        catch (e) { if (e.name === 'AbortError') return; }
    }
    document.getElementById('modal-body').innerHTML = `
        <h3>Save Backup File</h3>
        <p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Tap Download to save to your phone, or Copy to paste it into Google Keep/Notes.</p>
        <textarea id="backup-text" style="width:100%; height:150px; font-family:monospace; font-size:12px; padding:10px; border-radius:8px; border:1px solid var(--line); margin-bottom:12px;" readonly>${jsonStr}</textarea>
        <div class="row">
            <button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('backup-text').value).then(()=>showToast('Copied to clipboard!','success'))">📋 Copy</button>
            <button class="btn" onclick="downloadBackup('${filename}', document.getElementById('backup-text').value)">📥 Download</button>
        </div>
    `;
    document.getElementById('modal').classList.add('active');
}
function downloadBackup(filename, content) {
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url); showToast('File downloaded', 'success');
}
function importJSON(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            if (!data['asad:settings']) throw new Error('Invalid backup file');
            Object.keys(data).forEach(key => { localStorage.setItem(key, JSON.stringify(data[key])); });
            showToast('Data restored successfully! Reloading...', 'success'); setTimeout(() => location.reload(), 1500);
        } catch (err) { showToast('Invalid JSON file: ' + err.message, 'err'); }
    };
    reader.readAsText(file);
}

function renderSales(main) { 
    const t = i18n[settings.lang];
    let historyHtml = '';
    const recentSales = [...sales].reverse().slice(0, 15);
    recentSales.forEach(s => {
        historyHtml += `<div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')"><div class="list-header"><span>${s.customerName}</span><strong class="pos">${formatNaira(s.totalAmount)}</strong></div><div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div><div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending</span>`}</div></div>`;
    });

    main.innerHTML = `
        <div class="card">
            <h3>${ico('plus')} ${t.newSale}</h3>
            
            <div class="eyebrow">Customer Info</div>
            <div class="form-group"><label>${t.customer}</label><input type="text" id="s-customer" list="customer-names" placeholder="Name" oninput="autofillPhone(this.value)"><datalist id="customer-names"></datalist></div>
            <div class="row">
                <div class="form-group"><label>${t.phone}</label><input type="tel" id="s-phone" placeholder="Phone"></div>
                <div class="form-group"><label>${t.date}</label><input type="date" id="s-date" value="${getTodayStr()}"></div>
            </div>

            <div class="eyebrow">Items Bought</div>
            <div style="background:var(--bg); padding:12px; border-radius:8px; margin-bottom:12px;">
                <div style="font-weight:700; font-size:13px; margin-bottom:8px;">Blocks</div>
                <div class="row">
                    <div class="form-group" style="flex:1.5;"><label>${t.size}</label><select id="s-size" onchange="updateDefaultPrice()"><option value="6">6"</option></select></div>
                    <div class="form-group" style="flex:1;"><label>Qty</label><input type="number" id="s-qty" value="" placeholder="0" oninput="calcSale()"></div>
                    <div class="form-group" style="flex:1.5;"><label>Price (₦)</label><input type="number" id="s-price" value="" placeholder="0" oninput="calcSale()"></div>
                </div>
            </div>

            <div class="row">
                <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="s-cement-qty" value="" placeholder="0" oninput="calcSale()"></div>
                <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="s-cement-price" value="" placeholder="0" oninput="calcSale()"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="s-sand-qty" value="" placeholder="0" oninput="calcSale()"></div>
                <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="s-sand-price" value="" placeholder="0" oninput="calcSale()"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Empty Bags Qty</label><input type="number" id="s-empty-bag-qty" value="" placeholder="0" oninput="calcSale()"></div>
                <div class="form-group"><label>Empty Bag Price (₦)</label><input type="number" id="s-empty-bag-price" value="" placeholder="0" oninput="calcSale()"></div>
            </div>

            <div class="eyebrow">Payment</div>
            <div class="row">
                <div class="form-group"><label>${t.delivery}</label><input type="number" id="s-delivery" value="" placeholder="0" oninput="calcSale()"></div>
                <div class="form-group"><label>${t.paid}</label><input type="number" id="s-paid" value="" placeholder="0" oninput="calcSale()"></div>
            </div>
            <div class="calc-box">
                <div class="line"><span>Total Amount</span> <span>₦<span id="s-total-display">0</span></span></div>
                <div class="line" style="color:var(--danger);"><span>${t.balance}</span> <span>₦<span id="s-balance-display">0</span></span></div>
            </div>
            
            <button class="btn" style="margin-top:0;" onclick="saveSale()">${t.save}</button>
        </div>
        <div class="section-title" style="display:flex; justify-content:space-between; align-items:center;"><span>${ico('sales')} ${t.salesHistory}</span><button class="btn btn-outline" style="width:auto; margin:0; padding:8px 12px; font-size:12px;" onclick="openReturn()">${t.logReturn || 'Log Return'}</button></div>
        <div class="form-group" style="margin-bottom:12px;"><input type="text" id="search-sales" placeholder="Search by customer name or date..." oninput="filterSales(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;"></div>
        <div id="sales-history-list">${historyHtml || `<div class="empty">${t.noSalesYet}</div>`}</div>
    `;
    const uniqueCustomers = {};
    sales.forEach(s => { if(s.customerName && s.customerPhone) uniqueCustomers[s.customerName] = s.customerPhone; });
    const custData = document.getElementById('customer-names');
    if(custData) custData.innerHTML = Object.keys(uniqueCustomers).map(name => `<option value="${name}"></option>`).join('');
    calcSale();
}

function updateDefaultPrice() { const size = document.getElementById('s-size').value; document.getElementById('s-price').value = settings.defaultPrices[size] || 0; calcSale(); }
function autofillPhone(name) { const match = sales.slice().reverse().find(s => s.customerName.toLowerCase() === name.toLowerCase()); if (match && match.customerPhone) document.getElementById('s-phone').value = match.customerPhone; }
function quickAdd(id, amount, calcFn) { const el = document.getElementById(id); el.value = (parseInt(el.value) || 0) + amount; if (typeof window[calcFn] === 'function') window[calcFn](); }
function calcSale() {
    const bQty = parseFloat(document.getElementById('s-qty')?.value) || 0;
    const bPrice = parseFloat(document.getElementById('s-price')?.value) || 0;
    const cQty = parseFloat(document.getElementById('s-cement-qty')?.value) || 0;
    const cPrice = parseFloat(document.getElementById('s-cement-price')?.value) || 0;
    const sQty = parseFloat(document.getElementById('s-sand-qty')?.value) || 0;
    const sPrice = parseFloat(document.getElementById('s-sand-price')?.value) || 0;
    const eQty = parseFloat(document.getElementById('s-empty-bag-qty')?.value) || 0;
    const ePrice = parseFloat(document.getElementById('s-empty-bag-price')?.value) || 0;
    const delivery = parseFloat(document.getElementById('s-delivery')?.value) || 0;
    const paid = parseFloat(document.getElementById('s-paid')?.value) || 0;
    
    const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;
    const balance = total - paid;
    
    const td = document.getElementById('s-total-display');
    if(td) td.textContent = total.toLocaleString();
    const bd = document.getElementById('s-balance-display');
    if(bd) bd.textContent = balance.toLocaleString();
}

function saveSale() {
    try {
        const qty = parseInt(document.getElementById('s-qty').value) || 0;
        const price = parseInt(document.getElementById('s-price').value) || 0;
        const delivery = parseInt(document.getElementById('s-delivery').value) || 0;
        const paid = parseInt(document.getElementById('s-paid').value) || 0;
        const saleDate = document.getElementById('s-date').value || getTodayStr();
        const custName = document.getElementById('s-customer').value || 'Walk-in';
        if(qty <= 0) return showToast('Enter valid quantity', 'err');
        const total = (qty * price) + delivery;
        const balance = total - paid;
        const limit = (settings.creditLimits && settings.creditLimits[custName]) ? settings.creditLimits[custName] : 0;
        if (limit > 0) {
            const existingOwed = sales.filter(s => s.customerName === custName).reduce((sum, s) => sum + (s.balanceOwing || 0), 0);
            if (existingOwed + balance > limit) {
                showDialog("Credit Limit Exceeded", `Total debt for <strong>${custName}</strong> will be <strong>${formatNaira(existingOwed + balance)}</strong>, exceeding their limit of <strong>${formatNaira(limit)}</strong>.<br><br>Proceed anyway?`, () => { executeSaveSale(qty, price, delivery, paid, saleDate, custName); });
                return;
            }
        }
        executeSaveSale(qty, price, delivery, paid, saleDate, custName);
    } catch (e) { showToast("Error saving sale: " + e.message, "err"); }
}
function executeSaveSale(qty, price, delivery, paid, saleDate, custName) {
    try {
        const cQty = parseInt(document.getElementById('s-cement-qty')?.value) || 0;
        const cPrice = parseFloat(document.getElementById('s-cement-price')?.value) || 0;
        const sQty = parseInt(document.getElementById('s-sand-qty')?.value) || 0;
        const sPrice = parseFloat(document.getElementById('s-sand-price')?.value) || 0;
        const eQty = parseInt(document.getElementById('s-empty-bag-qty')?.value) || 0;
        const ePrice = parseFloat(document.getElementById('s-empty-bag-price')?.value) || 0;
        
        const total = (qty * price) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;
        const balance = total - paid;

        let maxInv = 0;
        sales.forEach(s => { if(s.invoiceNo && typeof s.invoiceNo === 'string') { const num = parseInt(s.invoiceNo.replace('INV-', '')); if(!isNaN(num) && num > maxInv) maxInv = num; } });
        const nextInv = 'INV-' + (maxInv + 1).toString().padStart(4, '0');
        
        const sale = { 
            id: Date.now().toString(), 
            createdAt: getWATDate().toISOString(), 
            invoiceNo: nextInv, 
            date: saleDate, 
            customerName: custName, 
            customerPhone: document.getElementById('s-phone')?.value || '', 
            size: document.getElementById('s-size')?.value || '6', 
            quantity: qty, 
            pricePerBlock: price, 
            cementQty: cQty,
            cementPrice: cPrice,
            sandQty: sQty,
            sandPrice: sPrice,
            emptyBagQty: eQty,
            emptyBagPrice: ePrice,
            deliveryCharge: delivery, 
            totalAmount: total, 
            amountPaidAtSale: paid, 
            balanceOwing: balance, 
            deliveryStatus: 'pending'
        };
        
        sales.push(sale); saveData('sales', sales);
        
        if (navigator.vibrate) navigator.vibrate(50);
        
        const todayStr = getTodayStr();
        const todayTotal = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
        if (todayTotal > (settings.bestDayAmount || 0)) { 
            settings.bestDayAmount = todayTotal; saveData('settings', settings); triggerConfetti(); showToast(`🏆 NEW BEST DAY! ${formatNaira(todayTotal)}`, 'success'); 
        }

        const waText = buildWhatsAppReceipt(sale);
        const waPhone = (sale.customerPhone || '').replace(/^0/, '234');
        const waLink = `https://wa.me/${waPhone}?text=${waText}`;

        let itemsHtml = '';
        if (qty > 0) itemsHtml += `<div class="kv"><span>${qty} pcs of ${sale.size}" Blocks</span><strong>${formatNaira(qty * price)}</strong></div>`;
        if (cQty > 0) itemsHtml += `<div class="kv"><span>${cQty} bags of Cement</span><strong>${formatNaira(cQty * cPrice)}</strong></div>`;
        if (sQty > 0) itemsHtml += `<div class="kv"><span>${sQty} bags of Sand</span><strong>${formatNaira(sQty * sPrice)}</strong></div>`;
        if (eQty > 0) itemsHtml += `<div class="kv"><span>${eQty} Empty Bags</span><strong>${formatNaira(eQty * ePrice)}</strong></div>`;
        if (delivery > 0) itemsHtml += `<div class="kv"><span>Delivery Charge</span><strong>${formatNaira(delivery)}</strong></div>`;

        document.getElementById('modal-body').innerHTML = `
            <div style="text-align:center; margin-bottom:20px;">
                <div style="width:48px; height:48px; border-radius:50%; background:var(--brand-soft); color:var(--brand-dark); display:grid; place-items:center; margin:0 auto 10px;"><svg class="ic" style="width:24px;height:24px;stroke-width:2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
                <h3 style="margin-bottom:2px;">Sale Recorded</h3>
                <p style="font-size:12px; color:var(--muted);">${new Date().toLocaleString()}</p>
            </div>
            <div class="kv"><span>Invoice No.</span><strong>${sale.invoiceNo}</strong></div>
            <div class="kv"><span>Customer</span><strong>${sale.customerName}</strong></div>
            
            <div class="eyebrow" style="margin-top:8px;">Items</div>
            ${itemsHtml || '<p style="font-size:13px; color:var(--muted);">No items logged.</p>'}
            
            <div class="kv" style="border-bottom:2px solid var(--line); padding-bottom:12px; margin-bottom:12px; margin-top:12px;">
                <span style="font-size:16px; font-weight:800;">Total Amount</span>
                <strong style="font-size:20px; color:var(--brand); font-weight:800;">${formatNaira(total)}</strong>
            </div>
            
            <div class="kv"><span>Amount Paid</span><strong>${formatNaira(sale.amountPaidAtSale)}</strong></div>
            <div class="kv" style="border-bottom:none;"><span>Outstanding Balance</span><strong style="color:${balance > 0 ? 'var(--danger)' : 'var(--brand)'}; font-size:16px;">${formatNaira(balance)}</strong></div>
            
            <div class="actions" style="margin-top:24px; margin-bottom:10px;">
                <a href="${waLink}" target="_blank"><button class="wa" style="padding:14px; font-size:15px;">WhatsApp</button></a>
                <button onclick="shareReceiptImage('${sale.id}')" style="padding:14px; font-size:15px; background:var(--accent); color:#fff; border:none;">📸 Image</button>
            </div>
            <div class="row"><button class="btn btn-outline" onclick="printDocument()">Print</button><button class="btn btn-outline" onclick="closeModal(); nav('sales')">Close</button></div>`;
        document.getElementById('modal').classList.add('active');
    } catch (e) { showToast("Error: " + e.message, "err"); }
}

function openSaleDetails(saleId) {
    const s = sales.find(x => x.id === saleId);
    if (!s) return;
    
    let itemsHtml = '';
    if (s.quantity > 0) itemsHtml += `<div class="kv"><span>${s.quantity} pcs of ${s.size}" Blocks</span><strong>${formatNaira(s.quantity * s.pricePerBlock)}</strong></div>`;
    if (s.cementQty > 0) itemsHtml += `<div class="kv"><span>${s.cementQty} bags of Cement</span><strong>${formatNaira(s.cementQty * s.cementPrice)}</strong></div>`;
    if (s.sandQty > 0) itemsHtml += `<div class="kv"><span>${s.sandQty} bags of Sand</span><strong>${formatNaira(s.sandQty * s.sandPrice)}</strong></div>`;
    if (s.emptyBagQty > 0) itemsHtml += `<div class="kv"><span>${s.emptyBagQty} Empty Bags</span><strong>${formatNaira(s.emptyBagQty * s.emptyBagPrice)}</strong></div>`;
    if (s.deliveryCharge > 0) itemsHtml += `<div class="kv"><span>Delivery Charge</span><strong>${formatNaira(s.deliveryCharge)}</strong></div>`;

    document.getElementById('modal-body').innerHTML = `
        <h3>Receipt · ${s.customerName}</h3>
        <div style="text-align:center; margin-bottom:20px;">
            <p style="font-size:13px; color:var(--muted);">${s.date} ${s.createdAt ? new Date(s.createdAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : ''}</p>
            <p style="font-size:28px; font-weight:800; color:var(--brand); margin-top:8px;">${formatNaira(s.totalAmount)}</p>
            ${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger); margin-top:6px;">Owing ${formatNaira(s.balanceOwing)}</span>` : `<span class="tag green" style="margin-top:6px;">Fully paid</span>`}
        </div>
        <div class="kv"><span>Invoice No.</span><strong>${s.invoiceNo || 'N/A'}</strong></div>
        <div class="kv"><span>Phone</span><strong>${s.customerPhone || 'N/A'}</strong></div>
        
        <div class="eyebrow">Items Bought</div>
        ${itemsHtml || '<p style="font-size:13px; color:var(--muted);">No items logged.</p>'}
        
        <div class="eyebrow">Payment</div>
        <div class="kv"><span>Amount Paid</span><strong>${formatNaira(s.amountPaidAtSale)}</strong></div>
        
        <div class="actions" style="margin-top:24px; margin-bottom:12px;">
            <a href="https://wa.me/${(s.customerPhone || '').replace(/^0/, '234')}?text=${buildWhatsAppReceipt(s)}" target="_blank"><button class="wa">WhatsApp</button></a>
            <button onclick="shareReceiptImage('${s.id}')">📸 Image</button>
        </div>
        <div class="row">
            <button class="btn btn-outline" onclick="closeModal()">Close</button>
            <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
        </div>
        <button class="btn ${s.deliveryStatus === 'delivered' ? 'btn-outline' : 'btn-dark'}" style="margin-top:8px; ${s.deliveryStatus === 'delivered' ? 'border-color:var(--brand); color:var(--brand);' : ''}" onclick="toggleDelivery('${s.id}')">
            ${s.deliveryStatus === 'delivered' ? '✅ Mark as Pending' : '🚚 Mark as Delivered'}
        </button>
        <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteSale('${s.id}')">Delete Sale</button>
    `;
    document.getElementById('modal').classList.add('active');
}

function editSale(saleId) {
    const s = sales.find(x => x.id === saleId);
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Sale</h3>
        
        <div class="eyebrow">Customer Info</div>
        <div class="form-group"><label>Customer Name</label><input type="text" id="edit-s-customer" value="${s.customerName}"></div>
        <div class="row">
            <div class="form-group"><label>Phone</label><input type="tel" id="edit-s-phone" value="${s.customerPhone || ''}" placeholder="Phone"></div>
            <div class="form-group"><label>Date</label><input type="date" id="edit-s-date" value="${s.date}"></div>
        </div>

        <div class="eyebrow">Items Bought</div>
        <div style="background:var(--bg); padding:12px; border-radius:8px; margin-bottom:12px;">
            <div style="font-weight:700; font-size:13px; margin-bottom:8px;">Blocks</div>
            <div class="row">
                <div class="form-group" style="flex:1.5;"><label>Block Size</label><select id="edit-s-size"><option value="6">6"</option></select></div>
                <div class="form-group" style="flex:1;"><label>Qty</label><input type="number" id="edit-s-qty" value="${s.quantity || ''}" placeholder="0" oninput="calcEditSale()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('edit-s-qty', 50, 'calcEditSale')">+50</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('edit-s-qty', 100, 'calcEditSale')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('edit-s-qty', 500, 'calcEditSale')">+500</button></div></div>
                <div class="form-group" style="flex:1.5;"><label>Price (₦)</label><input type="number" id="edit-s-price" value="${s.pricePerBlock || ''}" placeholder="0" oninput="calcEditSale()"></div>
            </div>
        </div>

        <div class="row">
            <div class="form-group"><label>Cement Qty (Bags)</label><input type="number" id="edit-s-cement-qty" value="${s.cementQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Cement Price (₦)</label><input type="number" id="edit-s-cement-price" value="${s.cementPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Sand Qty (Bags)</label><input type="number" id="edit-s-sand-qty" value="${s.sandQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Sand Price (₦)</label><input type="number" id="edit-s-sand-price" value="${s.sandPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        <div class="row">
            <div class="form-group"><label>Empty Bags Qty</label><input type="number" id="edit-s-empty-bag-qty" value="${s.emptyBagQty || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Empty Bag Price (₦)</label><input type="number" id="edit-s-empty-bag-price" value="${s.emptyBagPrice || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>

        <div class="eyebrow">Payment</div>
        <div class="row">
            <div class="form-group"><label>Delivery Charge (₦)</label><input type="number" id="edit-s-delivery" value="${s.deliveryCharge || ''}" placeholder="0" oninput="calcEditSale()"></div>
            <div class="form-group"><label>Amount Paid (₦)</label><input type="number" id="edit-s-paid" value="${s.amountPaidAtSale || ''}" placeholder="0" oninput="calcEditSale()"></div>
        </div>
        
        <div class="calc-box">
            <div class="line"><span>Total Amount</span> <span>₦<span id="edit-s-total">0</span></span></div>
            <div class="line" style="color:var(--danger);"><span>Balance Owing</span> <span>₦<span id="edit-s-balance">0</span></span></div>
        </div>
        
        <button class="btn" style="margin-top:0; margin-bottom:10px;" onclick="saveEditedSale('${s.id}')">Save Changes</button>
        <button class="btn btn-outline" onclick="openSaleDetails('${s.id}')">Cancel</button>
    `;
    calcEditSale();
}

function calcEditSale() {
    const bQty = parseFloat(document.getElementById('edit-s-qty')?.value) || 0;
    const bPrice = parseFloat(document.getElementById('edit-s-price')?.value) || 0;
    const cQty = parseFloat(document.getElementById('edit-s-cement-qty')?.value) || 0;
    const cPrice = parseFloat(document.getElementById('edit-s-cement-price')?.value) || 0;
    const sQty = parseFloat(document.getElementById('edit-s-sand-qty')?.value) || 0;
    const sPrice = parseFloat(document.getElementById('edit-s-sand-price')?.value) || 0;
    const eQty = parseFloat(document.getElementById('edit-s-empty-bag-qty')?.value) || 0;
    const ePrice = parseFloat(document.getElementById('edit-s-empty-bag-price')?.value) || 0;
    const delivery = parseFloat(document.getElementById('edit-s-delivery')?.value) || 0;
    const paid = parseFloat(document.getElementById('edit-s-paid')?.value) || 0;
    
    const total = (bQty * bPrice) + (cQty * cPrice) + (sQty * sPrice) + (eQty * ePrice) + delivery;
    const balance = total - paid;
    
    const td = document.getElementById('edit-s-total');
    if(td) td.textContent = total.toLocaleString();
    const bd = document.getElementById('edit-s-balance');
    if(bd) bd.textContent = balance.toLocaleString();
}

function saveEditedSale(saleId) {
    const s = sales.find(x => x.id === saleId);
    s.customerName = document.getElementById('edit-s-customer')?.value || 'Walk-in';
    s.date = document.getElementById('edit-s-date')?.value;
    s.customerPhone = document.getElementById('edit-s-phone')?.value;
    s.size = document.getElementById('edit-s-size')?.value;
    
    s.quantity = parseInt(document.getElementById('edit-s-qty')?.value) || 0;
    s.pricePerBlock = parseInt(document.getElementById('edit-s-price')?.value) || 0;
    s.cementQty = parseInt(document.getElementById('edit-s-cement-qty')?.value) || 0;
    s.cementPrice = parseFloat(document.getElementById('edit-s-cement-price')?.value) || 0;
    s.sandQty = parseInt(document.getElementById('edit-s-sand-qty')?.value) || 0;
    s.sandPrice = parseFloat(document.getElementById('edit-s-sand-price')?.value) || 0;
    s.emptyBagQty = parseInt(document.getElementById('edit-s-empty-bag-qty')?.value) || 0;
    s.emptyBagPrice = parseFloat(document.getElementById('edit-s-empty-bag-price')?.value) || 0;
    
    s.deliveryCharge = parseInt(document.getElementById('edit-s-delivery')?.value) || 0;
    s.amountPaidAtSale = parseInt(document.getElementById('edit-s-paid')?.value) || 0;
    
    s.totalAmount = (s.quantity * s.pricePerBlock) + (s.cementQty * s.cementPrice) + (s.sandQty * s.sandPrice) + (s.emptyBagQty * s.emptyBagPrice) + s.deliveryCharge;
    s.balanceOwing = s.totalAmount - s.amountPaidAtSale;
    
    saveData('sales', sales); closeModal(); nav('sales'); showToast('Sale updated successfully', 'success');
}

function toggleDelivery(id) {
    const s = sales.find(x => x.id === id);
    if (!s) return;
    s.deliveryStatus = s.deliveryStatus === 'delivered' ? 'pending' : 'delivered';
    saveData('sales', sales); openSaleDetails(id); showToast('Delivery status updated', 'success');
}
function deleteSale(id) {
    showDialog("Delete Sale?", "Are you sure? This will remove the sale and return the blocks to your inventory.", () => {
        sales = sales.filter(s => s.id !== id); saveData('sales', sales); closeModal(); nav('sales'); showToast('Sale deleted', 'success');
    });
}
function openReturn() {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `
        <h3>${t.logReturn || 'Log Return'}</h3>
        <div class="form-group"><label>${t.customer}</label><input type="text" id="r-customer" placeholder="Name"></div>
        <div class="row"><div class="form-group"><label>${t.date}</label><input type="date" id="r-date" value="${getTodayStr()}"></div><div class="form-group"><label>${t.size}</label><select id="r-size"><option value="6">6"</option></select></div></div>
        <div class="row"><div class="form-group"><label>${t.qtyReturned || 'Qty Returned'}</label><input type="number" id="r-qty" value="" min="1" placeholder="1"></div><div class="form-group"><label>${t.refundAmt || 'Refund Amount (₦)'}</label><input type="number" id="r-refund" value="" placeholder="0"></div></div>
        <div class="form-group"><label>${t.reason || 'Reason'}</label><input type="text" id="r-reason" placeholder="e.g. Broken"></div>
        <button class="btn" onclick="saveReturn()">Save Return</button>
        <button class="btn btn-outline" onclick="closeModal()">Cancel</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function saveReturn() {
    const qty = parseInt(document.getElementById('r-qty').value) || 0;
    if (qty <= 0) return showToast('Enter valid quantity', 'err');
    returns.push({ id: Date.now().toString(), date: document.getElementById('r-date').value, customerName: document.getElementById('r-customer').value || 'Walk-in', size: document.getElementById('r-size').value, quantity: qty, refundAmount: parseFloat(document.getElementById('r-refund').value) || 0, reason: document.getElementById('r-reason').value || 'Unknown' });
    saveData('returns', returns); closeModal(); nav('sales'); showToast('Return logged', 'success');
}
function buildWhatsAppReceipt(sale) {
    let itemsText = "";
    if (sale.quantity > 0) itemsText += `- ${sale.quantity} pcs of ${sale.size}" Blocks @ ₦${sale.pricePerBlock.toLocaleString()}\n`;
    if (sale.cementQty > 0) itemsText += `- ${sale.cementQty} bags of Cement @ ₦${sale.cementPrice.toLocaleString()}\n`;
    if (sale.sandQty > 0) itemsText += `- ${sale.sandQty} bags of Sand @ ₦${sale.sandPrice.toLocaleString()}\n`;
    if (sale.emptyBagQty > 0) itemsText += `- ${sale.emptyBagQty} Empty Bags @ ₦${sale.emptyBagPrice.toLocaleString()}\n`;
    if (sale.deliveryCharge > 0) itemsText += `- Delivery Charge: ₦${sale.deliveryCharge.toLocaleString()}\n`;

    const text = "*🧱 " + settings.businessName.toUpperCase() + "*\n" +
        "📞 " + (settings.businessPhone || 'N/A') + "\n" +
        "--------------------------------\n" +
        "*INVOICE / RECEIPT*\n" +
        "Invoice No: " + (sale.invoiceNo || 'N/A') + "\n" +
        "Date: " + sale.date + " " + (sale.createdAt ? new Date(sale.createdAt).toLocaleTimeString() : '') + "\n" +
        "Customer: " + sale.customerName + "\n" +
        "--------------------------------\n" +
        "*ITEMS BOUGHT:*\n" + itemsText + "\n" +
        "*Total Amount: ₦" + sale.totalAmount.toLocaleString() + "*\n" +
        "Amount Paid: ₦" + sale.amountPaidAtSale.toLocaleString() + "\n" +
        "*Outstanding Balance: ₦" + sale.balanceOwing.toLocaleString() + "*\n" +
        "--------------------------------\n" +
        "Thank you for your patronage! 🙏";
    return encodeURIComponent(text);
}

function shareReceiptImage(saleId) {
    try {
        const s = sales.find(x => x.id === saleId);
        if (!s) return showToast('Sale not found', 'err');

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const width = 600, height = 900;
        canvas.width = width; canvas.height = height;

        // Background
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, width, height);

        // Header
        ctx.fillStyle = '#059669'; ctx.fillRect(0, 0, width, 120);
        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 32px Arial'; ctx.textAlign = 'center';
        ctx.fillText((settings.businessName || 'MY BUSINESS').toUpperCase(), width / 2, 50);
        ctx.font = '18px Arial'; ctx.fillText('📞 ' + (settings.businessPhone || ''), width / 2, 85);

        // Invoice Info
        ctx.fillStyle = '#0f172a'; ctx.textAlign = 'left'; ctx.font = 'bold 24px Arial';
        ctx.fillText('INVOICE / RECEIPT', 40, 170);

        ctx.font = '16px Arial'; ctx.fillStyle = '#64748b';
        ctx.fillText('Invoice No:', 40, 210); ctx.fillText('Date:', 40, 240); ctx.fillText('Customer:', 40, 270);

        ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial';
        ctx.fillText(s.invoiceNo || 'N/A', 160, 210);
        ctx.fillText(s.date + ' ' + (s.createdAt ? new Date(s.createdAt).toLocaleTimeString() : ''), 160, 240);
        ctx.fillText(s.customerName, 160, 270);

        // Divider
        ctx.beginPath(); ctx.moveTo(40, 300); ctx.lineTo(560, 300); ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 2; ctx.stroke();

        // Table Headers
        ctx.fillStyle = '#64748b'; ctx.font = 'bold 16px Arial'; ctx.textAlign = 'left';
        ctx.fillText('Item Description', 40, 340);
        ctx.textAlign = 'right'; ctx.fillText('Subtotal', 560, 340);

        let yPos = 380;
        let hasItems = false;

        const drawLineItem = (title, qty, price) => {
            if (qty > 0) {
                hasItems = true;
                ctx.textAlign = 'left'; ctx.fillStyle = '#0f172a'; ctx.font = '16px Arial';
                ctx.fillText(`${title} (${qty} @ ₦${price.toLocaleString()})`, 40, yPos);
                ctx.textAlign = 'right'; ctx.font = 'bold 16px Arial';
                ctx.fillText(`₦${(qty * price).toLocaleString()}`, 560, yPos);
                yPos += 30;
            }
        };

        drawLineItem(`${s.size}" Blocks`, s.quantity, s.pricePerBlock);
        drawLineItem(`Cement Bags`, s.cementQty, s.cementPrice);
        drawLineItem(`Sand Bags`, s.sandQty, s.sandPrice);
        drawLineItem(`Empty Bags`, s.emptyBagQty, s.emptyBagPrice);

        if (s.deliveryCharge > 0) {
            hasItems = true;
            ctx.textAlign = 'left'; ctx.fillStyle = '#64748b'; ctx.font = '16px Arial';
            ctx.fillText(`Delivery Charge`, 40, yPos);
            ctx.textAlign = 'right'; ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial';
            ctx.fillText(`₦${s.deliveryCharge.toLocaleString()}`, 560, yPos);
            yPos += 30;
        }

        if (!hasItems) {
            ctx.textAlign = 'left'; ctx.fillStyle = '#64748b'; ctx.font = 'italic 16px Arial';
            ctx.fillText('No items logged.', 40, yPos);
            yPos += 30;
        }

        // Divider
        yPos += 10;
        ctx.beginPath(); ctx.moveTo(40, yPos); ctx.lineTo(560, yPos); ctx.stroke();

        // Totals
        yPos += 40;
        ctx.textAlign = 'left'; ctx.font = 'bold 20px Arial'; ctx.fillText('Total Amount:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = '#059669'; ctx.fillText(`₦${s.totalAmount.toLocaleString()}`, 560, yPos);

        yPos += 40;
        ctx.fillStyle = '#64748b'; ctx.font = '16px Arial'; ctx.textAlign = 'left'; ctx.fillText('Amount Paid:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = '#0f172a'; ctx.font = 'bold 16px Arial'; ctx.fillText(`₦${s.amountPaidAtSale.toLocaleString()}`, 560, yPos);

        yPos += 40;
        ctx.fillStyle = '#64748b'; ctx.textAlign = 'left'; ctx.font = '16px Arial'; ctx.fillText('Outstanding Balance:', 40, yPos);
        ctx.textAlign = 'right'; ctx.fillStyle = s.balanceOwing > 0 ? '#dc2626' : '#059669'; ctx.font = 'bold 18px Arial'; ctx.fillText(`₦${s.balanceOwing.toLocaleString()}`, 560, yPos);

        // Footer
        ctx.fillStyle = '#64748b'; ctx.font = 'italic 16px Arial'; ctx.textAlign = 'center';
        ctx.fillText('Thank you for your business!', width / 2, height - 80);
        ctx.font = '14px Arial';
        ctx.fillText('Powered by Asad Tech Concepts', width / 2, height - 50);

        canvas.toBlob(function(blob) {
            try {
                const file = new File([blob], 'Receipt_' + (s.invoiceNo || s.id) + '.png', { type: 'image/png' });
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    navigator.share({ files: [file], title: 'Receipt' }).catch(e => console.log(e));
                } else {
                    const url = URL.createObjectURL(blob); const a = document.createElement('a');
                    a.href = url; a.download = 'Receipt_' + (s.invoiceNo || s.id) + '.png'; a.click();
                    URL.revokeObjectURL(url); showToast('Receipt image downloaded', 'success');
                }
            } catch(err) { showToast('Image download error', 'err'); }
        }, 'image/png');
    } catch (e) { showToast("Canvas Error: " + e.message, "err"); }
}

function renderProduction(main) { 
    const t = i18n[settings.lang]; const today = getTodayStr();
    const uniqueWorkers = [...new Set(batches.map(b => b.worker).filter(w => w && w !== 'Unknown' && w !== 'System Adjustment'))];
    let listHtml = ''; const recent = [...batches].reverse().slice(0, 15);
    recent.forEach(b => {
        const isCuring = b.status === 'curing';
        listHtml += `<div class="list-item ${isCuring ? 'curing' : ''}" style="cursor:pointer;" onclick="openBatchDetails('${b.id}')"><div class="list-header"><span>${b.size}" Blocks · ${b.blocksProduced} pcs</span><span class="pos">${formatNaira(b.costPerBlock)}<small style="color:var(--muted); font-weight:600;">/block</small></span></div><div class="list-sub">${b.worker} · ${b.date}</div><span class="tag ${isCuring ? 'blue' : 'green'}">${isCuring ? t.curing : t.ready}</span>${isCuring ? `<div class="actions"><button onclick="markReady('${b.id}')">${t.markReady}</button></div>` : ''}</div>`;
    });
    main.innerHTML = `
        <div class="card">
            <h3>${ico('production')} ${t.newBatch}</h3>
            <div class="row"><div class="form-group"><label>Date</label><input type="date" id="p-date" value="${today}"></div><div class="form-group"><label>${t.size}</label><select id="p-size"><option value="6">6"</option></select></div></div>
            <div class="row"><div class="form-group"><label>${t.worker}</label><input type="text" id="p-worker" list="worker-names" placeholder="Worker name"><datalist id="worker-names"></datalist></div><div class="form-group"><label>${t.blocksProduced}</label><input type="number" id="p-blocks" value="" placeholder="0" oninput="calcBatchCost()"><div style="display:flex; gap:6px; margin-top:6px;"><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 100, 'calcBatchCost')">+100</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 500, 'calcBatchCost')">+500</button><button type="button" class="btn btn-outline" style="padding:6px; font-size:12px; margin:0;" onclick="quickAdd('p-blocks', 1000, 'calcBatchCost')">+1000</button><button type="button" class="btn" style="padding:6px; font-size:12px; margin:0; background:var(--accent); color:#fff; border:none;" onclick="autoFillMaterials()">⚡ Auto-Fill Mix</button></div></div></div>
            <div class="eyebrow">Materials Used</div>
            <div class="row"><div class="form-group"><label>${t.cementBags}</label><input type="number" id="p-cement-bags" value="" placeholder="0" oninput="calcBatchCost()"></div><div class="form-group"><label>${t.costPerBag}</label><input type="number" id="p-cement-cost" value="" placeholder="0" oninput="calcBatchCost()"></div></div>
            <div class="row"><div class="form-group"><label>${t.sandCost}</label><input type="number" id="p-sand-cost" value="" placeholder="0" oninput="calcBatchCost()"></div><div class="form-group"><label>${t.sandQty}</label><input type="number" id="p-sand-qty" value="" placeholder="0"></div></div>
            <div class="row"><div class="form-group"><label>${t.labourCost}</label><input type="number" id="p-labour-cost" value="" placeholder="0" oninput="calcBatchCost()"></div><div class="form-group"><label>${t.otherCost}</label><input type="number" id="p-other-cost" value="" placeholder="0" oninput="calcBatchCost()"></div></div>
            <div class="form-group"><label>${t.breakages}</label><input type="number" id="p-breakages" value="" placeholder="0"></div>
            <div class="form-group"><label>${t.curingLoss}</label><input type="number" id="p-curing-loss" value="" placeholder="0"></div>
            <div class="calc-box"><div class="line"><span>${t.totalCost}</span> <span>₦<span id="p-total-display">0</span></span></div><div class="line pos"><span>${t.costPerBlock}</span> <span>₦<span id="p-cpb-display">0.00</span></span></div></div>
            <button class="btn btn-blue" style="margin-top:0;" onclick="saveBatch()">${t.saveBatch}</button>
        </div>
        <div class="section-title">${ico('bars')} Recent Batches</div>${listHtml || '<div class="empty">No batches logged yet.</div>'}`;
    document.getElementById('worker-names').innerHTML = uniqueWorkers.map(w => `<option value="${w}"></option>`).join('');
}
function autoFillMaterials() {
    const blocks = parseInt(document.getElementById('p-blocks').value) || 0;
    if(blocks <= 0) return showToast('Enter blocks produced first', 'err');
    document.getElementById('p-cement-bags').value = Math.ceil(blocks / (settings.mixCement || 50));
    document.getElementById('p-sand-qty').value = Math.ceil(blocks / (settings.mixSand || 500));
    calcBatchCost(); showToast('Quantities auto-filled based on mix', 'success');
}
function calcBatchCost() {
    const cb = (parseFloat(document.getElementById('p-cement-bags').value) || 0) * (parseFloat(document.getElementById('p-cement-cost').value) || 0);
    const sc = parseFloat(document.getElementById('p-sand-cost').value) || 0;
    const lc = parseFloat(document.getElementById('p-labour-cost').value) || 0;
    const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
    const total = cb + sc + lc + oc;
    const blocks = parseFloat(document.getElementById('p-blocks').value) || 0;
    const cpb = blocks > 0 ? (total / blocks) : 0;
    document.getElementById('p-total-display').textContent = total.toLocaleString();
    document.getElementById('p-cpb-display').textContent = cpb.toFixed(2);
}
function saveBatch() {
    const blocks = parseInt(document.getElementById('p-blocks').value) || 0;
    if (blocks <= 0) return showToast('Enter valid number of blocks', 'err');
    const cb = (parseFloat(document.getElementById('p-cement-bags').value) || 0) * (parseFloat(document.getElementById('p-cement-cost').value) || 0);
    const sc = parseFloat(document.getElementById('p-sand-cost').value) || 0;
    const lc = parseFloat(document.getElementById('p-labour-cost').value) || 0;
    const oc = parseFloat(document.getElementById('p-other-cost').value) || 0;
    const totalCost = cb + sc + lc + oc;
    const batch = { id: Date.now().toString(), date: document.getElementById('p-date').value, size: document.getElementById('p-size').value, worker: document.getElementById('p-worker').value || 'Unknown', blocksProduced: blocks, breakages: parseInt(document.getElementById('p-breakages').value) || 0, curingLoss: parseInt(document.getElementById('p-curing-loss').value) || 0, cementBags: parseFloat(document.getElementById('p-cement-bags').value) || 0, sandQty: parseFloat(document.getElementById('p-sand-qty').value) || 0, labourCost: lc, totalCost: totalCost, costPerBlock: totalCost / blocks, status: 'curing' };
    batches.push(batch); saveData('batches', batches); nav('production'); showToast('Production batch saved', 'success');
}
function markReady(id) { const b = batches.find(x => x.id === id); if (b) { b.status = 'ready'; saveData('batches', batches); nav('production'); showToast('Batch marked ready', 'success'); } }
function openBatchDetails(batchId) {
    const b = batches.find(x => x.id === batchId);
    if (!b) return;
    document.getElementById('modal-body').innerHTML = `
        <h3>Batch Details · ${b.size}"</h3>
        <div class="kv"><span>Date</span><strong>${b.date}</strong></div>
        <div class="kv"><span>Worker</span><strong>${b.worker}</strong></div>
        <div class="kv"><span>Produced</span><strong>${b.blocksProduced} pcs</strong></div>
        <div class="kv"><span>Breakages</span><strong class="neg">${b.breakages} pcs</strong></div>
        <div class="kv"><span>Curing Loss</span><strong class="neg">${b.curingLoss} pcs</strong></div>
        <div class="eyebrow">Financials</div>
        <div class="kv"><span>Total Cost</span><strong>${formatNaira(b.totalCost)}</strong></div>
        <div class="kv"><span>Cost per Block</span><strong class="pos">${formatNaira(b.costPerBlock)}</strong></div>
        <div class="kv"><span>Status</span><span class="tag ${b.status==='curing'?'blue':'green'}">${b.status.toUpperCase()}</span></div>
        <div class="row" style="margin-top:24px;"><button class="btn btn-outline" onclick="closeModal()">Close</button><button class="btn" onclick="editBatch('${b.id}')">Edit Batch</button></div>
        <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteBatch('${b.id}')">Delete Batch</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function editBatch(batchId) {
    const b = batches.find(x => x.id === batchId);
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Batch</h3>
        <div class="row"><div class="form-group"><label>Date</label><input type="date" id="edit-b-date" value="${b.date}"></div><div class="form-group"><label>Size</label><select id="edit-b-size"><option value="6">6"</option></select></div></div>
        <div class="row"><div class="form-group"><label>Worker</label><input type="text" id="edit-b-worker" value="${b.worker}"></div><div class="form-group"><label>Blocks Produced</label><input type="number" id="edit-b-blocks" value="${b.blocksProduced || ''}" placeholder="0" oninput="calcEditBatch()"></div></div>
        <div class="row"><div class="form-group"><label>Total Cost (₦)</label><input type="number" id="edit-b-totalcost" value="${b.totalCost || ''}" placeholder="0" oninput="calcEditBatch()"></div><div class="form-group"><label>Breakages</label><input type="number" id="edit-b-breakages" value="${b.breakages || ''}" placeholder="0"></div></div>
        <div class="form-group"><label>Curing Loss</label><input type="number" id="edit-b-curing-loss" value="${b.curingLoss || ''}" placeholder="0"></div>
        <div class="calc-box"><div class="line pos"><span>Cost per Block</span> <span>₦<span id="edit-b-cpb">0.00</span></span></div></div>
        <div class="row"><button class="btn btn-outline" onclick="openBatchDetails('${b.id}')">Back</button><button class="btn" onclick="saveEditedBatch('${b.id}')">Save Changes</button></div>
    `;
    calcEditBatch();
}
function calcEditBatch() {
    const totalCost = parseFloat(document.getElementById('edit-b-totalcost').value) || 0;
    const blocks = parseFloat(document.getElementById('edit-b-blocks').value) || 0;
    document.getElementById('edit-b-cpb').textContent = (blocks > 0 ? (totalCost / blocks) : 0).toFixed(2);
}
function saveEditedBatch(batchId) {
    const b = batches.find(x => x.id === batchId);
    b.date = document.getElementById('edit-b-date').value; b.size = document.getElementById('edit-b-size').value;
    b.worker = document.getElementById('edit-b-worker').value || 'Unknown'; b.blocksProduced = parseInt(document.getElementById('edit-b-blocks').value) || 0;
    b.breakages = parseInt(document.getElementById('edit-b-breakages').value) || 0; b.curingLoss = parseInt(document.getElementById('edit-b-curing-loss').value) || 0;
    b.totalCost = parseFloat(document.getElementById('edit-b-totalcost').value) || 0;
    b.costPerBlock = b.blocksProduced > 0 ? (b.totalCost / b.blocksProduced) : 0;
    saveData('batches', batches); closeModal(); nav('production'); showToast('Batch updated', 'success');
}
function deleteBatch(id) {
    showDialog("Delete Batch?", "Are you sure? This will remove all blocks produced in this batch.", () => {
        batches = batches.filter(b => b.id !== id); saveData('batches', batches); closeModal(); nav('production'); showToast('Batch deleted', 'success');
    });
}

function renderExpenses(main) { 
    const t = i18n[settings.lang]; const today = getTodayStr();
    let listHtml = ''; const recent = [...expenses].reverse().slice(0, 20);
    recent.forEach(e => { listHtml += `<div class="list-item neutral" style="cursor:pointer;" onclick="openExpenseDetails('${e.id}')"><div class="list-header"><span>${t[e.category] || e.category}</span><span class="neg">₦${e.amount.toLocaleString()}</span></div><div class="list-sub">${e.date}${e.note ? ' · ' + e.note : ''}</div></div>`; });
    main.innerHTML = `
        <div class="card">
            <h3>${ico('expenses')} ${t.newExpense}</h3>
            <div class="row"><div class="form-group"><label>Date</label><input type="date" id="e-date" value="${today}"></div><div class="form-group"><label>${t.category}</label><select id="e-category">${['wages','repairs','generator_fuel','rent','transport','loaders','phone_data','other',...settings.customExpenses].map(c=>`<option value="${c}">${t[c]||c}</option>`).join('')}</select></div></div>
            <div class="form-group"><label>${t.amount}</label><input type="number" id="e-amount" value="" placeholder="0"></div>
            <div class="form-group"><label>${t.note}</label><input type="text" id="e-note" placeholder="Optional"></div>
            <button class="btn" style="margin-top:0;" onclick="saveExpense()">${t.saveExpense}</button>
        </div>
        <div class="section-title">${ico('bars')} Recent Expenses</div>${listHtml || '<div class="empty">No expenses logged yet.</div>'}`;
}
function saveExpense() {
    const amount = parseInt(document.getElementById('e-amount').value) || 0;
    if (amount <= 0) return showToast('Enter valid amount', 'err');
    const exp = { id: Date.now().toString(), date: document.getElementById('e-date').value, category: document.getElementById('e-category').value, amount: amount, note: document.getElementById('e-note').value };
    expenses.push(exp); saveData('expenses', expenses); nav('expenses'); showToast('Expense logged', 'success');
}
function openExpenseDetails(id) {
    const e = expenses.find(x => x.id === id);
    if (!e) return;
    document.getElementById('modal-body').innerHTML = `
        <h3>Expense Details</h3>
        <div class="kv"><span>Date</span><strong>${e.date}</strong></div>
        <div class="kv"><span>Category</span><strong style="text-transform:capitalize;">${e.category}</strong></div>
        <div class="kv"><span>Amount</span><strong class="neg">${formatNaira(e.amount)}</strong></div>
        <div class="kv"><span>Note</span><strong>${e.note || 'N/A'}</strong></div>
        <div class="row" style="margin-top:24px;"><button class="btn btn-outline" onclick="closeModal()">Close</button><button class="btn" onclick="editExpense('${e.id}')">Edit</button></div>
        <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteExpense('${e.id}')">Delete Expense</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function editExpense(id) {
    const e = expenses.find(x => x.id === id); const t = i18n[settings.lang];
    const cats = ['wages', 'repairs', 'generator_fuel', 'rent', 'transport', 'loaders', 'phone_data', 'other', ...settings.customExpenses];
    document.getElementById('modal-body').innerHTML = `
        <h3>Edit Expense</h3>
        <div class="row"><div class="form-group"><label>Date</label><input type="date" id="edit-e-date" value="${e.date}"></div><div class="form-group"><label>Category</label><select id="edit-e-category">${cats.map(c => `<option value="${c}" ${e.category === c ? 'selected' : ''}>${t[c] || c}</option>`).join('')}</select></div></div>
        <div class="form-group"><label>Amount (₦)</label><input type="number" id="edit-e-amount" value="${e.amount || ''}" placeholder="0"></div>
        <div class="form-group"><label>Note</label><input type="text" id="edit-e-note" value="${e.note || ''}"></div>
        <div class="row"><button class="btn btn-outline" onclick="openExpenseDetails('${e.id}')">Back</button><button class="btn" onclick="saveEditedExpense('${e.id}')">Save Changes</button></div>
    `;
}
function saveEditedExpense(id) {
    const e = expenses.find(x => x.id === id);
    e.date = document.getElementById('edit-e-date').value; e.category = document.getElementById('edit-e-category').value;
    e.amount = parseFloat(document.getElementById('edit-e-amount').value) || 0; e.note = document.getElementById('edit-e-note').value;
    saveData('expenses', expenses); closeModal(); nav('expenses'); showToast('Expense updated', 'success');
}
function deleteExpense(id) {
    showDialog("Delete Expense?", "Are you sure you want to remove this expense?", () => {
        expenses = expenses.filter(e => e.id !== id); saveData('expenses', expenses); closeModal(); nav('expenses'); showToast('Expense deleted', 'success');
    });
}

function renderDebts(main) {
    const t = i18n[settings.lang]; 
    const owingSales = sales.filter(s => s.balanceOwing > 0 && !s.writtenOff);
    const owingPurchases = purchases.filter(p => p.cost > (p.amountPaid || 0));
    let html = `<div class="segmented"><button class="${currentDebtTab === 'customer' ? 'on' : ''}" onclick="setDebtTab('customer')">${t.customerDebts}</button><button class="${currentDebtTab === 'supplier' ? 'on' : ''}" onclick="setDebtTab('supplier')">${t.supplierDebts}</button></div><div class="form-group" style="margin-bottom:12px;"><input type="text" id="search-debts" placeholder="Search name..." oninput="filterDebts(this.value)" style="padding:10px 14px; font-size:14px; border-radius:20px;"></div><div id="debts-list">`;
    if (currentDebtTab === 'customer') {
        if (owingSales.length > 0) { html += `<button class="btn btn-dark" style="margin-bottom: 16px;" onclick="generateBulkReminder()">📢 Generate Bulk Reminder List</button>`; }
        if (owingSales.length === 0) { html += `<div class="empty">No outstanding customer debts.</div>`; } else {
            owingSales.forEach(s => {
                const days = Math.floor((new Date(getTodayStr()) - new Date(s.date)) / (1000 * 60 * 60 * 24));
                const waText = encodeURIComponent(`Hello ${s.customerName}, this is a reminder from ${settings.businessName}. Your outstanding balance is ₦${s.balanceOwing}. Please settle. Thank you!`);
                const waPhone = (s.customerPhone || '').replace(/^0/, '234'); const waLink = `https://wa.me/${waPhone}?text=${waText}`;
                html += `<div class="list-item owing" style="cursor:pointer;" onclick="openCustomerStatement('${s.customerName.replace(/'/g, "\\'")}')"><div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div><div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${s.size}" Blocks · ${s.quantity} pcs · ${days} ${t.daysAgo}</div><div class="actions"><button onclick="event.stopPropagation(); openPayment('${s.id}')">${t.pay}</button><a href="${waLink}" target="_blank" onclick="event.stopPropagation();"><button class="wa">${t.remind}</button></a></div></div>`;
            });
        }
    } else {
        html += `<button class="btn btn-dark" style="margin-bottom: 16px;" onclick="openPurchase()">+ ${t.logPurchase}</button>`;
        if (owingPurchases.length === 0) { html += `<div class="empty">${t.noSupplierDebts}</div>`; } else {
            owingPurchases.forEach(p => {
                const balance = p.cost - (p.amountPaid || 0);
                const days = Math.floor((new Date(getTodayStr()) - new Date(p.date)) / (1000 * 60 * 60 * 24));
                html += `<div class="list-item owing"><div class="list-header"><span>${p.supplierName || 'Unknown Supplier'}</span><span class="neg">₦${balance.toLocaleString()}</span></div><div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${p.material.toUpperCase()} · ${p.qty} units · ${days} ${t.daysAgo}</div><div class="list-sub">Total ₦${p.cost.toLocaleString()} · Paid ₦${(p.amountPaid || 0).toLocaleString()}</div><div class="actions"><button onclick="openSupplierPayment('${p.id}')" style="background:var(--accent-soft); color:#92400e; border-color:#fde68a;">${t.paySupplier}</button></div></div>`;
            });
        }
    }
    html += `</div>`; main.innerHTML = html;
}
function setDebtTab(tab) { currentDebtTab = tab; nav('debts'); }
function filterDebts(query) {
    const q = query.toLowerCase(); let html = '';
    if (currentDebtTab === 'customer') {
        const owingSales = sales.filter(s => s.balanceOwing > 0 && !s.writtenOff && s.customerName.toLowerCase().includes(q));
        if (owingSales.length === 0) { html += `<div class="empty">No outstanding customer debts found.</div>`; } else {
            owingSales.forEach(s => {
                const days = Math.floor((new Date(getTodayStr()) - new Date(s.date)) / (1000 * 60 * 60 * 24));
                const waText = encodeURIComponent(`Hello ${s.customerName}, this is a reminder from ${settings.businessName}. Your outstanding balance is ₦${s.balanceOwing}. Please settle. Thank you!`);
                const waPhone = (s.customerPhone || '').replace(/^0/, '234'); const waLink = `https://wa.me/${waPhone}?text=${waText}`;
                html += `<div class="list-item owing" style="cursor:pointer;" onclick="openCustomerStatement('${s.customerName.replace(/'/g, "\\'")}')"><div class="list-header"><span>${s.customerName}</span><span class="neg">₦${s.balanceOwing.toLocaleString()}</span></div><div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${s.size}" Blocks · ${s.quantity} pcs · ${days} ${i18n[settings.lang].daysAgo}</div><div class="actions"><button onclick="event.stopPropagation(); openPayment('${s.id}')">${i18n[settings.lang].pay}</button><a href="${waLink}" target="_blank" onclick="event.stopPropagation();"><button class="wa">${i18n[settings.lang].remind}</button></a></div></div>`;
            });
        }
    } else {
        const owingPurchases = purchases.filter(p => p.cost > (p.amountPaid || 0) && p.supplierName.toLowerCase().includes(q));
        if (owingPurchases.length === 0) { html += `<div class="empty">No outstanding supplier debts found.</div>`; } else {
            owingPurchases.forEach(p => {
                const balance = p.cost - (p.amountPaid || 0);
                const days = Math.floor((new Date(getTodayStr()) - new Date(p.date)) / (1000 * 60 * 60 * 24));
                html += `<div class="list-item owing"><div class="list-header"><span>${p.supplierName || 'Unknown Supplier'}</span><span class="neg">₦${balance.toLocaleString()}</span></div><div class="list-sub" style="color:${days > 30 ? 'var(--danger)' : 'var(--muted)'}; font-weight:${days > 30 ? '700' : '400'};">${p.material.toUpperCase()} · ${p.qty} units · ${days} ${i18n[settings.lang].daysAgo}</div><div class="list-sub">Total ₦${p.cost.toLocaleString()} · Paid ₦${(p.amountPaid || 0).toLocaleString()}</div><div class="actions"><button onclick="openSupplierPayment('${p.id}')" style="background:var(--accent-soft); color:#92400e; border-color:#fde68a;">${i18n[settings.lang].paySupplier}</button></div></div>`;
            });
        }
    }
    document.getElementById('debts-list').innerHTML = html;
}
function openPayment(saleId) {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `<h3>${t.pay}</h3><div class="form-group"><label>${t.amount}</label><input type="number" id="pay-amount" value="" placeholder="0"></div><button class="btn" onclick="recordPayment('${saleId}')">Save</button><button class="btn btn-outline" onclick="closeModal()">Cancel</button>`;
    document.getElementById('modal').classList.add('active');
}
function recordPayment(saleId) {
    const amount = parseInt(document.getElementById('pay-amount').value) || 0;
    if (amount <= 0) return showToast('Enter valid amount', 'err');
    const sale = sales.find(s => s.id === saleId); if (!sale) return;
    sale.balanceOwing -= amount; if (sale.balanceOwing < 0) sale.balanceOwing = 0;
    payments.push({ id: Date.now().toString(), saleId: saleId, amount: amount, date: getTodayStr() });
    saveData('sales', sales); saveData('customerPayments', payments); closeModal(); nav('debts'); showToast('Payment recorded', 'success');
}
function openSupplierPayment(purchaseId) {
    const t = i18n[settings.lang];
    document.getElementById('modal-body').innerHTML = `<h3>${t.paySupplier}</h3><div class="form-group"><label>${t.amount}</label><input type="number" id="pay-supp-amount" value="" placeholder="0"></div><button class="btn" onclick="recordSupplierPayment('${purchaseId}')">Save</button><button class="btn btn-outline" onclick="closeModal()">Cancel</button>`;
    document.getElementById('modal').classList.add('active');
}
function recordSupplierPayment(purchaseId) {
    const amount = parseInt(document.getElementById('pay-supp-amount').value) || 0;
    if (amount <= 0) return showToast('Enter valid amount', 'err');
    const pur = purchases.find(p => p.id === purchaseId); if (!pur) return;
    pur.amountPaid = (pur.amountPaid || 0) + amount; if (pur.amountPaid > pur.cost) pur.amountPaid = pur.cost;
    saveData('purchases', purchases); closeModal(); nav('debts'); showToast('Supplier payment recorded', 'success');
}
function openCustomerStatement(custName) {
    const custSales = sales.filter(s => s.customerName === custName);
    const saleIds = custSales.map(s => s.id);
    const custPayments = payments.filter(p => saleIds.includes(p.saleId));
    const totalBought = custSales.reduce((sum, s) => sum + s.totalAmount, 0);
    const totalPaidAtSale = custSales.reduce((sum, s) => sum + s.amountPaidAtSale, 0);
    const totalExtraPayments = custPayments.reduce((sum, p) => sum + p.amount, 0);
    const totalPaid = totalPaidAtSale + totalExtraPayments;
    const totalOwing = custSales.reduce((sum, s) => sum + s.balanceOwing, 0);
    const phone = custSales.find(s => s.customerPhone)?.customerPhone || '';
    let history = [];
    custSales.forEach(s => {
        history.push({ date: s.date, type: 'sale', desc: `${s.size}" Blocks × ${s.quantity}`, amt: s.totalAmount, color: 'var(--text)' });
        if (s.amountPaidAtSale > 0) history.push({ date: s.date, type: 'payment', desc: `Paid at sale`, amt: s.amountPaidAtSale, color: 'var(--brand)' });
    });
    custPayments.forEach(p => { history.push({ date: p.date, type: 'payment', desc: `Payment received`, amt: p.amount, color: 'var(--brand)' }); });
    history.sort((a, b) => new Date(a.date) - new Date(b.date));
    let historyHtml = history.map(h => `<div class="kv" style="font-size:13px;"><span>${h.date} · ${h.desc}</span><strong style="color:${h.color};">${h.type === 'sale' ? '+' : '-'}${formatNaira(h.amt)}</strong></div>`).join('');
    document.getElementById('modal-body').innerHTML = `
        <h3>${custName}</h3><p style="font-size:13px; color:var(--muted); margin-top:-10px; margin-bottom:16px;">📞 ${phone || 'No phone saved'}</p>
        <div class="calc-box" style="background:#f8fafc; border-color:var(--line);"><div class="line" style="color:var(--text);"><span>Total Purchases</span> <span>${formatNaira(totalBought)}</span></div><div class="line" style="color:var(--brand);"><span>Total Paid</span> <span>${formatNaira(totalPaid)}</span></div><div class="line" style="color:var(--danger); font-size:16px; border-top:1px solid var(--line); padding-top:6px; margin-top:6px;"><span>Outstanding</span> <span>${formatNaira(totalOwing)}</span></div></div>
        <div class="eyebrow">Transaction History</div>
        <div style="max-height:200px; overflow-y:auto; margin-bottom:16px; border:1px solid var(--line); border-radius:8px; padding:0 12px;">${historyHtml || '<p style="font-size:13px; color:var(--muted); padding:12px 0;">No transactions yet.</p>'}</div>
        <div class="row" style="margin-top:24px;"><button class="btn btn-outline" onclick="closeModal()">Close</button><button class="btn" style="background:#25D366; color:#fff;" onclick="shareStatement('${custName.replace(/'/g, "\\'")}', '${phone.replace(/'/g, "\\'")}', ${totalBought}, ${totalPaid}, ${totalOwing})">Send Statement</button></div>
    `;
    document.getElementById('modal').classList.add('active');
}
function shareStatement(custName, phone, bought, paid, owing) {
    const waPhone = phone.replace(/^0/, '234');
    const msg = encodeURIComponent(`*🧱 ${settings.businessName.toUpperCase()}*\n📞 ${settings.businessPhone || 'N/A'}\n--------------------------------\n*STATEMENT OF ACCOUNT*\nCustomer: ${custName}\nDate: ${getTodayStr()}\n--------------------------------\n*Total Purchases:* ₦${bought.toLocaleString()}\n*Total Paid:* ₦${paid.toLocaleString()}\n--------------------------------\n*OUTSTANDING BALANCE: ₦${owing.toLocaleString()}*\n--------------------------------\nPlease kindly settle your outstanding balance.\nThank you for your patronage! 🙏`);
    if (waPhone && waPhone.length > 5) window.open(`https://wa.me/${waPhone}?text=${msg}`, '_blank');
    else navigator.clipboard.writeText(msg).then(() => showToast('No phone saved. Copied to clipboard!', 'success'));
}
function generateBulkReminder() {
    const owingSales = sales.filter(s => s.balanceOwing > 0 && !s.writtenOff);
    if (owingSales.length === 0) return showToast('No outstanding debts to remind.', 'err');
    const debtors = {};
    owingSales.forEach(s => { debtors[s.customerName] = (debtors[s.customerName] || 0) + s.balanceOwing; });
    let msg = `*🧱 ${settings.businessName.toUpperCase()}*\n📞 ${settings.businessPhone || 'N/A'}\n--------------------------------\n*DEBT REMINDER LIST*\nDate: ${getTodayStr()}\n--------------------------------\n`;
    let total = 0;
    Object.keys(debtors).sort((a,b) => debtors[b] - debtors[a]).forEach(name => { msg += `- ${name}: ₦${debtors[name].toLocaleString()}\n`; total += debtors[name]; });
    msg += `--------------------------------\n*Total Outstanding: ₦${total.toLocaleString()}*\n\nPlease kindly settle your outstanding balances. Thank you! 🙏`;
    document.getElementById('modal-body').innerHTML = `
        <h3>Bulk Reminder</h3><p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Copy this list to send in a WhatsApp group, or share it directly.</p>
        <textarea id="bulk-reminder-text" style="width:100%; height:220px; font-family:monospace; font-size:13px; padding:12px; border-radius:8px; border:1.5px solid var(--line); margin-bottom:16px; background:#f8fafc;" readonly>${msg}</textarea>
        <div class="row"><button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('bulk-reminder-text').value).then(()=>showToast('Copied!','success'))">📋 Copy</button><button class="btn" style="background:#25D366; color:#fff;" onclick="shareBulkReminder()">📤 Share</button></div>
        <button class="btn btn-outline" style="margin-top:8px;" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function shareBulkReminder() {
    const text = document.getElementById('bulk-reminder-text').value;
    if (navigator.share) navigator.share({ title: 'Debt Reminders', text: text }).then(() => showToast('Shared', 'success')).catch(e => console.log(e));
    else navigator.clipboard.writeText(text).then(() => showToast('Copied!', 'success'));
}
function writeOffDebt(saleId) {
    showDialog("Write Off Debt?", "Are you sure? This will clear the debt from your dashboard. This action cannot be undone.", () => {
        const sale = sales.find(s => s.id === saleId);
        if (sale) { sale.writtenOff = true; sale.balanceOwing = 0; saveData('sales', sales); closeModal(); nav('debts'); showToast('Debt written off', 'success'); }
    });
}

function openDailyClosing() {
    const todayStr = getTodayStr();
    const dayName = getWATDate().toLocaleDateString('en-US', {weekday:'long', year:'numeric', month:'long', day:'numeric'});
    const todaySales = sales.filter(s => s.date === todayStr);
    const todayBatches = batches.filter(b => b.date === todayStr);
    const todayExps = expenses.filter(e => e.date === todayStr);
    const todayPayments = payments.filter(p => p.date === todayStr);
    const totalProduced = todayBatches.reduce((sum, b) => sum + b.blocksProduced, 0);
    const totalSalesAmt = todaySales.reduce((sum, s) => sum + s.totalAmount, 0);
    const cashFromSales = todaySales.reduce((sum, s) => sum + s.amountPaidAtSale, 0);
    const cashFromPayments = todayPayments.reduce((sum, p) => sum + p.amount, 0);
    const totalExp = todayExps.reduce((sum, e) => sum + e.amount, 0);
    const netCash = cashFromSales + cashFromPayments - totalExp;
    let report = `*📊 DAILY CLOSING REPORT*\n*${settings.businessName.toUpperCase()}*\nDate: ${dayName}\n--------------------------------\n*PRODUCTION*\nTotal Blocks Produced: ${totalProduced} pcs\n--------------------------------\n*SALES*\nTotal Sales Value: ₦${totalSalesAmt.toLocaleString()}\nCash Collected Today: ₦${(cashFromSales + cashFromPayments).toLocaleString()}\n--------------------------------\n*EXPENSES*\nTotal Expenses: ₦${totalExp.toLocaleString()}\n--------------------------------\n*NET CASH IN HAND TODAY*\n₦${netCash.toLocaleString()}\n--------------------------------\nEnd of day summary.`;
    document.getElementById('modal-body').innerHTML = `
        <h3>Daily Closing Report</h3><p style="font-size:13px; color:var(--muted); margin-bottom:12px;">Share this with the owner or keep it for your records.</p>
        <textarea id="closing-report-text" style="width:100%; height:220px; font-family:monospace; font-size:13px; padding:12px; border-radius:8px; border:1.5px solid var(--line); margin-bottom:16px; background:#f8fafc;" readonly>${report}</textarea>
        <div class="row"><button class="btn btn-outline" onclick="navigator.clipboard.writeText(document.getElementById('closing-report-text').value).then(()=>showToast('Copied!','success'))">📋 Copy</button><button class="btn" style="background:#25D366; color:#fff;" onclick="shareClosingReport()">📤 Share</button></div>
        <button class="btn btn-outline" style="margin-top:8px;" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function shareClosingReport() {
    const text = document.getElementById('closing-report-text').value;
    if (navigator.share) navigator.share({ title: 'Daily Closing Report', text: text }).then(() => showToast('Shared', 'success')).catch(e => console.log(e));
    else navigator.clipboard.writeText(text).then(() => showToast('Copied!', 'success'));
}

function openDirectory() {
    const uniqueCustomers = {};
    sales.forEach(s => { if(s.customerName && s.customerName !== 'Walk-in') uniqueCustomers[s.customerName] = s.customerPhone; });
    const uniqueSuppliers = [...new Set(purchases.map(p => p.supplierName).filter(n => n && n !== 'Unknown'))];
    let custHtml = Object.keys(uniqueCustomers).map(c => {
        const limit = settings.creditLimits[c] || 0;
        const limitText = limit > 0 ? `Limit: ${formatNaira(limit)}` : 'No Limit';
        const totalOwed = sales.filter(s => s.customerName === c && !s.writtenOff).reduce((sum, s) => sum + s.balanceOwing, 0);
        return `<div class="list-item neutral" style="padding:12px; margin-bottom:8px;"><div class="list-header"><span>${c}</span> <span style="font-size:12px; color:var(--muted);">${uniqueCustomers[c] || 'No phone'}</span></div><div class="list-sub" style="font-size:11px; margin-top:4px;">Owed: <strong style="color:${totalOwed > 0 ? 'var(--danger)' : 'var(--brand)'}">${formatNaira(totalOwed)}</strong> · ${limitText}<button class="btn-outline" style="padding:2px 6px; font-size:10px; margin-left:6px; border-radius:4px;" onclick="setCreditLimit('${c.replace(/'/g, "\\'")}', ${limit})">Edit Limit</button></div>${uniqueCustomers[c] ? `<div class="actions" style="margin-top:8px;"><a href="tel:${uniqueCustomers[c]}" style="flex:1; text-decoration:none;"><button class="btn-outline" style="width:100%; padding:6px; font-size:12px;">📞 Call</button></a><a href="https://wa.me/${uniqueCustomers[c].replace(/^0/, '234')}" target="_blank" style="flex:1; text-decoration:none;"><button class="wa" style="width:100%; padding:6px; font-size:12px; border:none; border-radius:6px;">WhatsApp</button></a><button class="btn" style="flex:1; padding:6px; font-size:12px;" onclick="startSaleForCustomer('${c.replace(/'/g, "\\'")}', '${uniqueCustomers[c].replace(/'/g, "\\'")}')">+ Sale</button></div>` : ''}</div>`;
    }).join('');
    let suppHtml = uniqueSuppliers.map(s => `<div class="list-item neutral" style="padding:12px; margin-bottom:8px;"><div class="list-header"><span>${s}</span></div></div>`).join('');
    document.getElementById('modal-body').innerHTML = `
        <h3>Directory</h3>
        <div class="segmented"><button class="on" id="dir-tab-cust" onclick="switchDirTab('cust')">Customers (${Object.keys(uniqueCustomers).length})</button><button id="dir-tab-supp" onclick="switchDirTab('supp')">Suppliers (${uniqueSuppliers.length})</button></div>
        <div id="dir-content-cust" style="max-height: 50vh; overflow-y:auto;">${custHtml || '<p style="text-align:center; color:var(--muted); font-size:13px;">No customers yet.</p>'}</div>
        <div id="dir-content-supp" style="display:none; max-height: 50vh; overflow-y:auto;">${suppHtml || '<p style="text-align:center; color:var(--muted); font-size:13px;">No suppliers yet.</p>'}</div>
        <button class="btn btn-outline" style="margin-top:16px;" onclick="closeModal()">Close</button>
    `;
    document.getElementById('modal').classList.add('active');
}
function switchDirTab(tab) {
    document.getElementById('dir-tab-cust').classList.toggle('on', tab === 'cust');
    document.getElementById('dir-tab-supp').classList.toggle('on', tab === 'supp');
    document.getElementById('dir-content-cust').style.display = tab === 'cust' ? 'block' : 'none';
    document.getElementById('dir-content-supp').style.display = tab === 'supp' ? 'block' : 'none';
}
function setCreditLimit(custName, currentLimit) {
    showDialog("Set Credit Limit", `Enter maximum debt allowed for ${custName} (₦). Enter 0 for no limit.`, (val) => {
        const lim = parseFloat(val) || 0; settings.creditLimits[custName] = lim; saveData('settings', settings); showToast('Credit limit updated', 'success'); openDirectory();
    }, true);
    setTimeout(() => { const input = document.getElementById('dialog-input'); if(input) input.value = currentLimit || ''; }, 100);
}
function startSaleForCustomer(name, phone) {
    closeModal(); nav('sales');
    setTimeout(() => { if(document.getElementById('s-customer')) { document.getElementById('s-customer').value = name; document.getElementById('s-phone').value = phone || ''; updateDefaultPrice(); } }, 100);
}
function filterPurchases(query) {
    const q = query.toLowerCase(); const filtered = [...purchases].reverse().filter(p => p.supplierName.toLowerCase().includes(q)).slice(0, 5);
    let html = '';
    filtered.forEach(p => { html += `<div class="list-item neutral" style="padding: 12px; margin-bottom: 8px; cursor:pointer;" onclick="openPurchaseDetails('${p.id}')"><div class="list-header"><span>${p.supplierName}</span><span>${p.material.toUpperCase()}</span></div><div class="list-sub">${p.qty} units · ₦${p.cost.toLocaleString()} ${p.amountPaid < p.cost ? '· <span style="color:var(--danger)">Owing</span>' : ''}</div></div>`; });
    document.getElementById('purchases-inner-list').innerHTML = html || `<p style="font-size:13px; color:var(--muted); text-align:center;">No purchases found.</p>`;
}
function filterSales(query) {
    const q = query.toLowerCase(); const filtered = [...sales].reverse().filter(s => s.customerName.toLowerCase().includes(q) || s.date.includes(q)).slice(0, 15);
    let html = '';
    filtered.forEach(s => { html += `<div class="list-item" style="cursor:pointer;" onclick="openSaleDetails('${s.id}')"><div class="list-header"><span>${s.customerName}</span><strong class="pos">${formatNaira(s.totalAmount)}</strong></div><div class="list-sub">${s.date} · ${s.size}" × ${s.quantity} · Paid ${formatNaira(s.amountPaidAtSale)}</div><div style="display:flex; gap:6px; margin-top:4px; flex-wrap:wrap;">${s.balanceOwing > 0 ? `<span class="tag" style="background:var(--danger-soft); color:var(--danger);">Owing ${formatNaira(s.balanceOwing)}</span>` : ''}${s.deliveryStatus === 'delivered' ? `<span class="tag green">✅ Delivered</span>` : `<span class="tag" style="background:var(--accent-soft); color:var(--warning);">🚚 Pending</span>`}</div></div>`; });
    document.getElementById('sales-history-list').innerHTML = html || `<div class="empty">No sales found.</div>`;
}

function closeModal() { document.getElementById('modal').classList.remove('active'); }

function handleDailyMaintenance() {
    const lastAction = localStorage.getItem('asad:lastAutoAction');
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;
    if (!lastAction) { localStorage.setItem('asad:lastAutoAction', now); return; }
    if (now - lastAction > oneDay) {
        showToast('Starting daily backup & update...', 'success');
        try {
            const data = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.startsWith('asad:') && !key.includes('auth') && !key.includes('lastAutoAction')) {
                    try { data[key] = JSON.parse(localStorage.getItem(key)); } catch(e) { data[key] = localStorage.getItem(key); }
                }
            }
            const jsonStr = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob); const a = document.createElement('a');
            const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_₦/g, '');
            const nowStr = new Date(); const timeStr = nowStr.toTimeString().split(' ')[0].replace(/:/g, '-');
            a.href = url; a.download = `${safeName}_AutoBackup_${getTodayStr()}_${timeStr}.json`;
            document.body.appendChild(a); a.click(); document.body.removeChild(a); window.URL.revokeObjectURL(url);
        } catch(err) { console.log('Auto backup failed', err); }
        localStorage.setItem('asad:lastAutoAction', now);
        setTimeout(async () => {
            try { if ('serviceWorker' in navigator) { const regs = await navigator.serviceWorker.getRegistrations(); for (let r of regs) { await r.unregister(); } } const keys = await caches.keys(); for (let k of keys) { await caches.delete(k); } } catch(e) { console.log(e); }
            window.location.reload();
        }, 3000);
    }
}

function printDocument() {
    if (document.getElementById('modal').classList.contains('active')) document.body.classList.add('printing-modal');
    else document.body.classList.add('printing-page');
    setTimeout(() => {
        window.print();
        setTimeout(() => { document.body.classList.remove('printing-modal'); document.body.classList.remove('printing-page'); }, 500);
    }, 100);
}

if ('serviceWorker' in navigator) { navigator.serviceWorker.register('./sw.js').catch(err => console.log('SW registration failed', err)); }

checkStreak();
handleDailyMaintenance();
if(settings.darkMode) document.body.classList.add('dark');
const bizName = settings.businessName || 'My Business';
document.title = bizName;
if(document.getElementById('login-title-text')) {
    document.getElementById('login-title-text').textContent = bizName;
    document.getElementById('login-logo').textContent = bizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
}
restoreSession();

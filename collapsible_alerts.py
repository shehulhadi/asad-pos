import re
with open('index.html', 'r') as f: html = f.read()

# 1. Replace the alert HTML generation in renderDashboard
old_alert_gen = '''        let lowStockHtml = '';
        if (cementStock <= settings.lowCement) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>🪨 Cement</span><span>${cementStock} bags left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowCement})</div></div>`;
        if (sandStock <= settings.lowSand) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>🏖️ Sand</span><span>${sandStock} trips left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowSand})</div></div>`;
        if (fuelStock <= settings.lowFuel) lowStockHtml += `<div class="list-item alert"><div class="list-header"><span>⛽ Fuel</span><span>${fuelStock} litres left</span></div><div class="list-sub">LOW STOCK ALERT (Threshold: ${settings.lowFuel})</div></div>`;'''

new_alert_gen = '''        let lowStockHtml = '';
        if (cementStock <= settings.lowCement) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🪨 Cement</span><span>${cementStock} bags left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;
        if (sandStock <= settings.lowSand) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>🏖️ Sand</span><span>${sandStock} trips left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;
        if (fuelStock <= settings.lowFuel) lowStockHtml += `<div class="list-item alert" style="margin-bottom:8px;"><div class="list-header"><span>⛽ Fuel</span><span>${fuelStock} litres left</span></div><div class="list-sub">LOW STOCK ALERT</div></div>`;

        let alertWrapper = '';
        if (lowStockHtml) {
            const isCollapsed = localStorage.getItem('asad:alertsCollapsed') === 'true';
            const displayStyle = isCollapsed ? 'none' : 'block';
            const iconState = isCollapsed ? '▼' : '▲';
            alertWrapper = `
                <div style="margin-bottom:16px;">
                    <div class="section-title neg" onclick="toggleAlerts()" style="margin-top:0; margin-bottom:0; cursor:pointer; display:flex; justify-content:space-between; align-items:center; background:var(--danger-soft); padding:12px 16px; border-radius:12px; border:1px solid #f7bcbc;">
                        <span style="display:flex; align-items:center; gap:8px;">${ico('alert')} Low Stock Alerts</span>
                        <span id="alert-toggle-icon" style="font-size:12px;">${iconState}</span>
                    </div>
                    <div id="alert-list-container" style="display:${displayStyle}; margin-top:12px;">
                        ${lowStockHtml}
                    </div>
                </div>
            `;
        }'''
html = html.replace(old_alert_gen, new_alert_gen)

# 2. Update the Dashboard HTML to use the wrapper
old_dash_insert = '''            ${lowStockHtml ? `<div class="section-title neg">${ico('alert')} Low Stock Alerts</div>${lowStockHtml}` : ''}'''
new_dash_insert = '''            ${alertWrapper}'''
html = html.replace(old_dash_insert, new_dash_insert)

# 3. Add the toggle function
toggle_func = '''
    function toggleAlerts() {
        const container = document.getElementById('alert-list-container');
        const icon = document.getElementById('alert-toggle-icon');
        if (!container) return;
        if (container.style.display === 'none') {
            container.style.display = 'block';
            icon.textContent = '▲';
            localStorage.setItem('asad:alertsCollapsed', 'false');
        } else {
            container.style.display = 'none';
            icon.textContent = '▼';
            localStorage.setItem('asad:alertsCollapsed', 'true');
        }
    }
'''
html = html.replace('// --- Details & Edit Modals ---', toggle_func + '\n// --- Details & Edit Modals ---')

with open('index.html', 'w') as f: f.write(html)

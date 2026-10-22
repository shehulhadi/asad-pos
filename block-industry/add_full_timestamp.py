import re
with open('app.js', 'r') as f: js = f.read()

# Locate the openStockItem function and replace the display logic to include time
old_map = '''    historyHtml = hist.slice(0, 20).map(h => {
        let clickAttr = '';
        if (h.clickType === 'pur') clickAttr = `onclick="openPurchaseDetails('${h.id}')" style="cursor:pointer;"`;
        if (h.clickType === 'sale') clickAttr = `onclick="openSaleDetails('${h.id}')" style="cursor:pointer;"`;
        return `<div class="kv" ${clickAttr}><span>${h.date} · ${h.desc}</span><strong style="color:${h.color};">${h.qty}</strong></div>`;
    }).join('');'''

new_map = '''    historyHtml = hist.slice(0, 20).map(h => {
        let clickAttr = '';
        if (h.clickType === 'pur') clickAttr = `onclick="openPurchaseDetails('${h.id}')" style="cursor:pointer;"`;
        if (h.clickType === 'sale') clickAttr = `onclick="openSaleDetails('${h.id}')" style="cursor:pointer;"`;
        
        let timeStr = '';
        if (h.timestamp) {
            const dt = new Date(h.timestamp);
            const time = dt.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
            timeStr = ' ' + time;
        }
        
        return `<div class="kv" ${clickAttr}><span>${h.date}${timeStr} · ${h.desc}</span><strong style="color:${h.color};">${h.qty}</strong></div>`;
    }).join('');'''

js = js.replace(old_map, new_map)

with open('app.js', 'w') as f: f.write(js)
print("Full timestamp added to history.")

import re
with open('app.js', 'r') as f: js = f.read()

# Find the exact spot in renderAnalytics to inject the missing calculation
target_str = '''    const totalQtySold = sales.reduce((sum, s) => sum + s.quantity, 0);
    const profitPerBlock = totalQtySold > 0 ? (allRevenue - allCOGS) / totalQtySold : 0;
    let breakEvenText = "Set fixed costs in Settings";'''

replacement = '''    let marginAlertHtml = '';
    sales.forEach(s => {
        const avgCost = getAvgCost(s.size);
        const minPrice = avgCost * (1 + (settings.marginAlertPct/100));
        if (s.pricePerBlock < minPrice && avgCost > 0) {
            marginAlertHtml += `<div class="list-item alert"><div class="list-header"><span>${s.customerName}</span><span>${formatNaira(s.pricePerBlock)}/block</span></div><div class="list-sub">${t.marginWarning} (Cost: ${formatNaira(avgCost)})</div></div>`;
        }
    });

    const totalQtySold = sales.reduce((sum, s) => sum + s.quantity, 0);
    const profitPerBlock = totalQtySold > 0 ? (allRevenue - allCOGS) / totalQtySold : 0;
    let breakEvenText = "Set fixed costs in Settings";'''

js = js.replace(target_str, replacement)

with open('app.js', 'w') as f: f.write(js)
print("Margin error fixed.")

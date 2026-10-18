with open('index.html', 'r') as f: html = f.read()

# 1. Add the calculation logic inside renderDashboard
old_logic = '''        const monthRev = sales.filter(s => s.date >= monthAgo).reduce((sum, s) => sum + s.totalAmount, 0);'''
new_logic = '''        const monthRev = sales.filter(s => s.date >= monthAgo).reduce((sum, s) => sum + s.totalAmount, 0);

        // Month-over-Month Calculation
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();
        const thisMonthRev = sales.filter(s => {
            const d = new Date(s.date);
            return d.getMonth() === currentMonth && d.getFullYear() === currentYear;
        }).reduce((sum, s) => sum + s.totalAmount, 0);

        const lastMonthDate = new Date(currentYear, currentMonth - 1, 1);
        const lastMonth = lastMonthDate.getMonth();
        const lastMonthYear = lastMonthDate.getFullYear();
        const lastMonthRev = sales.filter(s => {
            const d = new Date(s.date);
            return d.getMonth() === lastMonth && d.getFullYear() === lastMonthYear;
        }).reduce((sum, s) => sum + s.totalAmount, 0);

        let momChangeHtml = '';
        if (lastMonthRev > 0) {
            const diff = thisMonthRev - lastMonthRev;
            const pct = (diff / lastMonthRev) * 100;
            const isUp = diff >= 0;
            momChangeHtml = `<div style="display:flex; align-items:center; justify-content:center; gap:4px; font-size:11px; font-weight:800; color:${isUp ? 'var(--brand-dark)' : 'var(--danger)'}; margin-top:4px;">
                ${isUp ? '↑' : '↓'} ${Math.abs(pct).toFixed(1)}% vs last month
            </div>`;
        } else if (thisMonthRev > 0) {
            momChangeHtml = `<div style="font-size:11px; font-weight:800; color:var(--brand-dark); margin-top:4px;">↑ New sales this month</div>`;
        }'''
html = html.replace(old_logic, new_logic)

# 2. Inject the HTML into the "This Month" box
old_html = '''<div><small>This Month</small><strong>${formatNaira(monthRev)}</strong></div>'''
new_html = '''<div><small>This Month</small><strong>${formatNaira(monthRev)}</strong>${momChangeHtml}</div>'''
html = html.replace(old_html, new_html)

with open('index.html', 'w') as f: f.write(html)

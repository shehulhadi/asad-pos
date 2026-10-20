with open('app.js', 'r') as f: js = f.read()

# Find the Quick Actions inside renderAnalytics
old_quick = '''        <div class="quick">
            <button onclick="nav('dashboard')">${ico('box')} Stock</button>
            <button onclick="nav('reports')">${ico('report')} Reports</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand);">📊 Close Day</button>
        </div>'''

new_quick = '''        <div class="quick" style="flex-wrap: wrap;">
            <button onclick="nav('dashboard')" style="flex: 1 1 30%;">${ico('box')} Stock</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''

js = js.replace(old_quick, new_quick)

with open('app.js', 'w') as f: f.write(js)
print("Debts button added to Analytics quick actions.")

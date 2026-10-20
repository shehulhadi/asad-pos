with open('app.js', 'r') as f: js = f.read()

# 1. Update Stock Page (renderDashboard) - Remove Prod
old_stock_quick = '''        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="nav('production')" style="flex: 1 1 30%;">${ico('production')} Prod</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''

new_stock_quick = '''        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 45%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 45%;">${ico('debts')} Debts</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''
js = js.replace(old_stock_quick, new_stock_quick)

# 2. Update Analytics Page (renderAnalytics) - Remove Stock, Add Prod
old_ana_quick = '''        <div class="quick" style="flex-wrap: wrap;">
            <button onclick="nav('dashboard')" style="flex: 1 1 30%;">${ico('box')} Stock</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''

new_ana_quick = '''        <div class="quick" style="flex-wrap: wrap;">
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="nav('production')" style="flex: 1 1 30%;">${ico('production')} Prod</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''
js = js.replace(old_ana_quick, new_ana_quick)

with open('app.js', 'w') as f: f.write(js)
print("Quick actions swapped perfectly.")

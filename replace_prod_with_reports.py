with open('app.js', 'r') as f: js = f.read()

# Replace the Quick Actions block in renderDashboard
old_quick = '''        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            <button onclick="nav('production')" style="flex: 1 1 45%;">${ico('production')} Production</button>
            <button onclick="nav('debts')" style="flex: 1 1 45%;">${ico('debts')} Debts</button>
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 45%;">${ico('report')} Reports</button>` : ''}
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 45%;">📊 Close Day</button>
        </div>'''

new_quick = '''        <div class="quick" style="margin-bottom: 20px; flex-wrap: wrap;">
            ${currentUser === 'owner' ? `<button onclick="nav('reports')" style="flex: 1 1 30%;">${ico('report')} Reports</button>` : ''}
            <button onclick="nav('debts')" style="flex: 1 1 30%;">${ico('debts')} Debts</button>
            <button onclick="nav('production')" style="flex: 1 1 30%;">${ico('production')} Prod</button>
            <button onclick="openDailyClosing()" style="color:var(--brand); border-color:var(--brand); flex: 1 1 100%; margin-top: 8px;">📊 Close Day</button>
        </div>'''
js = js.replace(old_quick, new_quick)

with open('app.js', 'w') as f: f.write(js)

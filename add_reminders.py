import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add reminder setting to defaults
html = html.replace(
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0",
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0, reminderInterval: 0"
)
if "if(settings.reminderInterval === undefined)" in html:
    html = html.replace(
        "if(settings.bestDayAmount === undefined) settings.bestDayAmount = 0;",
        "if(settings.bestDayAmount === undefined) settings.bestDayAmount = 0;\n    if(settings.reminderInterval === undefined) settings.reminderInterval = 0;"
    )

# 2. Add Reminder UI to Settings
old_settings_ui = '''            <div class="form-group" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; background:var(--bg); padding:12px; border-radius:8px;">
                <label style="margin:0; font-size:14px; font-weight:700;">Dark Mode</label>
                <input type="checkbox" id="set-dark-mode" style="width:20px; height:20px;" ${settings.darkMode ? 'checked' : ''}>
            </div>'''
new_settings_ui = '''            <div class="form-group" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; background:var(--bg); padding:12px; border-radius:8px;">
                <label style="margin:0; font-size:14px; font-weight:700;">Dark Mode</label>
                <input type="checkbox" id="set-dark-mode" style="width:20px; height:20px;" ${settings.darkMode ? 'checked' : ''}>
            </div>
            <div class="form-group" style="margin-top:16px;">
                <label>Sales Reminder Notification</label>
                <select id="set-reminder">
                    <option value="0" ${settings.reminderInterval == 0 ? 'selected' : ''}>Off</option>
                    <option value="1" ${settings.reminderInterval == 1 ? 'selected' : ''}>Every 1 Hour</option>
                    <option value="2" ${settings.reminderInterval == 2 ? 'selected' : ''}>Every 2 Hours</option>
                    <option value="4" ${settings.reminderInterval == 4 ? 'selected' : ''}>Every 4 Hours</option>
                    <option value="8" ${settings.reminderInterval == 8 ? 'selected' : ''}>Every 8 Hours</option>
                </select>
                <p style="font-size:11px; color:var(--muted); margin-top:4px;">Note: Reminders work while the app is running in the background. If you swipe the app away, Android stops the timer.</p>
            </div>'''
html = html.replace(old_settings_ui, new_settings_ui)

# 3. Save reminder setting and restart timer
old_save = '''        settings.darkMode = document.getElementById('set-dark-mode').checked;
        if(settings.darkMode) document.body.classList.add('dark');
        else document.body.classList.remove('dark');'''
new_save = '''        settings.darkMode = document.getElementById('set-dark-mode').checked;
        if(settings.darkMode) document.body.classList.add('dark');
        else document.body.classList.remove('dark');
        
        const newReminder = parseInt(document.getElementById('set-reminder').value);
        if (newReminder > 0 && Notification.permission !== 'granted') {
            Notification.requestPermission().then(perm => {
                if (perm === 'granted') {
                    settings.reminderInterval = newReminder;
                    saveData('settings', settings);
                    setupReminders();
                } else {
                    showToast('Notification permission denied', 'err');
                }
            });
        } else {
            settings.reminderInterval = newReminder;
            setupReminders();
        }'''
html = html.replace(old_save, new_save)

# 4. Add Timer Logic
reminder_js = '''
    let reminderTimer = null;
    function setupReminders() {
        if (reminderTimer) clearInterval(reminderTimer);
        if (settings.reminderInterval && settings.reminderInterval > 0) {
            if (Notification.permission === 'granted') {
                reminderTimer = setInterval(() => {
                    const now = new Date();
                    // Don't remind at night (10 PM to 6 AM)
                    if (now.getHours() >= 22 || now.getHours() < 6) return;
                    
                    if (document.visibilityState === 'hidden') {
                        new Notification("🧱 Sales Reminder", {
                            body: "Don't forget to log your recent block sales!",
                            icon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzA1OTY2OSIvPjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1zaXplPSI0MCIgZm9udC1mYW1pbHk9InNhbnMtc2VyaWYiIGZvbnQtd2VpZ2h0PSJib2xkIiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSI+Qkk8L3RleHQ+PC9zdmc+"
                        });
                    } else {
                        showToast("⏰ Reminder: Don't forget to log your sales!", "success");
                    }
                }, settings.reminderInterval * 60 * 60 * 1000);
            }
        }
    }

    // --- Gamification Features ---
'''
html = html.replace('// --- Gamification Features ---', reminder_js)

# 5. Initialize reminders on load
html = html.replace(
    "checkStreak();",
    "checkStreak();\n    setupReminders();"
)

with open('index.html', 'w') as f: f.write(html)

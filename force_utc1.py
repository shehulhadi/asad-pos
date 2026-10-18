import re
with open('index.html', 'r') as f: html = f.read()

# 1. Inject the UTC+1 Time Helper functions
time_helpers = '''
    // --- UTC+1 (Nigeria) Time Helpers ---
    function getWATDate() {
        const now = new Date();
        // Convert local time to UTC, then add 1 hour
        const watTime = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (1 * 3600000));
        return watTime;
    }
    function getTodayStr() {
        return getWATDate().toISOString().split('T')[0];
    }

    function saveData(key, data) { localStorage.setItem('asad:' + key, JSON.stringify(data)); }
'''
html = html.replace('    function saveData(key, data) { localStorage.setItem(\'asad:\' + key, JSON.stringify(data)); }', time_helpers)

# 2. Replace all instances of current date generation with getTodayStr()
html = html.replace("new Date().toISOString().split('T')[0]", "getTodayStr()")

# 3. Replace timestamps with UTC+1 timestamps
# We don't want to replace ALL new Date().toISOString(), only the ones used for createdAt and data storage
html = html.replace("createdAt: new Date().toISOString()", "createdAt: getWATDate().toISOString()")
html = html.replace("lastAction = Date.now()", "lastAction = getWATDate().getTime()")

# 4. Replace display time strings with UTC+1
html = html.replace("new Date().toLocaleTimeString()", "getWATDate().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })")
html = html.replace("new Date(s.createdAt).toLocaleTimeString()", "new Date(s.createdAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })")

# 5. Fix the time string in the Daily Closing Report
html = html.replace("const dayName = d.toLocaleDateString('en-US', {weekday:'long', year:'numeric', month:'long', day:'numeric'});", "const dayName = getWATDate().toLocaleDateString('en-US', {weekday:'long', year:'numeric', month:'long', day:'numeric'});")

with open('index.html', 'w') as f: f.write(html)

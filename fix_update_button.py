with open('index.html', 'r') as f: html = f.read()

# 1. Remove the redundant Refresh button from the HTML header
html = html.replace('<button class="icon-btn" id="btn-refresh" onclick="nav(\'dashboard\')" title="Refresh Dashboard"></button>\n                ', '')

# 2. Update loadApp() to remove references to btn-refresh and change ib-update icon
old_load_app = '''        document.getElementById('ib-update').innerHTML = ico('update');
        document.getElementById('ib-backup').innerHTML = ico('update'); // Using update icon as backup trigger
        document.getElementById('ib-logout').innerHTML = ico('logout');
        document.getElementById('btn-refresh').innerHTML = ico('refresh');
        document.getElementById('btn-settings').innerHTML = ico('settings');
        const owner = currentUser === 'owner';
        document.getElementById('btn-refresh').classList.toggle('show', owner);
        document.getElementById('btn-settings').classList.toggle('show', owner);'''

new_load_app = '''        document.getElementById('ib-update').innerHTML = ico('refresh');
        document.getElementById('ib-backup').innerHTML = ico('update');
        document.getElementById('ib-logout').innerHTML = ico('logout');
        document.getElementById('btn-settings').innerHTML = ico('settings');
        const owner = currentUser === 'owner';
        document.getElementById('btn-settings').classList.toggle('show', owner);'''
html = html.replace(old_load_app, new_load_app)

# 3. Ensure the forceUpdate function is robust
old_force_update = '''    function forceUpdate() {
        showDialog("Clear App Cache?", "This only downloads new app updates. YOUR STOCK, SALES, AND DEBTS WILL NOT BE DELETED.", async () => {
            if ('serviceWorker' in navigator) {
                const registrations = await navigator.serviceWorker.getRegistrations();
                for (let registration of registrations) { await registration.unregister(); }
            }
            const keys = await caches.keys();
            for (let key of keys) { await caches.delete(key); }
            location.reload(true);
        });
    }'''

new_force_update = '''    async function forceUpdate() {
        showDialog("Update App?", "This will download the latest version.\\nYOUR STOCK, SALES, AND DEBTS WILL NOT BE DELETED.", async () => {
            try {
                if ('serviceWorker' in navigator) {
                    const registrations = await navigator.serviceWorker.getRegistrations();
                    for (let registration of registrations) { await registration.unregister(); }
                }
                const keys = await caches.keys();
                for (let key of keys) { await caches.delete(key); }
            } catch(e) { console.log('Cache clear error', e); }
            
            showToast('Clearing cache and updating...', 'success');
            setTimeout(() => {
                // Force a hard reload bypassing browser cache
                window.location.href = window.location.pathname + '?v=' + Date.now();
            }, 1000);
        });
    }'''
html = html.replace(old_force_update, new_force_update)

with open('index.html', 'w') as f: f.write(html)

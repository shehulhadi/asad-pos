import re
with open('index.html', 'r') as f: html = f.read()

# Inject the automatic maintenance script right before the restoreSession() call
maintenance_js = '''
    // --- Auto Backup & Cache Clear (Once every 24 hours) ---
    function handleDailyMaintenance() {
        const lastAction = localStorage.getItem('asad:lastAutoAction');
        const now = Date.now();
        const oneDay = 24 * 60 * 60 * 1000;

        // If never set, just set it and do nothing
        if (!lastAction) {
            localStorage.setItem('asad:lastAutoAction', now);
            return;
        }

        // If 24 hours have passed
        if (now - lastAction > oneDay) {
            showToast('Starting daily backup & update...', 'success');

            // 1. Silent Auto Backup
            try {
                const data = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    // Don't backup auth session or the timer itself
                    if (key.startsWith('asad:') && !key.includes('auth') && !key.includes('lastAutoAction')) {
                        try { data[key] = JSON.parse(localStorage.getItem(key)); }
                        catch(e) { data[key] = localStorage.getItem(key); }
                    }
                }
                const jsonStr = JSON.stringify(data, null, 2);
                const blob = new Blob([jsonStr], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `AsadTech_AutoBackup_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch(err) {
                console.log('Auto backup failed', err);
            }

            // 2. Update the timer immediately
            localStorage.setItem('asad:lastAutoAction', now);

            // 3. Clear Cache and Reload after a short delay
            setTimeout(async () => {
                try {
                    if ('serviceWorker' in navigator) {
                        const regs = await navigator.serviceWorker.getRegistrations();
                        for (let r of regs) { await r.unregister(); }
                    }
                    const keys = await caches.keys();
                    for (let k of keys) { await caches.delete(k); }
                } catch(e) { console.log('Cache clear error', e); }
                
                window.location.reload();
            }, 3000); // 3 second delay so the download can start
        }
    }

    handleDailyMaintenance();
    restoreSession();
'''

html = html.replace('    restoreSession();', maintenance_js)

with open('index.html', 'w') as f: f.write(html)

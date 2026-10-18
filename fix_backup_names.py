import re
with open('index.html', 'r') as f: html = f.read()

# 1. Update manual exportJSON filename
old_export_name = '''        const jsonStr = JSON.stringify(data, null, 2);
        const filename = `AsadTech_Backup_${new Date().toISOString().split('T')[0]}.txt`;'''
new_export_name = '''        const jsonStr = JSON.stringify(data, null, 2);
        const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
        const filename = `${safeName}_Backup_${new Date().toISOString().split('T')[0]}.txt`;'''
html = html.replace(old_export_name, new_export_name)

# 2. Update auto-backup filename in handleDailyMaintenance
old_auto_name = '''                const a = document.createElement('a');
                a.href = url;
                a.download = `AsadTech_AutoBackup_${new Date().toISOString().split('T')[0]}.json`;'''
new_auto_name = '''                const safeName = (settings.businessName || 'Business').replace(/[^a-zA-Z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
                const a = document.createElement('a');
                a.href = url;
                a.download = `${safeName}_AutoBackup_${new Date().toISOString().split('T')[0]}.json`;'''
html = html.replace(old_auto_name, new_auto_name)

with open('index.html', 'w') as f: f.write(html)

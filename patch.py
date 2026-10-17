import re
with open('index.html', 'r') as f: html = f.read()

# Fix the exportJSON crash
old_code = '''        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('asad:')) data[key] = JSON.parse(localStorage.getItem(key));
        }
        const jsonStr = JSON.stringify(data, null, 2);'''

new_code = '''        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('asad:')) {
                try { data[key] = JSON.parse(localStorage.getItem(key)); } 
                catch(e) { data[key] = localStorage.getItem(key); }
            }
        }
        const jsonStr = JSON.stringify(data, null, 2);'''

html = html.replace(old_code, new_code)
with open('index.html', 'w') as f: f.write(html)

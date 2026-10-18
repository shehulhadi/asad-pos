import re
with open('index.html', 'r') as f: html = f.read()

# 1. Find and completely replace the @media print block
start_idx = html.find('@media print {')
if start_idx != -1:
    # Find the end of the media query block (counting brackets)
    open_brackets = 0
    end_idx = start_idx
    for i in range(start_idx, len(html)):
        if html[i] == '{': open_brackets += 1
        elif html[i] == '}': 
            open_brackets -= 1
            if open_brackets == 0:
                end_idx = i + 1
                break

    new_css = '''@media print {
            /* 1. Unlock the page height and overflow */
            html, body {
                height: auto !important;
                min-height: auto !important;
                overflow: visible !important;
                display: block !important;
                background: #fff !important;
            }
            
            /* 2. Hide all app navigation and non-printing elements */
            header, nav, #toast-container, .dialog-overlay, .icon-btn, .btn, .actions, .back-link, .quick { 
                display: none !important; 
            }

            /* 3. If printing a Modal (Receipt) */
            body.printing-modal #app-view, body.printing-modal #login-view { display: none !important; }
            body.printing-modal #modal {
                display: block !important;
                position: static !important;
                inset: auto !important;
                background: transparent !important;
                backdrop-filter: none !important;
                padding: 0 !important;
                margin: 0 !important;
                width: 100% !important;
                height: auto !important;
            }
            body.printing-modal #modal .modal-content {
                display: block !important;
                position: static !important;
                box-shadow: none !important;
                border: none !important;
                max-height: none !important;
                overflow: visible !important;
                padding: 0 !important;
                margin: 0 !important;
                width: 100% !important;
                max-width: 100% !important;
            }
            /* Hide buttons inside the printed modal */
            body.printing-modal #modal button { display: none !important; }

            /* 4. If printing a Page (Reports) */
            body.printing-page #modal { display: none !important; }
            body.printing-page #app-view { display: block !important; height: auto !important; }
            body.printing-page main { display: block !important; padding: 0 !important; overflow: visible !important; height: auto !important; }
            
            /* 5. Prevent page breaks inside cards */
            .card { page-break-inside: avoid; }
        }'''
    
    html = html[:start_idx] + new_css + html[end_idx:]

# 2. Update printDocument to add a slight delay so the browser renders the print CSS first
old_print_js = re.search(r'    function printDocument\(\) \{.*?\n    \}', html, re.DOTALL).group(0)
new_print_js = '''    function printDocument() {
        if (document.getElementById('modal').classList.contains('active')) {
            document.body.classList.add('printing-modal');
        } else {
            document.body.classList.add('printing-page');
        }
        
        // Give the browser 100ms to apply the print CSS before opening the dialog
        setTimeout(() => {
            window.print();
            setTimeout(() => {
                document.body.classList.remove('printing-modal');
                document.body.classList.remove('printing-page');
            }, 500);
        }, 100);
    }'''
html = html.replace(old_print_js, new_print_js)

with open('index.html', 'w') as f: f.write(html)

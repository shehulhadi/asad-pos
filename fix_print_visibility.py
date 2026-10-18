import re
with open('index.html', 'r') as f: html = f.read()

# 1. Replace the print CSS with a visibility-based approach
old_css = re.search(r'@media print \{.*?\n        \}', html, re.DOTALL).group(0)
new_css = '''@media print {
            /* Hide everything on the page */
            body * { visibility: hidden !important; }
            
            /* Make ONLY the active modal and its contents visible */
            body.printing-modal #modal, body.printing-modal #modal * { visibility: visible !important; }
            body.printing-modal #modal { 
                position: absolute !important; 
                left: 0 !important; 
                top: 0 !important; 
                width: 100% !important; 
                display: block !important; 
                background: #fff !important; 
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
                padding: 0 !important; 
                margin: 0 !important; 
            }
            body.printing-modal #modal .modal-content { 
                box-shadow: none !important; 
                border: none !important; 
                max-height: none !important; 
                overflow: visible !important; 
                padding: 0 !important; 
                margin: 0 !important; 
                width: 100% !important; 
                max-width: 100% !important; 
                background: #fff !important;
                animation: none !important;
            }
            /* Hide buttons in the printed modal */
            body.printing-modal #modal .actions, 
            body.printing-modal #modal .row, 
            body.printing-modal #modal button { display: none !important; }

            /* Make ONLY the main content visible for Reports */
            body.printing-page main, body.printing-page main * { visibility: visible !important; }
            body.printing-page main { 
                position: absolute !important; 
                left: 0 !important; 
                top: 0 !important; 
                width: 100% !important; 
                padding: 0 !important; 
            }
            body.printing-page header, body.printing-page nav, body.printing-page .btn, 
            body.printing-page .actions, body.printing-page input, body.printing-page select,
            body.printing-page .back-link { display: none !important; }
        }'''
html = html.replace(old_css, new_css)

# 2. Ensure the printDocument function is clean and adds the class correctly
old_print_js = re.search(r'    function printDocument\(\) \{.*?\n    \}', html, re.DOTALL).group(0)
new_print_js = '''    function printDocument() {
        if (document.getElementById('modal').classList.contains('active')) {
            document.body.classList.add('printing-modal');
        } else {
            document.body.classList.add('printing-page');
        }
        
        window.print();
        
        setTimeout(() => {
            document.body.classList.remove('printing-modal');
            document.body.classList.remove('printing-page');
        }, 1000);
    }'''
html = html.replace(old_print_js, new_print_js)

with open('index.html', 'w') as f: f.write(html)

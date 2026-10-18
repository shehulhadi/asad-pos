import re
with open('index.html', 'r') as f: html = f.read()

# 1. Completely replace the print CSS with an isolation strategy
old_css = re.search(r'@media print \{.*?\n        \}', html, re.DOTALL).group(0)
new_css = '''@media print {
            /* Hide everything on the page by default */
            body > * { display: none !important; }
            
            /* Print ONLY the modal (receipt) if a modal is active */
            body.printing-modal #modal { display: block !important; position: static !important; background: transparent !important; padding: 0 !important; }
            body.printing-modal #modal .modal-content { display: block !important; box-shadow: none !important; border: none !important; width: 100% !important; max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
            
            /* Hide buttons/actions inside the printed modal */
            body.printing-modal #modal button, 
            body.printing-modal #modal .actions, 
            body.printing-modal #modal .row,
            body.printing-modal #modal a { display: none !important; }
            
            /* Print ONLY the main content (e.g. Reports) if no modal is active */
            body.printing-page main { display: block !important; position: static !important; padding: 0 !important; width: 100% !important; }
            body.printing-page header, body.printing-page nav { display: none !important; }
            
            /* Hide inputs and buttons on the page being printed */
            body.printing-page .btn, 
            body.printing-page .actions, 
            body.printing-page input, 
            body.printing-page select, 
            body.printing-page .back-link { display: none !important; }
            
            /* General print formatting */
            body { height: auto !important; overflow: visible !important; background: #fff !important; }
            .card { box-shadow: none !important; border: 1px solid #ccc !important; page-break-inside: avoid; }
            .modal-content { animation: none !important; }
        }'''
html = html.replace(old_css, new_css)

# 2. Replace all window.print() calls with our new printDocument() function
html = html.replace('onclick="window.print()"', 'onclick="printDocument()"')

# 3. Add the printDocument JS logic
print_func = '''
    function printDocument() {
        const isModalOpen = document.getElementById('modal').classList.contains('active');
        if (isModalOpen) {
            document.body.classList.add('printing-modal');
        } else {
            document.body.classList.add('printing-page');
        }
        
        window.print();
        
        // Clean up classes after print dialog closes
        setTimeout(() => {
            document.body.classList.remove('printing-modal');
            document.body.classList.remove('printing-page');
        }, 1000);
    }
    
    // Ensure cleanup happens even if print is cancelled
    window.onafterprint = () => {
        document.body.classList.remove('printing-modal');
        document.body.classList.remove('printing-page');
    };
'''
if 'function printDocument()' not in html:
    html = html.replace('// --- Clear Cache ---', print_func + '\n// --- Clear Cache ---')

with open('index.html', 'w') as f: f.write(html)

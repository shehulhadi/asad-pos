import re
with open('index.html', 'r') as f: html = f.read()

# 1. Make Expenses clickable
html = html.replace(
    'recent.forEach(e => { listHtml += `<div class="list-item neutral"><div class="list-header">',
    'recent.forEach(e => { listHtml += `<div class="list-item neutral" style="cursor:pointer;" onclick="openExpenseDetails(\'${e.id}\')"><div class="list-header">'
)

# 2. Add Delete Buttons to Sale Details
html = html.replace(
    '''<div class="row">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
            </div>''',
    '''<div class="row">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editSale('${s.id}')">Edit Sale</button>
            </div>
            <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteSale('${s.id}')">Delete Sale</button>'''
)

# 3. Add Delete Buttons to Batch Details
html = html.replace(
    '''<div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editBatch('${b.id}')">Edit Batch</button>
            </div>''',
    '''<div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editBatch('${b.id}')">Edit Batch</button>
            </div>
            <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteBatch('${b.id}')">Delete Batch</button>'''
)

# 4. Inject the new logic functions
new_functions = '''
    // --- Delete Logic ---
    function deleteSale(id) {
        showDialog("Delete Sale?", "Are you sure? This will remove the sale and return the blocks to your inventory.", () => {
            sales = sales.filter(s => s.id !== id);
            saveData('sales', sales);
            closeModal();
            nav('sales');
            showToast('Sale deleted', 'success');
        });
    }

    function deleteBatch(id) {
        showDialog("Delete Batch?", "Are you sure? This will remove all blocks produced in this batch.", () => {
            batches = batches.filter(b => b.id !== id);
            saveData('batches', batches);
            closeModal();
            nav('production');
            showToast('Batch deleted', 'success');
        });
    }

    // --- Expense Edit & Delete Logic ---
    function openExpenseDetails(id) {
        const e = expenses.find(x => x.id === id);
        if (!e) return;
        document.getElementById('modal-body').innerHTML = `
            <h3>Expense Details</h3>
            <div class="kv"><span>Date</span><strong>${e.date}</strong></div>
            <div class="kv"><span>Category</span><strong style="text-transform:capitalize;">${e.category}</strong></div>
            <div class="kv"><span>Amount</span><strong class="neg">${formatNaira(e.amount)}</strong></div>
            <div class="kv"><span>Note</span><strong>${e.note || 'N/A'}</strong></div>
            <div class="row" style="margin-top:24px;">
                <button class="btn btn-outline" onclick="closeModal()">Close</button>
                <button class="btn" onclick="editExpense('${e.id}')">Edit</button>
            </div>
            <button class="btn btn-danger" style="margin-top:12px;" onclick="deleteExpense('${e.id}')">Delete Expense</button>
        `;
        document.getElementById('modal').classList.add('active');
    }

    function editExpense(id) {
        const e = expenses.find(x => x.id === id);
        const t = i18n[settings.lang];
        const cats = ['wages', 'repairs', 'generator_fuel', 'rent', 'transport', 'loaders', 'phone_data', 'other', ...settings.customExpenses];
        
        document.getElementById('modal-body').innerHTML = `
            <h3>Edit Expense</h3>
            <div class="row">
                <div class="form-group"><label>Date</label><input type="date" id="edit-e-date" value="${e.date}"></div>
                <div class="form-group"><label>Category</label>
                    <select id="edit-e-category">
                        ${cats.map(c => `<option value="${c}" ${e.category === c ? 'selected' : ''}>${t[c] || c}</option>`).join('')}
                    </select>
                </div>
            </div>
            <div class="form-group"><label>Amount (₦)</label><input type="number" id="edit-e-amount" value="${e.amount}"></div>
            <div class="form-group"><label>Note</label><input type="text" id="edit-e-note" value="${e.note || ''}"></div>
            <div class="row">
                <button class="btn btn-outline" onclick="openExpenseDetails('${e.id}')">Back</button>
                <button class="btn" onclick="saveEditedExpense('${e.id}')">Save Changes</button>
            </div>
        `;
    }

    function saveEditedExpense(id) {
        const e = expenses.find(x => x.id === id);
        e.date = document.getElementById('edit-e-date').value;
        e.category = document.getElementById('edit-e-category').value;
        e.amount = parseFloat(document.getElementById('edit-e-amount').value) || 0;
        e.note = document.getElementById('edit-e-note').value;
        
        saveData('expenses', expenses);
        closeModal();
        nav('expenses');
        showToast('Expense updated', 'success');
    }

    function deleteExpense(id) {
        showDialog("Delete Expense?", "Are you sure you want to remove this expense?", () => {
            expenses = expenses.filter(e => e.id !== id);
            saveData('expenses', expenses);
            closeModal();
            nav('expenses');
            showToast('Expense deleted', 'success');
        });
    }

    // --- Debts Module ---
'''
html = html.replace('// --- Debts Module ---', new_functions)

with open('index.html', 'w') as f: f.write(html)

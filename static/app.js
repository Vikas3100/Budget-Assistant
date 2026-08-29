// Fetch dashboard data periodically and after every interaction
async function fetchDashboard() {
    try {
        const response = await fetch('/api/expenses');
        const data = await response.json();
        
        // Update summary numbers
        const budgetEl = document.getElementById('monthly-budget');
        const remainingEl = document.getElementById('remaining-budget');
        const spentEl = document.getElementById('total-spent');
        const deletedEl = document.getElementById('total-deleted');

        if (budgetEl) {
            if (data.budget_set) {
                budgetEl.innerText = `₹${Number(data.monthly_budget).toLocaleString()}`;
                budgetEl.style.color = '#60a5fa';
            } else {
                budgetEl.innerText = 'Not Set (Enter in chat)';
                budgetEl.style.color = 'var(--text-secondary)';
                budgetEl.style.fontSize = '18px';
            }
        }

        const remaining = Number(data.remaining_budget) || 0;
        if (!data.budget_set && (Number(data.total_spent) || 0) === 0) {
            remainingEl.innerText = '₹0';
            remainingEl.style.color = 'var(--text-secondary)';
        } else if (remaining < 0) {
            remainingEl.innerText = `-₹${Math.abs(remaining).toLocaleString()}`;
            remainingEl.style.color = '#ef4444';
        } else {
            remainingEl.innerText = `₹${remaining.toLocaleString()}`;
            remainingEl.style.color = '#10b981';
        }

        spentEl.innerText = `₹${(Number(data.total_spent) || 0).toLocaleString()}`;
        deletedEl.innerText = `₹${(Number(data.total_deleted) || 0).toLocaleString()}`;
        
        // Update active transactions list
        const txList = document.getElementById('transactions-list');
        txList.innerHTML = '';
        if (data.expenses && data.expenses.length > 0) {
            // Reverse so newest is on top
            data.expenses.slice().reverse().forEach(tx => {
                const el = document.createElement('div');
                el.className = 'list-item';
                el.innerHTML = `
                    <div class="info">
                        <span class="item-name">${tx.item}</span>
                        <span class="item-cat">${tx.category}</span>
                    </div>
                    <div class="amount text-danger">₹${Number(tx.amount).toLocaleString()}</div>
                `;
                txList.appendChild(el);
            });
        } else {
            txList.innerHTML = '<div style="color:var(--text-secondary);font-size:14px;padding:10px;">No expenses yet.</div>';
        }

        // Update deleted transactions list
        const delList = document.getElementById('deleted-list');
        delList.innerHTML = '';
        if (data.deleted_expenses && data.deleted_expenses.length > 0) {
            data.deleted_expenses.slice().reverse().forEach(tx => {
                const el = document.createElement('div');
                el.className = 'list-item deleted-item';
                el.innerHTML = `
                    <div class="info">
                        <span class="item-name">${tx.item}</span>
                        <span class="item-cat">${tx.category}</span>
                    </div>
                    <div class="amount">₹${tx.amount}</div>
                `;
                delList.appendChild(el);
            });
        } else {
            delList.innerHTML = '<div style="color:var(--text-secondary);font-size:14px;padding:10px;">No deleted expenses.</div>';
        }

    } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
    }
}

// Append a message to the chat UI
function appendMessage(role, text) {
    const box = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    
    // Simple markdown formatting (bold, links, line breaks)
    const formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                              .replace(/\n/g, '<br>');
                              
    bubble.innerHTML = formattedText;
    
    msgDiv.appendChild(bubble);
    box.appendChild(msgDiv);
    
    // Auto scroll to bottom
    box.scrollTop = box.scrollHeight;
}

// Handle chat submission
document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    // Add user message to UI
    appendMessage('user', message);
    input.value = '';
    
    // Add temporary loading indicator
    const loadingId = 'loading-' + Date.now();
    const box = document.getElementById('chat-box');
    const loadDiv = document.createElement('div');
    loadDiv.id = loadingId;
    loadDiv.className = 'message assistant typing';
    loadDiv.innerHTML = '<div class="msg-bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
    box.appendChild(loadDiv);
    box.scrollTop = box.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove loading
        document.getElementById(loadingId).remove();
        
        if (data.response) {
            appendMessage('assistant', data.response);
        } else if (data.error) {
            appendMessage('assistant', `*Error:* ${data.error}`);
        }
        
        // Always refresh dashboard after interaction
        fetchDashboard();
        
    } catch (err) {
        document.getElementById(loadingId).remove();
        appendMessage('assistant', "*Sorry, there was an error connecting to the server.*");
        console.error("Chat error:", err);
    }
});

// Initial dashboard load
fetchDashboard();

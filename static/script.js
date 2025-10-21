const messagesDiv = document.getElementById('messages');
const questionInput = document.getElementById('question-input');
const sendBtn = document.getElementById('send-btn');
const statusDiv = document.getElementById('status');
const loadingSpinner = document.getElementById('loading-spinner');

function addMessage(text, isUser, citations = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const textP = document.createElement('p');
    textP.textContent = text;
    messageDiv.appendChild(textP);
    
    if (citations && citations.length > 0) {
        const citationsDiv = document.createElement('div');
        citationsDiv.className = 'citations';
        
        const title = document.createElement('h4');
        title.textContent = '📚 Sources:';
        citationsDiv.appendChild(title);
        
        citations.forEach(citation => {
            const citationDiv = document.createElement('div');
            citationDiv.className = 'citation';
            citationDiv.innerHTML = `[${citation.index}] <strong>${citation.source}</strong> ${citation.snippet}`;
            citationsDiv.appendChild(citationDiv);
        });
        
        messageDiv.appendChild(citationsDiv);
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showLoading() {
    statusDiv.innerHTML = ' Thinking...';
    sendBtn.disabled = true;
    loadingSpinner.style.display = 'inline-block';
}

function hideLoading() {
    statusDiv.innerHTML = '';
    sendBtn.disabled = false;
    loadingSpinner.style.display = 'none';
}

async function sendQuestion() {
    const question = questionInput.value.trim();
    if (!question) return;
    
    addMessage(question, true);
    questionInput.value = '';
    showLoading();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage(data.answer, false, data.citations);
            statusDiv.innerHTML = `Response time: ${data.latency}s`;
            setTimeout(hideLoading, 2000);
        } else {
            addMessage(`Error: ${data.error}`, false);
            hideLoading();
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, false);
        hideLoading();
    }
}

sendBtn.addEventListener('click', sendQuestion);

questionInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') sendQuestion();
});

// Initial system greeting
fetch('/health')
    .then(r => r.json())
    .then(data => {
        if (data.status === 'healthy') {
            addMessage("Hello! I'm your company policy assistant. Ask me anything about our policies!", false);
        }
    })
    .catch(() => {
        addMessage("System initializing, please wait...", false);
    });

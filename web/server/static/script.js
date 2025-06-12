let typingInterval;
const typingIndicator = document.createElement('div');
typingIndicator.className = 'message bot-message typing-indicator';

function showTypingIndicator(isTyping) {
    const chatBox = document.getElementById('chat-box');

    if (isTyping) {
        if (!chatBox.contains(typingIndicator)) {
            chatBox.appendChild(typingIndicator);
            scrollChatToBottom();
        }

        let dots = 0;
        typingInterval = setInterval(() => {
            dots = (dots + 1) % 4;
            typingIndicator.textContent = 'Печатает' + '.'.repeat(dots);
        }, 500);
    } else {
        clearInterval(typingInterval);
        typingIndicator.remove();
    }
}

function scrollChatToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const inputElement = document.getElementById("user-input");
    const messageText = inputElement.value.trim();
    const sessionId = getSessionId();

    if (!messageText) return;

    appendMessage(messageText, 'user-message');
    inputElement.value = '';
    resetTextareaHeight();

    showTypingIndicator(true);

    try {
        const response = await getAIResponse(messageText, sessionId);
        appendMessage(response, 'bot-message');
    } finally {
        showTypingIndicator(false);
    }
}

function generateSessionId() {
    const sessionId = crypto.randomUUID();
    localStorage.setItem('sessionId', sessionId);
    return sessionId;
}

function getSessionId() {
    return localStorage.getItem('sessionId') || generateSessionId();
}

function displaySessionId() {
    const sessionId = getSessionId();
    const sessionElement = document.getElementById("session-id");
    if (sessionElement) {
        sessionElement.textContent = `Сессия: ${sessionId}`;
    }
}

async function redirectUser() {
    const sessionId = getSessionId();
    try {
        await fetch("http://localhost:8000/", {
            method: "GET",
            body: sessionId
        });
    } catch (error) {
        console.error("Ошибка при получении ответа от ИИ:", error);
    }
}

function parseMessages(inputString) {
    const messages = inputString.split('\n\n\n\n\n');
    let flag = 'bot-message';
    
    messages.forEach(message => {
        if (message.trim()) {
            appendMessage(message, flag);
            flag = flag === 'bot-message' ? 'user-message' : 'bot-message';
        }
    });
}

function setupEventListeners() {
    displaySessionId();
    const userInput = document.getElementById('user-input');

    if (userInput) {
        userInput.addEventListener("input", adjustTextareaHeight);
        userInput.addEventListener('keydown', handleKeyDown);
    }
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    } else if (e.key === "Enter") {
        e.preventDefault();
        insertNewLine();
    }
}

function insertNewLine() {
    const userInput = document.getElementById('user-input');
    const { selectionStart, value } = userInput;
    
    userInput.value = `${value.slice(0, selectionStart)}\n${value.slice(selectionStart)}`;
    userInput.selectionStart = userInput.selectionEnd = selectionStart + 1;
    adjustTextareaHeight();
}

async function getAIResponse(userMessage, sessionID) {
    try {
        const response = await fetch("http://localhost:8000/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                message: userMessage,
                id: sessionID
            })
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        return data.response || "Не удалось получить ответ от сервера";
    } catch (error) {
        console.error("Ошибка при получении ответа от ИИ:", error);
        return "Извините, произошла ошибка. Попробуйте еще раз.";
    }
}

function appendMessage(text, className) {
    const chatBox = document.getElementById('chat-box');
    if (!chatBox) return;

    const message = document.createElement('div');
    message.className = `message ${className}`;
    
    message.innerHTML = className === "bot-message" 
        ? marked.parse(text) 
        : document.createTextNode(text).textContent;

    chatBox.appendChild(message);
    scrollChatToBottom();
}

function adjustTextareaHeight() {
    const inputElement = document.getElementById("user-input");
    if (inputElement) {
        inputElement.style.height = "auto";
        inputElement.style.height = `${inputElement.scrollHeight}px`;
    }
}

function resetTextareaHeight() {
    const inputElement = document.getElementById("user-input");
    if (inputElement) {
        inputElement.style.height = "auto";
    }
}

function redirectToSession() {
    if (window.location.pathname === '/') {
        const sessionId = getSessionId();
        window.location.replace(`${window.location.origin}/c/${sessionId}`);
    }
}

document.addEventListener('DOMContentLoaded', setupEventListeners);
window.addEventListener('load', redirectToSession);

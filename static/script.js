const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

const userName = "You";
const botName = "ZEL";

// display messages in the chat box
function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender === 'user' ? 'user' : 'bot');
    
    const messageContent = document.createElement('div');
    messageContent.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    
    const nameElement = document.createElement('strong');
    nameElement.innerText = sender === 'user' ? userName : botName;
    messageContent.appendChild(nameElement);

    const textElement = document.createElement('span');
    textElement.innerText = ": " + message;
    messageContent.appendChild(textElement);

    messageElement.appendChild(messageContent);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        displayMessage(message, 'user');
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = await response.json();
            displayMessage(data.response, 'bot');
        } catch (error) {
            console.error("Error:", error);
            displayMessage("I apologize, but I'm having trouble processing your message right now. Please try again in a moment.", 'bot');
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }
}

function displayWelcomeMessage() {
    const welcomeMessage = "Hello! I'm ZEL, your friendly AI assistant. How can I help you today? 😊";
    displayMessage(welcomeMessage, 'bot');
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Display welcome message when the page loads
window.onload = displayWelcomeMessage;

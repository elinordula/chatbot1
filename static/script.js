document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message === '') return;

    addMessage('user', message);
    userInput.value = '';

    // Send the user message to the backend
    fetch('/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        addMessage('chatbot', data.response);
    });
}

function addMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add(`${sender}-message`);

    const heading = document.createElement('h4');
    heading.textContent = sender === 'user' ? 'User' : 'Chatbot';
    messageElement.appendChild(heading);

    const text = document.createElement('p');
    text.textContent = message;
    messageElement.appendChild(text);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

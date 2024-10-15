const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Function to display messages
function displayMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);

    const profileImg = document.createElement('img');
    profileImg.classList.add('profile-image');
    // Set the source based on the message type
    profileImg.src = type === 'user-message' ? 'D:/Mridula/stud chatbot/stupid/tutorial/image1.jpg' : 'D:/Mridula/stud chatbot/stupid/tutorial/image2.jpg'; // Use your image paths

    const textDiv = document.createElement('div');
    textDiv.textContent = message;

    messageDiv.appendChild(profileImg);
    messageDiv.appendChild(textDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

// Function to handle user input
sendBtn.addEventListener('click', () => {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        displayMessage(userMessage, 'user-message');
        userInput.value = ''; // Clear input field
        // Simulate bot response
        setTimeout(() => {
            displayMessage('This is a simulated response.', 'bot-message');
        }, 1000);
    }
});

// Allow pressing Enter to send message
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});

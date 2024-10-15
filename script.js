const input = document.querySelector('input[type="text"]');
const chatContainer = document.querySelector('.chat-container');

document.querySelector('button').addEventListener('click', sendMessage);

function sendMessage() {
  const messageText = input.value;
  if (messageText.trim() !== "") {
    const newMessage = document.createElement('div');
    newMessage.classList.add('message', 'sent');
    newMessage.innerHTML = `<div class="text">${messageText}</div>`;
    chatContainer.insertBefore(newMessage, document.querySelector('.input-container'));
    input.value = '';
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

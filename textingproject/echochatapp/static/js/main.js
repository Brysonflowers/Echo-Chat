const menuButton = document.getElementById('menu-toggle-btn');
const slideMenu = document.getElementById('nav-bar');

menuButton.addEventListener('click', () => {
    slideMenu.classList.toggle('open');
});

function home_page() {
    document.location.href = "http://127.0.0.1:8000"
}

if (menuToggleButton) {
    menuToggleButton.addEventListener('click', () => {
      // Toggle the 'hidden' class to show/hide the navbar
      navbar.classList.toggle('visisble');
    
      // Alternative using 'visible' class:
      // navbar.classList.toggle('visible');
    });
}

const roomNameElement = document.getElementById('room-name');
if (roomNameElement) {
    const roomName = JSON.parse(roomNameElement.textContent);
    const chatLog = document.querySelector('#chat-log');
    const messageInput = document.querySelector('#chat-message-input');
    const messageSubmit = document.querySelector('#chat-message-submit');

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `<span class="username">${data.username}:</span> <span class="text">${data.message}</span>`;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    messageInput.focus();
    messageInput.onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            messageSubmit.click();
        }
    };

    messageSubmit.onclick = function(e) {
        const message = messageInput.value;
        if (message.trim() !== '') {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        }
    };
}



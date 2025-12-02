document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('menu-toggle-btn');
    const slideMenu = document.getElementById('nav-bar');
    const roomNameElement = document.getElementById('room-name');

    menuButton.addEventListener('click', () => {
        slideMenu.classList.toggle('open');
    });

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

    const privateChatId = JSON.parse(document.getElementById('private-chat-id').textContent);
    const chatLog = document.querySelector('#chat-messages');
    const messageInput = document.querySelector('#chat-message-input');
    const messageSubmit = document.querySelector('#chat-message-submit');

    const ws_url = 'ws://'
        + window.location.host
        + '/ws/private_chat/'
        + privateChatId
        + '/';
    console.log("Connecting to WebSocket at:", ws_url);
    const chatSocket = new WebSocket(ws_url);

    chatSocket.onmessage = function(e) {
        console.log("Message received:", e.data);
        const data = JSON.parse(e.data);
        const messageDiv = document.createElement('div');
        messageDiv.classList = 'message current-user';
        messageDiv.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly. Code:', e.code, 'Reason:', e.reason);
    };

    messageInput.focus();
    messageInput.onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            messageSubmit.click();
        }
    };

    messageSubmit.onclick = function(e) {
        const message = messageInput.value;
        console.log("Sending message:", message);
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    };
})

function home_page() {
    document.location.href = "http://127.0.0.1:8000"
}

function find_user_page() {
    document.location.href = "http://127.0.0.1:8000/echochatapp/private%20chats"
}
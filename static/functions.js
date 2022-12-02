"use strict";
// Establish a WebSocket connection with the server
const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// const socket = new WebSocket(wsProtocol + "://" + location.host + "/websocket/{{ username }}");

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
    if (event.code === "Enter") {
        sendMessage();
    }
});

// Read the comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
function sendMessage() {
    const chatBox = document.getElementById("chat-comment");
    const comment = chatBox.value;

    chatBox.value = "";
    chatBox.focus();
    if (comment !== "") {
        socket.send(JSON.stringify({'Username': 'ChangedByServer', 'comment': comment}));
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage.username + "</b>: " + chatMessage.message + "<br/>";
}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function(ws_message) {
    const message = JSON.parse(ws_message.data)
    addMessage(message)
}

socket.onopen = function(event) {
    console.log("Client connected!");
    socket.send(JSON.stringify({'Username': 'ChangedByServer', 'socketMessage': "connected"}));
}

socket.onclose = function(event) {
    console.log('The connection has been closed successfully.');
    socket.send(JSON.stringify({'Username': 'ChangedByServer', 'socketMessage': "close"}));
}

// Handle any errors that occur.
socket.onerror = function(error) {
    console.log('WebSocket Error: ' + error);
};
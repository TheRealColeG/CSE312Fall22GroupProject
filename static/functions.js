"use strict";

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
        socket.send(JSON.stringify({'messageType': 'chatMessage', 'comment': comment}));
    }
}

// Called whenever data is received from the server over the WebSocket connection
socket.onmessage = function(ws_message) {
    const message = JSON.parse(ws_message.data)
    const messageType = message.messageType

    switch (messageType) {
        case 'chatMessage':
            addMessage(message);
            break; 
        case 'connections':
            reflectConnections(message);
            break;
        case 'boardUpdateRequest':
            updateBoard(message);
            break;
    }
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage.username + "</b>: " + chatMessage.message + "<br/>";
}

// Renders when a new user connect to the page
function reflectConnections(users) { // user is a javascript map/dictionary
    let connection_count = document.getElementById('reflectConnections');
    connection_count.innerHTML = "<b>" + "Users connected" + "</b>: " + users.user_count + "<br/>";
}

// Renders a new board
function updateBoard(new_board) {
    let game_board = document.getElementById('game-board');
    game_board.innerHTML = "<b>" + new_board.board + "</b>"
}

function updateBoardRequest() {
    socket.send(JSON.stringify({'boardUpdateRequest': "game_board_update_request"}));
}

socket.onopen = function(event) {
    console.log("Client connected!");
    socket.send(JSON.stringify({'socketMessage': "connected"}));
}

window.onbeforeunload = function() {
    socket.send(JSON.stringify({'socketMessage': "close"}));
}

// Handle any errors that occur.
socket.onerror = function(error) {
    console.log('WebSocket Error: ' + error);
};
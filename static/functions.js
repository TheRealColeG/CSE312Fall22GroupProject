"use strict";
let test = "wss";
if (window.location.protocol === "http:") {
    test = "ws";
    console.log(window.location.protocol)
}

const socket = new WebSocket(test + "://" + location.host + '/websocket');

// const socket = new WebSocket(wsProtocol + "://" + location.host + "/websocket/{{ username }}");
console.log("HOST:" + window.location.host)
console.log("WINDOW: " + test + "://" + window.location.host + '/websocket')
console.log("NOT WINDOW: " + test + "://" + location.host + '/websocket')

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
        case 'DisplayBoard':
            DisplayBoard(message);
            break;
    }

    return false;
}

// Renders a new chat message to the page
function addMessage(chatMessage) {
    let chat = document.getElementById('chat');
    chat.innerHTML += "<b>" + chatMessage.username + "</b>: " + chatMessage.message + "<br/>";
}

// Renders when a new user connect to the page
function reflectConnections(users) { // user is a javascript map/dictionary
    let count = 4
    let connection_count = document.getElementById('reflectConnections');
    let user_acc = users.user_count % count == 0 ? users.user_count % count + count : users.user_count % count;
    connection_count.innerHTML = "<b>" + "Users connected" + "</b>: " + user_acc + "<br/>";
    let game_board = document.getElementById('game-board');
    if (users.user_count % count == 0) {
        socket.send(JSON.stringify({'DisplayBoard': 'OpenGame'}));
    }
    else if (users.user_count <= count) {
        game_board.innerHTML = "<b>" + "Waiting for enough players..." + "</b>"
    }
    return false;
}

// Renders a new board
function DisplayBoard(new_board) {
    let game_board = document.getElementById('game-board');
    game_board.innerHTML = "<b>" + new_board.board + "</b>"
}

socket.onopen = function(event) {
    console.log("Client connected!");
    socket.send(JSON.stringify({'socketMessage': "connected"}));
    return false;
}

socket.onclose = function(event) {
    console.log("Client disconnected!");
    socket.send(JSON.stringify({'socketMessage': "close"}));
}

window.addEventListener("beforeunload", function(event) {
    socket.send(JSON.stringify({'socketMessage': "close"}));
  });

// Handle any errors that occur.
socket.onerror = function(error) {
    console.log('WebSocket Error: ' + error);
    return false;
};

//User pressed roll
function roll() {
    socket.send((JSON.stringify({'button_type': 'roll'})));
    return false;
}

//User wants to buy current property
function buy() {
    socket.send((JSON.stringify({'button_type': 'buy'})));
    return false;
}

//User does NOT want to buy current property
function pass() {
    socket.send((JSON.stringify({'button_type': 'pass'})));
    return false;
}

//User wants to leave game (i.e. remove their websocket connection quietly)
function leave() {
    console.log("Client disconnecting!");
    socket.close()
}
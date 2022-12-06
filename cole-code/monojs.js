const socket = new WebSocket('ws://' + window.location.host + '/websocket')

//User pressed roll
function roll() {
    socket.send((JSON.stringify({'type': 'roll'})));
}

//User wants to buy current property
function buy() {
    socket.send((JSON.stringify({'type': 'buy'})));
}

//User does NOT want to buy current property
function pass() {
    socket.send((JSON.stringify({'type': 'pass'})));
}

//User wants to leave game (i.e. remove their websocket connection quietly)
function leave() {
    socket.close()
}
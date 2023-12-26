const socket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(data.message);
};

function sendMessage(message) {
    socket.send(JSON.stringify({
        'message': message
    }));
}
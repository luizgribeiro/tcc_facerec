const socket = io('http://localhost:5000');

socket.on('connect', ()=> {
  console.log("Conexão websocket estabelecida");
})

const frameSender = new FrameSender(socket);
attendanceUpdate(socket)
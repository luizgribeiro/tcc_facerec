const socket = io('woody', {path:'/apifacerec/socket.io'});

socket.on('connect', ()=> {
  console.log("Conexão websocket estabelecida");
})

const frameSender = new FrameSender(socket);
attendanceUpdate(socket)

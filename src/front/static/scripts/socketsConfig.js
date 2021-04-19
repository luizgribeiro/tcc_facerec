

const socket = io('http://localhost:5000');

socket.on('connect', ()=> {
  console.log("Conectado");
})

const frameSender = new FrameSender(socket);
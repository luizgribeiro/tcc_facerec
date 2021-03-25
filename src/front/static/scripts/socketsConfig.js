

const socket = io('http://localhost:5000');

socket.on('connect', ()=> {
  //socket.emit('raw_frame', {"oi": "Tchau"});
  console.log("Envio de msgs");
})

const frameSender = new FrameSender(socket);
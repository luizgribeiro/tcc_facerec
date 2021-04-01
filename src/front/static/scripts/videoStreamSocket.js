class FrameSender {
  constructor (ioSocket) {
    this._ioSocket = ioSocket;
    this.video = document.querySelector('video');
    this.screenShoter = document.createElement('canvas');
    enableVideoStream();
    this.setSocketHander();
  }

  setSocketHander() {
    this._ioSocket.on('processed_frame', (procFrame)=>{
      this.sendFrame();
      const enc = new TextDecoder("utf-8");
      const frameB64String = enc.decode(procFrame.data);
      document.getElementById("ItemPreview").src = `data:image/jpeg;charset=utf-8;base64,${frameB64String}`;
    });

    this._ioSocket.on('broken_frame', (procFrame)=>{
      this.sendFrame();
    });
  }

  sendFrame() {
    this._ioSocket.emit('raw_frame', JSON.stringify(this.generateFrame()));
  }

  generateFrame() {
      this.screenShoter.width = this.video.videoWidth;
      this.screenShoter.height = this.video.videoHeight;
      this.screenShoter.getContext("2d").drawImage(this.video, 0, 0);
      
      
      return { image_data: this.screenShoter.toDataURL("image/jpg") };
    };
  }

  //abre conexão websocket
  //de tempos em tempos "tira print" do vídeo
  //envia imagem via socket

  /*
  function attendanceUpdate() {
    var socket = io();

    socket.on('connect', function() {
        setInterval(()=>{
            socket.emit('update_atendences');
        }, 1000);
        
    });

    socket.on("updated_list", (data)=> {
        
        newlyDetected = [];
        currentStudents = getAttendanceList();

        for (let student of data.faces) {
            if (currentStudents.indexOf(student) == -1) {
                newlyDetected.push(student);
            }
        }
        let attendanceList = document.querySelector('#lista-presentes');
        for (let face of newlyDetected) {
            let student = document.createElement("li");
            student.innerText = face;
            student.classList.add("text-light");
            attendanceList.appendChild(student);
        }
    });

  


}

*/

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
      
      
      return { image_data: this.screenShoter.toDataURL("image/jpg"),
        socket_id : this._ioSocket.id};
    }
  }
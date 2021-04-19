const videoCaptureSetup = () => {
    const screenshotButton = document.getElementById("capture-btn");
    const restartVideoButton = document.getElementById("restart-video");
    const img = document.querySelector("img");
    const video = document.querySelector("video");
    const canvas = document.createElement("canvas");
    
    const constraints = {
    video: true,
    };

    (() =>  {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(handleSuccess)
        .catch(handleError);
    })();

    screenshotButton.onclick = video.onclick = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        video.style.display = "none";
        img.style.display = "";
        img.src = canvas.toDataURL("image/png");
        
        screenshotButton.disabled = true;
        restartVideoButton.disabled = false;
 
    }

    restartVideoButton.onclick = () => {
        video.style.display = "";
        img.style.display = "none"
        screenshotButton.disabled = false;
        restartVideoButton.disabled = true;
    }

    function handleSuccess(stream) {
        screenshotButton.disabled = false;
        video.srcObject = stream;
    }

    function handleError(err) {
        console.log(err);
        //TODO: implementar notificação de na ausência de dispostitivo de captura
    }
    
}

videoCaptureSetup();
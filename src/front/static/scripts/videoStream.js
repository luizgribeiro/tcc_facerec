const enableVideoStream = () =>  {

  const constraints = {
    video: true,
  }

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(handleSuccess)
    .catch(handleError);
}

const handleSuccess = (stream)  => {
  const video = document.querySelector('video');
  video.srcObject = stream;
}

const handleError = (error) => {
  console.log(error);
}


/*
const screenshotButton = document.querySelector("button");
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
  // Other browsers will fall back to image/png
  img.src = canvas.toDataURL("image/webp");
  console.log(img.src);
  fetch('http://localhost:5000/', {
    method: 'POST',
        headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "image_data": canvas.toDataURL("image/jpg")
    })
  }).then(response => console.log("Ok"))
    .catch(err => console.log(`Req error: ${err}`));
};

function handleSuccess(stream) {
  video.srcObject = stream;
}

function handleError(err) {
  console.log(err);
}
*/
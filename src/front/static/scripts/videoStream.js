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
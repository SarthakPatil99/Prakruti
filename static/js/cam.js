`use strict`;
const snapshot = document.getElementById("snapshot");
const canvas = document.getElementById("canvas");
const video = document.getElementById("video");
const errorMessage = document.getElementById("span#ErrorMessage");

const constraints = {
  audio: false,
  video: {
    width: 480,
    height: 360,
  },
};
async function init() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    errorMessage.innerHTML = `navigator.getUserMedia.errror:${e.toString()}`;
  }
}

function handleSuccess(stream) {
  window.stream = stream;
  video.srcObject = stream;
}

init();

var context = canvas.getContext("2d");
snapshot.addEventListener("click", function () {
  context.drawImage(video, 0, 0, 480, 360);
});

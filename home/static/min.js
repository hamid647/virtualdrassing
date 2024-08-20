const toTop = document.querySelector(".to-top");

window.addEventListener("scroll",() =>{
    if (window.pageYOffset > 120) {
        toTop.classList.add("active");
    }
    else{
        toTop.classList.remove("active");
    }
})





var MainImg = document.getElementById('MainImg');
          var smallimg = document.getElementsByClassName('small-img');

          smallimg[0].onclick = function() {
            MainImg.src = smallimg[0].src;
          }

          smallimg[1].onclick = function() {
            MainImg.src = smallimg[1].src;
          }

          smallimg[2].onclick = function() {
            MainImg.src = smallimg[2].src;
          }

          smallimg[3].onclick = function() {
            MainImg.src = smallimg[3].src;
          }

          // get the start
          const startWebcamButton = document.getElementById("start-webcam-button");
          const webcam = document.getElementById("webcam");
          startWebcamButton.addEventListener("click",() =>{
            navigator.mediaDevices.getUserMedia({video: true})
            .then(stream =>{
              webcam.srcObject= stream;

            })
            .catch(error => {
              console.error("Error accessing webcam:", error);
            });
          });



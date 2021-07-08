let time = 4050,
    currentImageIndex = 0,/* imagem do momento */
    images = document.querySelectorAll("#slider img")
    max = images.length;
 
function nextImage() {
    images[currentImageIndex].classList.remove("selected")
    currentImageIndex++
    if(currentImageIndex >=max)
        currentImageIndex=0
        images[currentImageIndex].classList.add("selected")
}

function start(){
    setInterval(()=>{
        nextImage()

    },time)
}

window.addEventListener("load",start)/* quando for carregado */
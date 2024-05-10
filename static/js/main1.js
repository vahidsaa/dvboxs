const mywrapper = document.querySelector(".mywrapper");
const mycarousel = document.querySelector(".mycarousel");
const arrowBtns = document.querySelectorAll(".mywrapper i");
const firstCardWidth = mycarousel.querySelector(".mycard").offsetWidth;
const carouselChilderens = [...mycarousel.children];


var isDragging = false, startX, startScrollLeft, timeoutId;

var cardPerView = Math.round(mycarousel.offsetWidth / firstCardWidth);


carouselChilderens.slice(-cardPerView).reverse().forEach(card => {
    mycarousel.insertAdjacentHTML("afterbegin", card.outerHTML);
});
carouselChilderens.slice(0, cardPerView).reverse().forEach(card => {
    mycarousel.insertAdjacentHTML("beforeend", card.outerHTML);
});


arrowBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        mycarousel.scrollLeft += btn.id === "myleft" ? -firstCardWidth : firstCardWidth;
    });
});


const dragStart = (e) => {
    isDragging = true;
    mycarousel.classList.add("dragging");
    startX = e.pageX;
    startScrollLeft = mycarousel.scrollLeft;
}

const dragging = (e) => {
    if(!isDragging) return;
    mycarousel.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
    isDragging = false;
    mycarousel.classList.remove("dragging");
}

const autoPlay = () => {
    if(window.innerWidth < 800) return;
    //autoplaye in 2500ms
    timeoutId = setTimeout(() => mycarousel.scrollLeft += firstCardWidth, 2500);

}
autoPlay();

const infiniteScroll = () => {
    if(mycarousel.scrollLeft === 0) {
        mycarousel.classList.add("no-transition");
        mycarousel.scrollLeft = mycarousel.scrollWidth - (2 * mycarousel.offsetWidth);
        mycarousel.classList.remove("no-transition");

    
    } else if(Math.ceil(mycarousel.scrollLeft) === mycarousel.scrollWidth -mycarousel.offsetWidth){
        mycarousel.classList.add("no-transition");
        mycarousel.scrollLeft = mycarousel.offsetWidth;
        mycarousel.classList.remove("no-transition");

    }
    //start autoplay again
    clearTimeout(timeoutId);
    if(!mywrapper.matches(":hover")) autoPlay();
}


mycarousel.addEventListener("mousedown", dragStart);
mycarousel.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
mycarousel.addEventListener("scroll", infiniteScroll);
mywrapper.addEventListener("mouseenter", () => clearTimeout(timeoutId));
mywrapper.addEventListener("mouseleave", autoPlay);




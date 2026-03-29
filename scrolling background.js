
var street_image;
/*used for position x of the image*/
var streetX = 0;

function preload() {
    street_image = loadImage("background.png")
}

function setup() {
    createCanvas(400,400)
}

function draw() {
  /*drawing two panels of background*/
  image(street_image, streetX, 0)
  image(street_image, streetX + street_image.width, 0)
  /*positionX of background decreases*/
  streetX --;
  /*if the first panel goes offscreen left, it is reset*/
  if (streetX < -width) {
    mountainsX = 0
  }
}

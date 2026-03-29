
let shots;

function preload() {
    shot_image = loadImage("shot.png");
}

function setup() {
    createCanvas(400,400)
    /*create new sprite group*/
    shots = new Group;
      /*this just creates a shot offscreen to prevent error because the sprite must be declared before the player shoots*/
      shot = createSprite(-50, -50);
      shot.remove();
}

function key_released() {
  if (keyCode === 32) {
    shot = createSprite(player.position.x, player.position.y);
    shot.addImage("normal", shot_image);
    shot.setSpeed(4);
    shots.add(shot);
  }
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

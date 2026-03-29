
var sprite_sheet;
var dog_animation;

function preload() {
    /*                                            first two numbers are dimensions of each frame, then your number of frames*/
    sprite_sheet = loadSpriteSheet('./assets/dog_spritesheet.png', 296, 355, 2)
    dog_animation = loadAnimation()
}

function setup() {
    createCanvas(400,400)
}

function draw() {
    clear()
                            /*position on screen*/
    textAlign(CENTER)
    text('test', width/2, height/2)
    animation(dog_animation, 200, 200)
}
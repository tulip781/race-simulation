<template>
  <div id="canvas"></div>
</template>

<script>
import P5 from 'p5';
export default {
  name: 'RaceTrack',
  props: {
    onOff: Boolean,
  },
  data() {
    return {

    };
  },
  mounted() {
    const sketch = (p5) => {
      // These are your typical setup() and draw() methods
      /* eslint-disable no-param-reassign */
      class Ball {
        constructor() {
          this.x = width/2;
          this.y = 150;
          this.vx = 0;
          this.vy = 0;
          this.size = 20;
          this.pulled = false;
          this.fired = false;
          this.c = p5.color(255, 204, 0);
          this.distance = 0;
          this.mass = 50;

          this.lastX = 0;
          this.lastY = 0;
          this.angle = 0;
        }


        setColor (){
          // Sets ball colour depending on if ball clicked
          this.pulled ? this.c = p5.color(255, 204, 110) : this.c = p5.color(0,62,116);
        }

        display() {
          // Set ball colour
          this.setColor();
          // Set up ball colour and styles with this ball colour
          p5.fill(this.c);
          p5.noStroke();
          // Draws ellipse using X,Y, and size variables
          p5.imageMode(p5.CENTER);
          // p5.rotate(this.angle)
          p5.image(img, this.x, this.y, this.size, this.size*1.4);
          // p5.ellipse(this.x, this.y, this.size * 2);
          // Changes colour to black for text
          p5.fill(p5.color(0, 0, 0));
          // Displays the ball mass on top of the ball
          p5.text( p5.round(ball.mass, 2) + "kg", ball.x +50 , ball.y -10);
        }

        clicked() {
          // Test to see if ball is clicked
          if ( p5.dist(p5.mouseX, p5.mouseY, this.x, this.y) < this.size) {
            // Set the pulled variable to true if it is clicked
            this.pulled = true;
          }
          // Otherwise return false as the ball is not clicked
          return false;
        }

        update () {
          // Test to see if ball is dragged
          if (this.pulled) {
            if (p5.dist(p5.mouseX, p5.mouseY, this.x, this.y) < 2 * this.size ) {
              this.x = p5.constrain(p5.mouseX, canvasDiv.offsetWidth / 3.5, canvasDiv.offsetWidth / 1.4);
              this.y = p5.constrain(p5.mouseY, 300, 399);
            }
          }

          if (this.fired && this.y !== (300)){


            //Velocity in Y Axis
            this.vy += g;
            // Positon - Velocity in Y and Mass
            this.y -= this.vy / this.mass

      //        Velocity X Axis
            if (this.vx === 0) {
              this.vx = canvasDiv.offsetWidth / 2 - this.x;
              console.log(this.vx);
            }

            this.x += this.vx / this.mass

            // update rotation

            let v1 = p5.createVector(this.lastX, this.lastY, 0);
            let v2 = p5.createVector(this.x, this.y, 0);

            this.angle = p5.degrees(v1.angleBetween(v2));
            // angle is PI/2


            this.lastX = this.x
            this.lasyY = this.y
            if (this.y > 300){
              this.y = 300;
              setTimeout(resetSketch, 500);
            }
          }
        }

      }
      // Catpult Still
      class Rope {
        constructor(b){
          this.ballx = b.x;
          this.bally = b.y;
          this.post1 = canvasDiv.offsetWidth / 3.5;
          this.post2 = 150;
          this.post3 = canvasDiv.offsetWidth / 1.4;
          this.post4 = 150;
        }

        update () {

        }

        display (b) {
          if (b.y < initY  ) {
      //       Draw Straight Line
            p5.fill(0);
            p5.stroke(126);
            p5.line(this.post1, this.post2, this.post3, this.post4);
            p5.ellipse(this.post1, this.post2, 7, 7);
            p5.ellipse(this.post3, this.post4, 7, 7);
          } else if (b.fired && b.vy < 0) {
              p5.fill(0);
              p5.stroke(126);
              p5.line(this.post1, this.post2, this.post3, this.post4);
              p5.ellipse(this.post1, this.post2, 7, 7);
              p5.ellipse(this.post3, this.post4, 7, 7);
          }
            else       {
            p5.fill(0);
            p5.stroke(126);
      //     First String
            p5.line(b.x, b.y, this.post1, this.post2);
            p5.ellipse(this.post1, this.post2, 7, 7);
      //     Second String
            p5.line(b.x, b.y, this.post3, this.post2);
            p5.ellipse(this.post3, this.post4, 7, 7);
          }

        }
      }

      class Tracer {
        constructor () {
          this.dots = []
        }

        display(b){
          if (b.fired){
            let xdot = b.x;
            let ydot = b.y;
            this.dots.push([xdot, ydot]);
            this.dots.forEach(d => {
              p5.ellipse(d[0], d[1], 2);

            })
          } else {
            return
          }
        }
      }

      // Canvas size constants

      // Init ball positon & size constants
      const initY = 150;

      // Physics constants
      const g = -9.80;

      // Initialize the Variables

      let slider;
      let ball;
      let rope;
      let tracer;
        let width;
        let canvasDiv;
      let img;
      p5.preload = () => {
        img = p5.loadImage(require('@/assets/rocket.png'));
      }
      p5.setup = () => {
         // Create canvas and set frame rate
        canvasDiv = document.getElementById('canvas');
        width = canvasDiv.offsetWidth;
        p5.createCanvas(width, 300);
        p5.frameRate(200);



        ball = new Ball ( );
        ball.x = canvasDiv.offsetWidth /2;
        ball.y = initY;
        rope = new Rope (ball);
        tracer = new Tracer (ball)
        p5.line(30, 20, 85, 75);
        let button = p5.createButton("Reset Catapult");
        button.position(10,10);
        button.mousePressed(resetSketch);

        slider = p5.createSlider(1, 20, 10, 1);
        slider.position(10, 40);
        slider.style('width', '100px');

      };
      p5.draw = () => {

        p5.background(212,239,252);
        p5.text( 'Rocket Mass = ' + slider.value() + ' kg' , 120, 55);
        ball.update();
        rope.display(ball);
        tracer.display(ball);
        ball.display();
        p5.fill(p5.color(0,0,0));
        p5.text( 'Rocket Velocity = ' + p5.round(ball.vy, 2), 10, 90);
        ball.mass = slider.value();
        ball.size = p5.map(slider.value(), 1, 20, 50, 120);
      };

      p5.mousePressed = () => {
        if (ball.clicked()) {
          ball.pulled = true;
          ball.fired = false;
        }
      }

      p5.mouseReleased = () => {
        if (ball.pulled) {
          // ball.vy = dist(200, 200, ball.x, ball.y);
          ball.vy = (ball.y - initY) * 2.5;
          ball.pulled = false;
          ball.fired = true;
        }
      };

      function resetSketch(){
        ball.x = canvasDiv.offsetWidth /2 ;
        ball.y = initY;
        ball.pulled = false;
        ball.fired = false;
        ball.vy = 0;
        ball.vx = 0;
        tracer.dots = [];
        ball.update();
        rope.display(ball);
        tracer.display(ball);
        ball.display();
      }

      p5.windowResized = () =>{
        p5.resizeCanvas(canvasDiv.offsetWidth, 300);
      }
    };
    // Attach the canvas to the div
    /* eslint-disable no-new */
    new P5(sketch, 'canvas');
  },
};
</script>

<style>
#canvas {
width: 100%;
  top: 0;
  left: 0;
}
</style>
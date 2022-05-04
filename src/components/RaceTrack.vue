<template>
  <div id="canvas"></div>
</template>

<script>
import P5 from 'p5';
export default {
  name: 'RaceTrack',
  props: {
    onOff: Boolean,
    carCompletion:{
      type: Number,
      deafault: 0,
    }
  },
  data() {
    return {

    };
  },
  mounted() {
    const sketch = (p5) => {
      // These are your typical setup() and draw() methods
      /* eslint-disable no-param-reassign */
      
      // Catpult Still

      class Track {
          constructor(){
              this.width = width;
              this.height= 200;
              this.x = 0;
              this.y = 0;
          }
          display( ){
              p5.fill(190, 190, 190);
              p5.rect(100, 100/4, canvasDiv.offsetWidth -200, 50);
              p5.fill(255,255,255);
      
             
              for(let i=0; i <= ( canvasDiv.offsetWidth -235)/2; i+= 30){
                  console.log("This loop is called", canvasDiv.offsetWidth -200 )
                   p5.rect(100 + 2*i, 100/2 -3, 30, 6);
                   }
            }
          update(){
               p5.rect(100, 20, canvasDiv.offsetWidth -200, 50);
          }
      }
      


      // Canvas size constants


        let width;
        let canvasDiv;
        let track;
      let img;
      p5.preload = () => {
        img = p5.loadImage(require('@/assets/rocket.png'));
      }
      p5.setup = () => {
         // Create canvas and set frame rate
        canvasDiv = document.getElementById('canvas');
        width = canvasDiv.offsetWidth;
        p5.createCanvas(width, 100);
        p5.frameRate(200);

        track = new Track ();


      };

      function placeCar(completion, trackStart, carWidth){
        // Place at start of track
        let posStart = trackStart - carWidth/2;
        let trackLength = canvasDiv.offsetWidth -200;
        let posEnd = posStart + trackLength*completion
        return posEnd
      }
      p5.draw = () => {

        p5.background(255,255,255);
        track.display();
        console.log("this track Completion ", this.carCompletion)
        p5.image(img, placeCar(this.carCompletion, 100, 50), 100/4, 50, 50)
      };




      p5.windowResized = () =>{
        p5.resizeCanvas(canvasDiv.offsetWidth, 100);
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
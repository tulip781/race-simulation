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
      default: 0,
    },
    speed: {
      type: [],
      default: []
    },
     acceleration: {
      type: [],
      default: []
    }
  },
  data() {
    return {
   iterationValue: 0,
    };
  },
  watch:{
    carCompletion: function(newVal, oldVal){
      if(newVal<oldVal){
        this.iterationValue = 0;
      }
    }
  },
  computed: {
    sixtyAcc(){
      let valsAcc = [];
      let valsVel = [];
      if(!this.acceleration){
        return {}
      }

      for (let i = 0; i < this.acceleration.length; i = i +27){
        valsAcc.push(this.acceleration[i]);
        valsVel.push(this.speed[i]);
      }
      let sumAcc = valsAcc.reduce((partialSum, a) => partialSum + a, 0);
      let sumVel = valsVel.reduce((partialSum, a) => partialSum + a, 0);
      let totalDistVelAcc = sumAcc + sumVel;

     let sum = valsAcc.map(function (num, idx) {
        return num + valsVel[idx];
        });
        let ollie = this;

      let sumRemapped = sum.map((item)=>{
   
        return ollie.scale(item, 0, sum[sum.length -1 ], 0, 1);
       
      });
      return {valsAcc, valsVel, totalDistVelAcc, sum, sumRemapped}
    }
  },
  methods: {
    scale: function(number, inMin, inMax, outMin, outMax) {
      return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
    },
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
            
                   p5.rect(100 + 2*i, 100/2 -3, 30, 6);
                   }
            }
          update(){
               p5.rect(100, 20, canvasDiv.offsetWidth -200, 50);
          }
      }
      


      // Canvas size constants

      let completionOllie = 0;
        let width;
        let canvasDiv;
        let track;
      let img;
      let ollieVue = this;

    
  
      p5.preload = () => {
        img = p5.loadImage(require('@/assets/racecar2.png'));
      }
      p5.setup = () => {
         // Create canvas and set frame rate
        canvasDiv = document.getElementById('canvas');
        width = canvasDiv.offsetWidth;
        p5.createCanvas(width, 100);
        p5.frameRate(60);
  
        track = new Track ();


      };
      function* calcCompletion() {
 
        if (!ollieVue.speed){
          completionOllie = 0;
          return completionOllie
        }
        while(ollieVue.iterationValue < ollieVue.sixtyAcc.sumRemapped.length){
   
          ollieVue.iterationValue = ollieVue.iterationValue + 1;
       
          yield completionOllie= ollieVue.sixtyAcc.sumRemapped[ollieVue.iterationValue]

        }
       
    return

      }
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
        if(ollieVue.iterationValue < 185 ){
          calcCompletion().next();}

        p5.image(img, placeCar(completionOllie, 100, 100), 100/4, 50, 50)
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
<template>
  <div id="app">
    <div class="header">
      <img src="./assets/imp.svg.png" class="logo" />
      <div class="header__titles">
        <h1>Kart Transmission Lab Materials</h1>
        <h2>MECH40007 - Design and Manufacture</h2>
      </div>
    </div>
  <p class="left-align">The purpose of the tool is to help students intuitively understand the effects of various transmission
and vehicle parameters (most importantly the Gear Ratio) on the performance of a kart. </p>


    <div class="simulation"><h2>Drag Race Simulation</h2><RaceTrack :carCompletion="tweenedRaceCompletion" :acceleration="results.acc" :speed="results.speed"/></div>

      <h5>Time taken to travel {{this.distance}} Meters = {{this.timeToTravel}}S</h5>

    <div class="panel-layout">
            <div class="simulation-inputs">
        <h1>Simulation inputs</h1>
        <p class="left-align"> Update the inputs below, then press Race to see the effect on the Go Kart. </p>

      <table class="table-inputs">
          <tr>
            <th>Race Distance</th>
            <td><input type="text" id="distance" :placeholder="distance" v-model="distance"></td>
            <td> <span class="units">m</span></td>
          </tr>
        <tr>
          <th>Number of Teeth on Gear 1 (Driving Gear, Sprocket Gear), <img class="latex__formatting" src="./assets/equation2.svg"></th>
          <td><input type="text" id="gearRatio" :placeholder="G1" v-model="G1"></td>
          <td><span class="units">Teeth</span></td>
        </tr>
        <tr>
          <th>Number of Teeth on Gear 2 (Driving Gear, Sprocket Gear), <img class="latex__formatting" src="./assets/equation3.svg"></th>
          <td><input type="text" id="gearRatio" :placeholder="G2" v-model="G2"></td>
          <td><span class="units">Teeth</span></td>
        </tr>
        <tr>
          <th>Modification, <img class="latex__formatting" src="./assets/equation.svg"></th>
          <td>{{GR}}</td>
          <td></td>
        </tr>
        <tr>
          <th>Mass of Kart + Driver</th>
          <td><input type="text" id="massKD" :placeholder="m" v-model="m"></td>
           <td><span class="units">kg</span></td>
        </tr>
        <tr>
          <th>Coefficient of Drag</th>
          <td><input type="text" id="Cd" :placeholder="Cd" v-model="Cd"></td>
          
        </tr>
        <tr>
          <th>Frontal Area</th>
          <td><input type="text" id="A" :placeholder="A" v-model="A"></td>
          <td><span class="units">m<sup>2</sup></span></td>
        </tr>
        <tr>
          <th>Wheel Radius</th>
          <td><input type="text" id="wheelr" :placeholder="wheelr" v-model="wheelr"></td>
          <td><span class="units">m</span></td>
        </tr>
        <tr>
          <th>Mass Factor</th>
          <td><input type="text" id="lm" :placeholder="lm" v-model="lm"></td>
        </tr>
        <tr>
          <th>Density of Air</th>
          <td><input type="text" id="rho" :placeholder="rho" v-model="rho"></td>
          <td><span class="units">kg/m<sup>3</sup></span></td>
        </tr>
        <tr>
          <th>Total Drive Train Efficiency  (not including clutch) (constant)</th>
          <td><input type="text" id="tEff" :placeholder="tEff" v-model="tEff"></td>
        </tr>
      </table>
      <button @click="raceKart" class="race-button" v-bind:class="{ active: race, reset: !race,  }">
        <p v-if="!race"> Race Kart</p>
        <p v-else class="calc-button"> {{buttonMessage}}  <span v-html="rawHtml"></span></p>
      </button>
      <button @click="resetValues" class="reset-values" v-bind:class="[{ active: race, reset: !race , },buttonStyle]">
        <p> Reset Parameters </p>
      </button>
    </div>
      <div class="left-wrap">
        <h1>Graph Results</h1>
        <p class="left-align">Below are the resulting graphs from the given inputs. You can use the buttons above each graph to download it as a PNG.</p>
        <div class="graph-grid">
        <GraphOne class="graph1" :gr="GR" :speed="results.speed" :time="results.time"></GraphOne>
        <GraphTwo class="graph2" :time="results.time" :fr="results.Fr" :fd="results.Fd" :ft="results.Ft"></GraphTwo>
        <GraphThree class="graph3" :time="results.time" :acc="results.acc"></GraphThree>
        <GraphFour class="graph4" :time="results.time" :w1="results.w1" :w2="results.w2" :enginerpm="results.enginerpm"></GraphFour>
        </div>
      </div>

</div>

    
  </div>
</template>

<script>
import GraphOne from "./components/GraphOne.vue";
import GraphTwo from "./components/GraphTwo.vue";
import GraphThree from "./components/GraphThree.vue";
import GraphFour from "./components/GraphFour.vue";
import RaceTrack from "./components/RaceTrack.vue";

import everpolate from "everpolate";
import _ from "lodash";


import gsap from "gsap";
export default {
  name: "App",
  title: "Dimensional Graph",
  components: {
    GraphOne,
    GraphTwo,
    GraphThree,
    GraphFour,
    RaceTrack,

  },
  data:function(){
    return {
      // raceCompletion must be decimal between 0-1
      buttonMessage: "Reset Race",
      buttonStyle: {
        'backgroundColor': 'green'
      } ,
      raceCompletion: 0, 
      rawHtml: "",
      tweenedRaceCompletion: 0,
      race: false,
      m: 96.5 +85,
      g: 9.81,
      p:2.48211,
      Cd: 0.5,
      A:0.4,
      wheelr: 0.2794/2,
      G1: 20,
      G2: 71,
      rho: 1.23,
      distance: 500,
      dt:0.01,
      tend: 50,
      engagedSpeed: 2000,
      tEff: 0.93,
      rpm: [2000, 2600, 3000, 3500, 4000, 5000, 6000, 6200, 6960],
      drpm: 1,
      results: {
        time: null,
        enginerpm: null,
        speed: null,
        acc: null,
        dist: null,
        timeDist: null,
        firstIndex: null,
        w1: null,
        w2: null,
        Fr: null,
        Fd: null,
        Ft: null
      }
    }
  },

  computed: {
    allProperties: function(){
      return `${this.m}|${this.g}|${this.p}|${this.Cd}|${this.A}|${this.wheelr}|${this.G1}|${this.G2}|${this.rho}|${this.distance}|${this.dt}|${this.tend}|${this.engagedSpeed}|${this.dt}|`
    },
    timeToTravel: function(){
      let val = 0;
      if(    this.results.timeDist){
         val = this.results.timeDist.toFixed(2)
      }

      return val
    },
    GR: function(){
      return this.G2/this.G1
    },
    lm: function(){
      return  1 + 0.04 + 0.0025*(this.GR**2)
    },
     parameters: function(){ 
       return {'m': this.m, 'g': this.g, 'p': this.p, 'Cd': this.Cd, 'A': this.A, 'wheelr': this.wheelr, 'lm': this.lm, 'rho': this.rho,
              'engagedSpeed': this.engagedSpeed, 'tEff': this.tEff}
    },
    trq: function(){
      let b = [5.0, 13.8, 15.0, 14.0, 13.0, 10.35, 7.0, 6.0, 1.0] ;
      b.forEach((i, index) => b[index] = 2*i);
      b.forEach((i, index) => b[index] = 1.03*i)
    return b
    },
    minrpm: function(){
      return this.rpm[0];
    },
    maxrpm: function(){
      return this.rpm[-1];
    },
    irpm: function(){
      let  arrangeResult = []
      for(let i = this.minrpm; i < this.maxrpm; i+= this.drpm ){
          arrangeResult.push(i);
      }
      return arrangeResult
    },
    t: function(){
        return  _.range(0, this.tend+ this.dt, this.dt)
    },
        
  },
  methods: {
    sayHello(){
      console.log("HELLOOO LOADER")
    },
      raceKart(){
      this.race = !this.race;
        this.buttonMessage = "CALCULATING";
        // this.$nextTick().catch(console.log("Ollie this doesnt work"));
        // console.log("Ollie, next tick has happened", this.buttonMessage)
    
      if(this.race){
        this.buttonMessage = "CALCULATING";
        this.rawHtml = `<div class="lds-ring"><div></div><div></div><div></div><div></div></div>`
        this.buttonStyle.backgroundColor = "orange";
        setTimeout(()=>{
          this.simulate(this.GR, this.t, this.parameters, this.distance);
          this.rawHtml = ``;
          this.buttonMessage = "Reset Race";
          this.buttonStyle.backgroundColor = "red";
          this.raceCompletion = 1;
        },100)

      } else {
        this.raceCompletion = 0;
        this.timeToTravel = 0;
        Object.keys(this.results).forEach(key => {
          this.results[key] = null;
        })
      }
    },
    simulate: function(GR, t, parameters, distance, initialVel = 0) {
      let v, c, Fr, Fd, Ft, a, d,w1, w2, eng, maxRpm, Teng, Tout, alpha, newEngSpeed, km, gs;
      let timeDist = null;
      let firstindex;
      let startingArray = []
      for (let i = 0; i < t.length; i++){
          startingArray.push(0)
      }
      v= [...startingArray]; 
      c= [...startingArray]; 
      Fr= [...startingArray]; 
      Fd= [...startingArray]; 
      Ft= [...startingArray]; 
      a= [...startingArray]; 
      d= [...startingArray];
      w1= [...startingArray]; 
      w2= [...startingArray]; 
      eng = [...startingArray];
      // initial kart velocity in m/s
      // assumed 0 in this version
      v[0] = initialVel*(1000/(60*60));
      // use initial kart velocity to set an initial output shaft rotation speed
      w2[0] = v[0]/(0.2794*0.5) * (60/(2*3.14));
      w1[0] = w2[0] * GR;
      // idling engine speed (RPM)
      eng[0] = 2200;
      // set engine speed maximum limit (based on experimental data)
      maxRpm = 6960
      for (let i = 0; i < t.length  ; i++){
  
        c[i+1] = 0.005 + (1/parameters['p'])*(0.01+0.0095*((v[i]*3.6)/100)**2)
        Fr[i+1] = c[i]*parameters['m'] * parameters['g']
        Fd[i+1] = 0.5*parameters['rho']*parameters['Cd']*parameters['A']*(v[i]**2)

        // torque for each engine speed using engine power curves

        Teng =everpolate.polynomial(eng[i], this.rpm, this.trq); 

        Tout = Teng * parameters['tEff'] * GR;
    
        Ft[i+1] = Tout/parameters['wheelr']

        if( w1[i]<maxRpm){
            a[i+1] = 1/(parameters['lm']*parameters['m']) * (Ft[i+1] - Fr[i+1] - Fd[i+1])
        } else {
            a[i+1] = 0
        }

        // calculate instantaneous speed change (over dt)
        v[i+1] = v[i] + a[i+1]*this.dt
        
        // calculate distance travelled (over dt)
        d[i+1] = d[i] + v[i+1]*this.dt
        
        // calculate rear axle rpm based on vehicle travel speed
        w2[i+1] = v[i+1]/(this.wheelr) * (60/(2*3.14))
        w1[i+1] = (w2[i+1])*GR
        
        // update new engine speed based on increase in output shaft speed
        // parameter that was tuned to reflect real life behaviour
        alpha = 0.40
        newEngSpeed = eng[i] + alpha*(w1[i+1]-w1[i])
        if( newEngSpeed >= maxRpm ||  w1[i+1] >= maxRpm){
          eng[i+1] = maxRpm;
          w1[i+1] = maxRpm;
        } else {
            if (newEngSpeed > w1[i+1]) {
              eng[i+1] = newEngSpeed
            }
            else {
                eng[i+1] = w1[i+1]
            }
        }
      }
      km = v.map(x=> x*3.6);
      gs = a.map(x=>x/this.g);
      function find(val, a, b ){
          let overindex = [];
          a.forEach((item, index)=> {
            if(item > val){
              overindex.push(index);
            }
          })
  
          //  overindex = np.where(a > val);
          // 
            let  firstindex = overindex[0]
            return [firstindex, b[firstindex] ]
        }
        try {
            [ firstindex, timeDist] = find(distance, d, t)
          } catch (error) {
            console.error('Time domain not sufficient for a distance of ', distance, 'm, increase T_end');
            timeDist = 0
          }


      this.results['time'] = t
      this.results['enginerpm'] = eng
      this.results['speed'] = km
      this.results['acc'] = gs
      this.results['dist'] = d
      this.results['timeDist'] = timeDist
      this.results['firstIndex'] = firstindex
      this.results['w1'] = w1
      this.results['w2'] = w2
      this.results['Fr'] = Fr
      this.results['Fd'] = Fd
      this.results['Ft'] = Ft
   
    },
    resetValues: function(){
      this.buttonMessage= "Reset Kart";
      this.raceCompletion= 0; 
      this.tweenedRaceCompletion= 0;
      this.race= false;
      this.m= 96.5 +85;
      this.g= 9.81;
      this.p=2.48211;
      this.Cd= 0.5;
      this.A=0.4;
      this.wheelr= 0.2794/2;
      this.G1= 20;
      this.G2= 71;
      this.rho= 1.23;
      this.distance= 500;
      this.dt=0.01;
      this.tend= 50;
      this.engagedSpeed= 2000;
      this.tEff= 0.93;
      this.rpm= [2000, 2600, 3000, 3500, 4000, 5000, 6000, 6200, 6960]
      this.drpm= 1;
      this.raceCompletion = 0;
      this.timeToTravel = 0;
      Object.keys(this.results).forEach(key => {
        this.results[key] = null;
      })
    },
  },
    watch: {
    raceCompletion: function(newValue) {
      gsap.to(this.$data, { duration: 2, tweenedRaceCompletion: newValue });
    },
    allProperties: function(){
      this.raceCompletion = 0;
      this.timeToTravel = 0;
      Object.keys(this.results).forEach(key => {
      this.results[key] = null;
      this.race = false;
      })
    },

  }
  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
  padding: 15px 30px;
}
h1 {
  margin: 3px;
  position: relative;

  text-align: left;
}
h2 {
  margin: 3px;

  text-align: left;
  position: relative;

}

th {
  min-width: 200px;
}
.logo {
  display: inline;
  width: 200px;
  height: 50px;
}
.header {
  display: flex;
  height: 200;
  margin-left: 1rem;
}
.header__titles {
  margin-left: 20px;
}
.grid-wrapper{
  padding: 30px;
  box-sizing: border-box;
  width: 100vw;
column-gap: 10px;
row-gap: 10px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: 1fr 800px 500px;
  grid-template-areas: 
  "header header header header"
  "main-left main-left main-right main-right"
  "mid-graph mid-graph mini1 mini2";
}
.simulation{
grid-area: header;

}

.simulation-inputs {

width: 100%;


}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 25px;
box-sizing: border-box;
margin-bottom: 15px;
}
th, td {
  padding: 5px;
  text-align: left;
}

.race-button{ 
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 5px 22px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 24px;
  margin: 10px ;
  cursor: pointer;
  border-radius: 12px;
  width: 300px;
}
.active {
  background-color: red;
}

.graph-grid {

  display: grid;
  grid-template-columns: 1fr 1fr ;
  grid-template-rows: 300px 300px;
  height:600 px;
  width: 100%;

}

@media only screen and (max-width: 1500px) {
  .graph-grid {
      grid-template-columns: 1fr;
       grid-template-rows: auto auto auto auto;
  }
}
.panel-layout {
  display: grid;
  gap: 50px;
  grid-template-columns: 1.5fr 2fr;
  height: 600px;
  box-sizing: border-box;
 
}

@media only screen and (max-width: 600px) {
  .panel-layout {
      grid-template-columns: 100%;
grid-template-rows: none;
      height: initial;
  }
    .graph-grid {
      grid-template-columns: 100%;
       grid-template-rows: auto auto auto auto;
  }
}

.left-wrap {
  width: 100%;
  height: 100%;
}

.left-align{
  text-align: left
}

.units {
  font-weight: bold;
  margin-left: 4px;
  text-align: right;
}

.reset-values {
  background-color: #4c91af;
  border: none;
  color: white;
  padding: 5px 22px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 24px;
  margin: 10px ;
  cursor: pointer;
  border-radius: 12px;
  width: 300px;
}

.table-inputs{
  width: 100%;

}
.lds-ring {
  display: inline-block;

  width: 30px;
  height: 30px;
}
.lds-ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 64px;
  height: 64px;
  margin: 8px;
  border: 8px solid #fff;
  border-radius: 50%;
  animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #fff transparent transparent transparent;
}
.lds-ring div:nth-child(1) {
  animation-delay: -0.45s;
}
.lds-ring div:nth-child(2) {
  animation-delay: -0.3s;
}
.lds-ring div:nth-child(3) {
  animation-delay: -0.15s;
}
@keyframes lds-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.calc-button{
  display: flex;
  align-items: center;;
}
</style>
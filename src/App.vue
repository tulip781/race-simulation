<template>
  <div id="app">
    <div class="header">
      <img src="./assets/imp.svg.png" class="logo" />
      <div class="header__titles">
        <h1>Kart Transmission Lab Materials</h1>
        <h2>MECH40007 - Design and Manufacture</h2>
      </div>
    </div>
    <label for="completion">Completion amount</label>
        <input id="completion" type="range" min="0" max="1" step="0.01" v-model="raceCompletion">
  <div class="grid-wrapper">

    <div class="simulation"><h2>Drag Race Simulation</h2><RaceTrack :carCompletion="tweenedRaceCompletion"/></div>
    
    <div class="simulation-inputs">
      <h2> Random Track Length: {{this.distance}} Meters</h2>
      <table style="width:100%">
        <tr>
          <th>Gear 1:</th>
          <td><input type="text" id="gearRatio" :placeholder="G1" v-model="G1"></td>
        </tr>
        <tr>
          <th>Gear 2:</th>
          <td><input type="text" id="gearRatio" :placeholder="G2" v-model="G2"></td>
        </tr>
        <tr>
          <th>Gear Ratio:</th>
          <td>G1 / G2 = {{GR}}</td>
        </tr>
        <tr>
          <th>Mass of Kart + Driver (kg):</th>
          <td><input type="text" id="massKD" :placeholder="m" v-model="m"></td>
        </tr>
        <tr>
          <th>Tyre Pressure (not including differences due to tyre temp change) (bar)</th>
          <td><input type="text" id="p"  :placeholder="p" v-model="p"></td>
        </tr>
        <tr>
          <th>Coefficient of drag</th>
          <td><input type="text" id="Cd" :placeholder="Cd" v-model="Cd"></td>
        </tr>
        <tr>
          <th>Frontal Area</th>
          <td><input type="text" id="A" :placeholder="A" v-model="A"></td>
        </tr>
        <tr>
          <th>Wheel Radius</th>
          <td><input type="text" id="wheelr" :placeholder="wheelr" v-model="wheelr"></td>
        </tr>
        <tr>
          <th>Mass Factor</th>
          <td><input type="text" id="lm" :placeholder="lm" v-model="lm"></td>
        </tr>
        <tr>
          <th>Density of Air</th>
          <td><input type="text" id="rho" :placeholder="rho" v-model="rho"></td>
        </tr>
        <tr>
          <th>T End - Between 0 - 10</th>
          <td><input type="text" id="tend" :placeholder="tend" v-model="tend" min="0" max="10"></td>
        </tr>
        <tr>
          <th>Engaged Speed</th>
          <td><input type="text" id="engagedSpeed" :placeholder="engagedSpeed" v-model="engagedSpeed"></td>
        </tr>
        <tr>
          <th>Total Drive Train Efficiency  (not including clutch) (constant)</th>
          <td><input type="text" id="tEff" :placeholder="tEff" v-model="tEff"></td>
        </tr>
      </table>
      <button @click="raceKart" class="race-button" v-bind:class="{ active: race, reset: !race }">
        
        <p v-if="!race"> Race Kart </p>
        <p v-else> Reset Race </p>

      </button>
    </div>
    <GraphOne class="graph1" :gr="GR" :speed="results.speed" :time="results.time"></GraphOne>
    <GraphTwo class="graph2" :time="results.time" :fr="results.Fr" :fd="results.Fd" :ft="results.Ft"></GraphTwo>
    <GraphThree class="graph3" :time="results.time" :acc="results.acc"></GraphThree>
    <GraphFour class="graph4" :time="results.time" :w1="results.w1" :w2="results.w2" :enginerpm="results.enginerpm"></GraphFour>
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
    RaceTrack
  },
  data:function(){
    return {
      // raceCompletion must be decimal between 0-1
      raceCompletion: 0, 
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
    raceKart: function(){
      this.race = !this.race;
      if(this.race){
        this.simulate(this.GR, this.t, this.parameters, this.distance)
        this.raceCompletion = Math.random() * (1 - 0) + 0;
      } else {
        this.raceCompletion = 0;
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
        // console.log(0.005 + (1/parameters['p'])*(0.01+0.0095*((v[i]*3.6)/100)**2))
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
          console.log("A ,", a)
          a.forEach((item, index)=> {
            if(item > val){
              overindex.push(index);
            }
          })
          console.log("Overindex, ", overindex)
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
   
    }
  },
    watch: {
    raceCompletion: function(newValue) {
      gsap.to(this.$data, { duration: 2, tweenedRaceCompletion: newValue });
    }
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
grid-area: main-left;

}
.graph1{
grid-area: main-right;

padding: 5px;
box-sizing: border-box;
}
.graph2{
grid-area: mid-graph;

}
.graph3{
grid-area: mini1;

}
.graph4{
  grid-area: mini2;
  background-color: rgb(255, 136, 0);
}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
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
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 10%;
}
.active {
  background-color: red;
}
</style>
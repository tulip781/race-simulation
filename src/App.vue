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
      <h2> Random Track Length: 250m</h2>
      <table style="width:100%">
        <tr>
          <th>Gear Ratio:</th>
          <td><input type="text" id="gearRatio" placeholder="0"></td>
        </tr>
        <tr>
          <th>Mass of Kart + Driver (kg):</th>
          <td><input type="text" id="massKD" placeholder="181.5kg"></td>
        </tr>
        <tr>
          <th>Tyre Pressure (not including differences due to tyre temp change) (bar)</th>
          <td><input type="text" id="p"  placeholder="2.48221"></td>
        </tr>
        <tr>
          <th>Coefficient of drag</th>
          <td><input type="text" id="Cd" placeholder="0.5"></td>
        </tr>
        <tr>
          <th>Frontal Area</th>
          <td><input type="text" id="A" placeholder="0.4"></td>
        </tr>
        <tr>
          <th>Wheel Radius</th>
          <td><input type="text" id="wheelr" placeholder="0.2794/2"></td>
        </tr>
        <tr>
          <th>Mass Factor</th>
          <td><input type="text" id="lm" placeholder="0.2794/2"></td>
        </tr>
        <tr>
          <th>Density of Air</th>
          <td><input type="text" id="rho" placeholder="0.2794/2"></td>
        </tr>
        <tr>
          <th>Engaged Speed</th>
          <td><input type="text" id="engagedSpeed" placeholder="2000"></td>
        </tr>
        <tr>
          <th>Total Drive Train Efficiency  (not including clutch) (constant)</th>
          <td><input type="text" id="tEff" placeholder="0.92"></td>
        </tr>
      </table>
      <button @click="raceKart" class="race-button" v-bind:class="{ active: race, reset: !race }">
        
        <p v-if="!race"> Race Kart </p>
        <p v-else> Reset Race </p>

      </button>
    </div>
    <GraphOne class="graph1"></GraphOne>
    <GraphTwo class="graph2"></GraphTwo>
    <GraphThree class="graph3"></GraphThree>
    <GraphFour class="graph4"></GraphFour>
  </div>
    
  </div>
</template>

<script>
import GraphOne from "./components/GraphOne.vue";
import GraphTwo from "./components/GraphTwo.vue";
import GraphThree from "./components/GraphThree.vue";
import GraphFour from "./components/GraphFour.vue";
import RaceTrack from "./components/RaceTrack.vue";
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
    }
  },
  methods: {
    raceKart: function(){
      this.race = !this.race;
      if(this.race){
        this.raceCompletion = Math.random() * (1 - 0) + 0;
      } else {
        this.raceCompletion = 0;
      }
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
  grid-template-rows: 1fr auto 300px;
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
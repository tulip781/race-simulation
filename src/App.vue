<template>
  <div id="app">
    <div class="header">
      <img src="./assets/imp.svg.png" class="logo" />
      <div class="header__titles">
        <h1>Kart Transmission Lab Materials</h1>
        <h2>MECH40007 - Design and Manufacture</h2>
      </div>
    </div>
  <div class="grid-wrapper">
    <div class="simulation"><h2>Drag Race Simulation</h2></div>
    <div class="simulation-inputs"><h2>Random Track Length: 250m</h2></div>
    <DemoGraph class="graph1"></DemoGraph>
    <DemoGraph class="graph2"></DemoGraph>
    <DemoGraph class="graph3"></DemoGraph>
    <DemoGraph class="graph4"></DemoGraph>
  </div>
    
  </div>
</template>

<script>
import DemoGraph from "./components/DemoGraph.vue";
export default {
  name: "App",
  title: "Dimensional Graph",
  components: {
    DemoGraph,
  },
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
  font-weight: lighter;
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
  box-sizing: border-box;
  width: 100vw;
  height: 600px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-template-rows: 100px 1fr 1fr;
  grid-template-areas: 
  "header header header header"
  "main-left main-left main-right main-right"
  "mid-graph mid-graph mini1 mini2";
}
.simulation{
grid-area: header;
background-color: pink;
}

.simulation-inputs {
grid-area: main-left;
background-color: orange;
}
.graph1{
grid-area: main-right;
background-color: yellow;
padding: 5px;
box-sizing: border-box;
}
.graph2{
grid-area: mid-graph;
background-color: green;
}
.graph3{
grid-area: mini1;
background-color: blue;
}
.graph4{
  grid-area: mini2;
  background-color: rgb(255, 136, 0);
}
</style>
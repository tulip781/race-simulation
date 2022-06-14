<template>
  <div>

    <Plotly
    class="graph"
    v-bind="graphData.data.attr"
    :data="graphData.data.data"
    :layout="graphData.data.layout"
       :display-mode-bar="false"
      :drag-mode="false"
      :responsive="true"
        ></Plotly>
  </div>
</template>
<script>


import { Plotly } from "vue-plotly";

export default {
  name: "GraphOne",
  components: {
      Plotly
  },

  props: {
    gr:{
      type: Number,
      default: 0
    },
    time: {
      type: Array,
      default: function(){
        return[]
      }
    },
    speed: {
      type: Array,
      default: function(){
        return[]
      }
    },

  },
  computed: {
        customRange(){
        let range;
        if (!Array.isArray(this.time) || !this.time.length){
          range = [0, 10];
        } else {
          range = []
        }
        return range},
            customTick(){
        let tick;
        if (!Array.isArray(this.time) || !this.time.length){
          tick = 2;
        } else {
          tick = 0;
        }
        return tick},
    code() {
      const {
        selected: {
          data: { attr }
        }
      } = this;
      const fromAttr = Object.keys(attr)
        .map(key => `:${key}="${attr[key]}"`)
        .join(" ");
      return `<plotly :data="data" :layout="layout" ${fromAttr}/>`;
    },
    trace1: function(){
      return {
        x: this.time,
        y: this.speed,
        type: 'scatter',
        line: {
          color:  "#0096FF"
        }
     }
    },
    graphData: function() {
      return{
        display: 'Scatter',
        data: {
          data: [this.trace1],
          attr: { displayModeBar: false },
          layout: {

            dragmode: false,
            scrollZoom: false,
            title: 'Kart Speed (km/h) vs Time (s) for a Gear Ration of ' + this.gr.toString(),           
              xaxis: {
                title: "Time (s)", dtick: this.customTick, range: this.customRange, tick: '',    showline: true,

              },

              yaxis: {
                title: "Speed (km/h)" , dtick: this.customTick, range: this.customRange, tick: ''    ,showline: true,
},
           


          },
        },
      }
    },}
};
</script>
<style>
.layout .jsoneditor-vue {
  height: 150px;
}
.data .jsoneditor-vue {
  height: 300px;
}
.jsoneditor-vue div.jsoneditor-tree {
  min-height: 100px;
}
.mark-up {
  margin-top: 8px;
}
.graph {
 height: 300px;
}
div.jsoneditor-menu {
  background-color: #007bff;
  border-bottom: 1px solid #007bff;
}
.descriptor > span {
  margin-left: 5px;
  margin-top: 5px;
}
</style>
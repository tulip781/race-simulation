
<template>
  <div>
    <Plotly
    class="graph"
    v-bind="graphData.attr"
    :data="graphData.data.data"
    :layout="graphData.data.layout"
        ></Plotly>
  </div>
</template>
<script>

import { Plotly } from "vue-plotly";

export default {
  name: "GraphTwo",
  components: {
      Plotly
  },

 props: {
   time: {
     type: Array,
     default: function(){
       return []
     }
   },
    fr: {
     type: Array,
     default: function(){
       return []
     }
   },
    fd: {
     type: Array,
     default: function(){
       return []
     }
   },
    ft: {
     type: Array,
     default: function(){
       return []
     }
   }
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
    frc: function( ){
      let newV = [];
      if(this.fr){
        newV = this.fr.map(item => item * -1)
      }
       
      return newV
    },
      fdc: function( ){
        let newV = [];
        if(this.fd ){
          newV = this.fd.map(item => item * -1)
        }
      return newV
    },
        ftc: function( ){
          let newV, newZ = [];
          if(this.ft ){
            newV = this.ft.map((item, index) => item - this.fr[index]);
            newZ = newV.map((item, index) => item - this.fd[index]);}
          return newZ
    },
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
        y: this.frc,
        type: 'scatter',
        line: {
          color:  "#66FF00"
        },
        name: "Rolling Resistance"
      }
    },
    trace2: function(){
      return {
        x: this.time,
        y: this.fdc,
        type: 'scatter',
        line: {
          color:  "#0096FF"
        },
        name: "Aerodynamic Drag"
      }
    },
    trace3:function(){
      return {
        x: this.time,
        y: this.ft,
        type: 'scatter',
        line: {
          color:  "#FFA500"
        },
        name: "Traction Force (Engine)"
      }
    },
    trace4:function(){
      return {
        y: this.ftc,
        x: this.time,
        type: 'scatter',

        line: {
          color:  "#EE4B2B"
        },
        name: "Net Force"
      }
    },
    graphData: function(){
      return {
    display: 'Scatter',
    data: {
      data: [this.trace1, this.trace2, this.trace3, this.trace4],
      attr: { displayModeBar: false },
      layout: {
        title: 'Kart Rear Wheel Forces (N)',

        dragmode: false,
        scrollZoom: false,
          yaxis: {
            title: "Forces (N)",autorange: true , dtick: this.customTick, range: this.customRange, tick: ''},


          xaxis: {
            title: "Time (s)",autorange: true , dtick: this.customTick, range: this.customRange, tick: '',

          },

      },
    },
  }
    },
  }
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
.graph-two {
   height: 30%;
   width: 70%;
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
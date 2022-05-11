
<template>
  <div>
    <Plotly
    class="graph"
    v-bind="graphData.attr"
    :data="graphData.data.data"
    :layout="graphData.layout"
        ></Plotly>
  </div>
</template>
<script>

import data4 from "./data4.js";
import { Plotly } from "vue-plotly";
export default {
  name: "GraphFour",
  components: {
      Plotly
  },

  data() {
    return {
      generics: [data4],
      selected: data4
    };
  },
  props:{
    time: {
     type: Array,
     default: function(){
       return []
     }
   },
   w1: {
     type: Array,
     default: function(){
       return []
     }
   },
   w2: {
     type: Array,
     default: function(){
       return []
     }
   },
   enginerpm: {
     type: Array,
     default: function(){
       return []
     }
   },
  },
  computed: {
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
        y: this.w1,
        type: 'scatter',
        line: {
          color:  "#66FF00"
        },
        name: "Rear Axle Sprocket"
      }
    },
    trace2: function(){
      return {
        x: this.time,
        y: this.w2,
        type: 'scatter',
        line: {
          color:  "#0096FF"
        },
        name: "Clutch Sprocket"
      }
    },
    trace3: function(){
      return {
        x: this.time,
        y: this.enginerpm,
        type: 'scatter',
        line: {
          color:  "#FFA500"
        },
        name: "Engine Speed"
      }
    },
    graphData(){
      return {
  display: 'Scatter',
  data: {
    data: [this.trace1, this.trace2, this.trace3],
    attr: { displayModeBar: false },
    layout: {
      title: 'Engine and Sprocket Speeds (RPM)',

      dragmode: false,
      scrollZoom: false,
        yaxis: {
          title: "Forces (N)"},
          dtick: 100,

        xaxis: {
          title: "Time (s)",
          dtick: 10,
        },

    },
  },
};
    }
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
.graph {
 height: 100%;
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
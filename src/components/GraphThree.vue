
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

import data3 from "./data3.js";
import { Plotly } from "vue-plotly";
export default {
  name: "GraphThree",
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
    acc: {
     type: Array,
     default: function(){
       return []
     }
   },
  },
  data() {
    return {
      generics: [data3],
      selected: data3
    };
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
        y: this.acc,
        x: this.time,
        type: 'scatter',
      }
    },
    graphData: function(){
      return  {
    display: 'Scatter',
    data: {
      data: [this.trace1],
      attr: { displayModeBar: false },
      layout: {
        title: 'Longitudional Acceleration (G/s)',

        dragmode: false,
        scrollZoom: false,
          yaxis: {
  
            dtick: 0.1,},

          xaxis: {
            title: "Time (s)",
            dtick: 10,
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
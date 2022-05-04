
<template>
  <div>
    <Plotly
    class="graph"
    v-bind="selected.data.attr"
    :data="selected.data.data"
    :layout="selected.data.layout"
        ></Plotly>
  </div>
</template>
<script>

import simple from "./simple.js";
import { Plotly } from "vue-plotly";
export default {
  name: "GraphTwo",
  components: {
      Plotly
  },

  data() {
    return {
      generics: [simple],
      selected: simple
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
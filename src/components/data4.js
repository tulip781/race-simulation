const trace1 = {
  x: [0,4,10, 20, 40, 50],
  y: [400,600,400,  200, 200, 200],
  type: 'scatter',
  line: {
    color:  "#66FF00"
  },
  name: "Traction Force Engine"
};

const trace2 = {
  x: [0, 50 ],
  y: [0, -10],
  type: 'scatter',
  line: {
    color:  "#0096FF"
  },
  name: "Rolling Resistance"
};

const trace3 = {
  x: [0, 10, 20, 30, 40, 50],
  y: [0, -90, -110, -110, -110, -110],
  type: 'scatter',
  line: {
    color:  "#FFA500"
  },
  name: "Aerodynamic Drag"
};
const trace4 = {
  y: [380, 300, 30, 30 , 30, 30],
  x: [0,10, 20, 30, 40,50],
  type: 'scatter',

  line: {
    color:  "#EE4B2B"
  },
  name: "Net Force"
};

export default {
  display: 'Scatter',
  data: {
    data: [trace1, trace2, trace3, trace4],
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
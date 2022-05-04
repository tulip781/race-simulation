const trace1 = {
    x: [0,2,4,10, 20, 50],
    y: [0,10,40,90,  115, 115],
    type: 'scatter',
    line: {
      color:  "#0096FF"
    }
  };
  

  export default {
    display: 'Scatter',
    data: {
      data: [trace1],
      attr: { displayModeBar: false },
      layout: {

        dragmode: false,
        scrollZoom: false,
        title: 'Kart Speed (km/h) vs Time (s) for a Gear Ration of 3',

          yaxis: {
            title: "Speed (km/h)"},
            dtick: 20,

          xaxis: {
            title: "Time (s)",
            dtick: 5,
          },

      },
    },
  };
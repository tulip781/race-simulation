const trace1 = {
    y: [0, 0.3, 0.25, 0.1, 0.1, 0.1, 0.1, 0.1 ,0.1 ,0.1, 0.1, 0.1],
    x: [0,5,10, 15,20,25,30,35,40,45,50],
    type: 'scatter',
  };

  
  export default {
    display: 'Scatter',
    data: {
      data: [trace1],
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
  };
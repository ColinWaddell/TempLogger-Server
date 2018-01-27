var chart = {};
var canvas = {};
var graph_data = [];

function DrawGraph(chart_id){
    chart[chart_id] = nv.models.lineChart();
    nv.addGraph(function() {
        chart[chart_id].margin({left: 60})  //Adjust chart margins to give the x-axis some breathing room.
             .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
             .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
             .showYAxis(true)        //Show the y-axis
             .showXAxis(true)        //Show the x-axis
             .interpolate("step-after") 
            ;
        
        chart[chart_id].xAxis
            .tickFormat(function(d) { 
                return d3.time.format('%a %H:%M')(new Date(d));
            });

        chart[chart_id].yAxis
            .axisLabel('Temperature (°C)')
            .tickFormat(function(d) { 
                return d.toFixed(2) + "°C";
            });

        nv.utils.windowResize(chart[chart_id].update);
        return chart[chart_id];
    });
}

function UpdateGraph(chart_id, data){
    if (data==null) return;
    // Tidy up iso to js-date
    data.forEach(datum => {
        datum.values.forEach(val => {
            val.x = new Date(val.x);
        })
        graph_data.push(datum);
    })
    
    canvas[chart_id] = d3.select(chart_id + " svg");
    canvas[chart_id].datum(graph_data).transition().duration(500).call(chart[chart_id]);
    nv.utils.windowResize(chart.update);
}
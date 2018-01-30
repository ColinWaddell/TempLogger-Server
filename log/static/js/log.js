var chart = {};
var canvas = {};
var graph_data = [];

function DrawGraph(chart_id){
    chart[chart_id] = nv.models.lineChart();
    nv.addGraph(function() {
        chart[chart_id].margin({left: 50})
            .showLegend(true)
            .showYAxis(true)
            .showXAxis(true)
            .tooltip.enabled(false);
        
        chart[chart_id].xAxis
            .tickPadding(20)
            .tickFormat(function(d) {
                return d3.time.format('%a %H:%M')(new Date(d));
            });

        chart[chart_id].yAxis
            .tickPadding(10)
            .tickFormat(function(d) { 
                return d.toFixed(1) + "°C";
            });

        nv.utils.windowResize(chart[chart_id].update);
        return chart[chart_id];
    });
}

function UpdateGraph(chart_id, data, stepafter){
    if (data==null) return;
    // Tidy up iso to js-date
    data.forEach(datum => {
        var stepped_data = new Array();

        datum.values.forEach(val => {
            val.x = new Date(val.x);
        });

        if (stepafter===true){    
            datum.values.forEach(function(val, i, a){
                if (i){
                    var step = {
                        "x": val.x,
                        "y": a[i-1].y,
                    };
                    stepped_data.push(step);
                }
                stepped_data.push(val);
            })
            datum.values = stepped_data;
        };

        graph_data.push(datum);
    })
    
    canvas[chart_id] = d3.select(chart_id + " svg");
    canvas[chart_id].datum(graph_data).call(chart[chart_id]);
}
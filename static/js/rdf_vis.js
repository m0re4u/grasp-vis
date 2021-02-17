"use strict";

var PRED_TYPE_TO_COLOR = {
    'lexical': "rgb(255,0,0)",
    'default': "rgb(0,0,0)"
}

function visualizeRDF(data) {
    var width = 1480, height = 900

    var svg = d3.select("#rdf-container")
        .append("svg")
            .attr("width", width)
            .attr("height", height);

  var force = d3.layout.force()
      .gravity(.03)
      .distance(300)
      .charge(-150)
      .size([width, height]);

    force
        .nodes(data.nodes)
        .links(data.links)
        .start();

    var link = svg.selectAll(".link")
        .data(data.links)
      .enter().append("line")
        .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

    var node = svg.selectAll(".node")
        .data(data.nodes)
      .enter().append("g")
        .attr("class", "node")
        .call(force.drag);

    node.append("circle")
        .attr("r","5")
        .style({fill: function(d) {return PRED_TYPE_TO_COLOR[d.type]}, stroke: function(d) {return PRED_TYPE_TO_COLOR[d.type]}});

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });
}
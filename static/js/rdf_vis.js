"use strict";

var PRED_TYPE_TO_COLOR = {
  'lexical': "rgb(255,0,0)",
  'default': "rgb(0,0,0)"
}

function visualizeRDF(data) {

  var width = 1480, height = 900

  const svg = d3.select('#rdf-container').append("svg")
    .attr("viewBox", [0, 0, width, height])
    .attr('width', width)
    .attr('height', height);

  const g = svg.append("g");

  //set up the simulation
  //nodes only for now
  var simulation = d3.forceSimulation()
    //add nodes
    .nodes(data.nodes);

  //add forces
  //we're going to add a charge to each node
  //also going to add a centering force
  simulation
    .force("charge_force", d3.forceManyBody())
    .force("center_force", d3.forceCenter(width / 2, height / 2))
    .force("collision_force", d3.forceCollide());

  var node = g.selectAll("g")
    .data(data.nodes);

  var nodeEnter = node.enter().append("g");

  var circle = nodeEnter.append("circle")
    .attr("r", 4)
    .attr("fill", (d) => PRED_TYPE_TO_COLOR[d.type]);

  var text = nodeEnter.append("text")
    .attr("dx", 12)
    .attr("dy", ".35em")
    .attr("id", 'node-text')
    .text( (d) => d.text );

  //add tick instructions:
  simulation.on("tick", tickActions);

  //Create the link force
  //We need the id accessor to use named sources and targets
  var link_force = d3.forceLink(data.links)
    .id(function (d) { return d.name; })

  //Add a links force to the simulation
  //Specify links  in d3.forceLink argument
  simulation.force("links", link_force)

  //draw lines for the links
  var link = g.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(data.links)
    .enter().append("line")
    .attr("stroke-width", 2);


  function tickActions() {
    //update circle positions each tick of the simulation
    circle
      .attr("cx", function (d) { return d.x; })
      .attr("cy", function (d) { return d.y; });
    text
      .attr("x", (d) => d.x)
      .attr("y", (d) => d.y);
    //update link positions
    //simply tells one end of the line to follow one node around
    //and the other end of the line to follow the other node around
    link
      .attr("x1", function (d) { return d.source.x; })
      .attr("y1", function (d) { return d.source.y; })
      .attr("x2", function (d) { return d.target.x; })
      .attr("y2", function (d) { return d.target.y; });

  }

  svg.call(d3.zoom()
    .extent([[0, 0], [width, height]])
    .scaleExtent([1, 8])
    .on("zoom", zoomed));

  function zoomed({ transform }) {
    g.attr("transform", transform);
  }

}
"use strict";

function visualizeSRL(fact_name, srl_data) {
    var children = [];
    for (const [role, span] of Object.entries(srl_data)) {
        var text = [];
        for (let i = 0; i < span.length; i++) {
            text.push($("#" + span[i]).text());
        }
        children.push({ 'span': span, 'name': text.join(" "), 'parent': "Top Level", 'role': role });
    }
    var treeData = {
        "role": "pred",
        "name": fact_name[0],
        "parent": "null",
        "children": children
    };
    var margin = { top: 20, right: 120, bottom: 20, left: 60 },
        width = 1200 - margin.right - margin.left,
        height = 500 - margin.top - margin.bottom;

    // const SRL_COLOR = 'rgb(0, 255, 127)';

    var tree = data => {
        const root = d3.hierarchy(data);
        console.log(root);
        root.dx = 80;
        root.dy = width / (root.height + 1);
        return d3.tree().nodeSize([root.dx, root.dy])(root);
    }

    const root = tree(treeData);

    let x0 = Infinity;
    let x1 = -x0;
    root.each(d => {
        if (d.x > x1) x1 = d.x;
        if (d.x < x0) x0 = d.x;
    });

    const svg = d3.select("#srl-container").append("svg")
        .attr("viewBox", [0, 0, width, x1 - x0 + root.dx * 2]);

    const g = svg.append("g")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .attr("transform", `translate(${root.dy / 3},${root.dx - x0})`);

    const link = g.append("g")
        .attr("fill", "none")
        .attr("stroke", "#555")
        .attr("stroke-opacity", 0.4)
        .attr("stroke-width", 5)
        .selectAll("path")
        .data(root.links())
        .join("path")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x));

    const node = g.append("g")
        .attr("stroke-linejoin", "round")
        .attr("stroke-width", 8)
        .selectAll("g")
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle")
        .attr("fill", d => d.children ? "#555" : "#999")
        .attr("r", 7);

    node.append("text")
        .attr("dy", "0.31em")
        .attr("x", d => d.children ? -10 : 10)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .style("font-size", 20)
        .text(d => d.data.role + " - " + d.data.name)
        .clone(true).lower()
        .attr("stroke", "white");
}
//     var tree = d3.layout.tree().size([height, width]);
//     var diagonal = d3.svg.diagonal().projection(function(d) { return [d.y, d.x]; });

//     var svg = d3.select("#srl-container").append("svg")
//         .attr("width", width + margin.right + margin.left)
//         .attr("height", height + margin.top + margin.bottom)
//         .append("g")
//         .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//     root = treeData[0];
//     root.x0 = height / 2;
//     root.y0 = 0;

//     update(root);

//     d3.select(self.frameElement).style("height", "500px");

//     function update(source) {
//         // Compute the new tree layout.
//         var nodes = tree.nodes(root).reverse(),
//         links = tree.links(nodes);

//         // Normalize for fixed-depth.
//         nodes.forEach(function(d) { d.y = d.depth * 180; });

//         // Update the nodes…
//         var node = svg.selectAll("g.node")
//             .data(nodes, function(d) { return d.id || (d.id = ++i); });

//         // Enter any new nodes at the parent's previous position.
//         var nodeEnter = node.enter().append("g")
//             .attr("class", "node")
//             .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
//             .on("click", click);

//         nodeEnter.append("circle")
//             .attr("r", 1e-6)
//             .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

//         nodeEnter.append("text")
//             .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
//             .attr("dy", ".35em")
//             .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
//             .text(function(d) {
//                 if (d.role) {
//                     return d.role + " - " +  d.name;
//                 } else {
//                     return d.name;
//                 }
//             })
//             .style("fill-opacity", 1e-6);

//         svg.selectAll("text")
//             .on("mouseover", function (d) {
//                 if (d.span) {
//                     for (let i=0;i<d.span.length;i++) {
//                         d3.selectAll("#"+d.span[i]).style('background-color', SRL_COLOR);
//                     }
//                 }
//             })
//             .on("mouseout", function (d) {
//                 if (d.span) {
//                     for (let i=0;i<d.span.length;i++) {
//                         d3.selectAll("#"+d.span[i]).style('background-color', "");
//                     }
//                 }
//             });


//         // Transition nodes to their new position.
//         var nodeUpdate = node.transition()
//             .duration(duration)
//             .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

//         nodeUpdate.select("circle")
//             .attr("r", 10)
//             .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

//         nodeUpdate.select("text")
//             .style("fill-opacity", 1);

//         // Transition exiting nodes to the parent's new position.
//         var nodeExit = node.exit().transition()
//             .duration(duration)
//             .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
//             .remove();

//         nodeExit.select("circle")
//             .attr("r", 1e-6);

//         nodeExit.select("text")
//             .style("fill-opacity", 1e-6);

//         // Update the links…
//         var link = svg.selectAll("path.link")
//             .data(links, function(d) { return d.target.id; });

//         // Enter any new links at the parent's previous position.
//         link.enter().insert("path", "g")
//             .attr("class", "link")
//             .attr("d", function(d) {
//                 var o = {x: source.x0, y: source.y0};
//                 return diagonal({source: o, target: o});
//             })

//         // Transition links to their new position.
//         link.transition()
//             .duration(duration)
//             .attr("d", diagonal);

//         // Transition exiting nodes to the parent's new position.
//         link.exit().transition()
//             .duration(duration)
//             .attr("d", function(d) {
//                 var o = {x: source.x, y: source.y};
//                 return diagonal({source: o, target: o});
//             })
//             .remove();

//         // Stash the old positions for transition.
//         nodes.forEach(function(d) {
//             d.x0 = d.x;
//             d.y0 = d.y;
//         });
//     }

//     // Toggle children on click.
//     function click(d) {
//         if (d.children) {
//             d._children = d.children;
//             d.children = null;
//         } else {
//             d.children = d._children;
//             d._children = null;
//         }
//         update(d);
//     }
// }
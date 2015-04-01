var width = 960,
    height = 500;

var fill = d3.scale.category20();

var force = d3.layout.force()
    .size([width, height])
    //.nodes([{"name": "TOTO"}]) // initialize with a single node
    .nodes([])
    .linkDistance(90)
    .charge(-180)
    .on("tick", tick);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    //.on("mousemove", mousemove);
    //.on("mousedown", mousedown);

svg.append("rect")
    .attr("width", width)
    .attr("height", height);

svg.append("defs").selectAll("marker")
    .data(["suit", "licensing", "resolved"])
  .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 25)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
    .style("stroke", "#4679BD")
    .style("opacity", "0.6");

var nodes = force.nodes(),
    links = force.links(),
    node = svg.selectAll(".node"),
    link = svg.selectAll(".link");



var cursor = svg.append("circle")
    .attr("r", 30)
    .attr("transform", "translate(-100,-100)")
    .attr("class", "cursor");

//---Insert-------
var node_drag = d3.behavior.drag()
        .on("dragstart", dragstart)
        .on("drag", dragmove)
        .on("dragend", dragend);

function dragstart(d, i) {

    d3.select(this).classed("fixed", d.fixed = true);
    force.resume();
}

function dragmove(d, i) {
    d.px += d3.event.dx;
    d.py += d3.event.dy;
    d.x += d3.event.dx;
    d.y += d3.event.dy;
}

function dragend(d, i) {
    d.fixed = true; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
    force.resume();
}

restart();


function releasenode(d) {
    d.fixed = false; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
    //force.resume();
}


function mousemove() {
  cursor.attr("transform", "translate(" + d3.mouse(this) + ")");
}

function mousedown() {

  py2js.showMessage('Hello from WebKit');

  var point = d3.mouse(this),
      node = {x: point[0], y: point[1], name: "COUCOU"},
      n = nodes.push(node);

  // add links to any nearby nodes
  nodes.forEach(function(target) {
    var x = target.x - node.x,
        y = target.y - node.y;
    if (Math.sqrt(x * x + y * y) < 30) {
      links.push({source: node, target: target});
    }
  });

  restart();
}

function tick() {

    // Place link
    link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

    // Translate node
    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}

function nodeselected()
{
    js2py.node_selected(d3.select(this).node().__data__.index);
    js2py.send_event({type: "node_selected", node_id: d3.select(this).node().__data__.name })
}

function restart() {
    link = link.data(links);

    link.enter().insert("line", ".node")
      .attr("class", "link")
      .style("marker-end",  "url(#suit)"); // Modified line ;

    node = node.data(nodes);

    // Append group to hold node representation
    anode = node.enter().append("g")
        .attr("class", "node")
        //.call(force.drag)
        .on('dblclick', nodeselected)
        .call(node_drag);

    // Append node point
    anode.append("circle", ".cursor")
        .attr("class", "node")
        .attr("r", 5)
        .style("fill", function (d) { return fill(d.group)} );

    // Append node label
    anode.append("text")
        .attr("class", "node")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });

    force.start();
}

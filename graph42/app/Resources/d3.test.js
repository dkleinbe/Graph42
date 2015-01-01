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
    .on("mousemove", mousemove)
    .on("mousedown", mousedown);

svg.append("rect")
    .attr("width", width)
    .attr("height", height);

var nodes = force.nodes(),
    links = force.links(),
    node = svg.selectAll(".node"),
    link = svg.selectAll(".link");


var cursor = svg.append("circle")
    .attr("r", 30)
    .attr("transform", "translate(-100,-100)")
    .attr("class", "cursor");

restart();

function mousemove() {
  cursor.attr("transform", "translate(" + d3.mouse(this) + ")");
}

function mousedown() {
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

function restart() {
    link = link.data(links);

    link.enter().insert("line", ".node")
      .attr("class", "link");

    node = node.data(nodes);

    // Append group to hold node representation
    anode = node.enter().append("g").attr("class", "node");

    // Append node point
    anode.append("circle", ".cursor")
        .attr("class", "node")
        .attr("r", 5);

    // Append node label
    anode.append("text")
        .attr("class", "node")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name })
        .call(force.drag);

    force.start();
}

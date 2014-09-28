
var graph = Viva.Graph.graph();

var graphics = Viva.Graph.View.svgGraphics(), nodeSize = 24;

graphics.node(function(node) {
              // This time it's a group of elements: http://www.w3.org/TR/SVG/struct.html#Groups
              var ui = Viva.Graph.svg('g'),
                  // Create SVG text element with user id as content
                  svgText = Viva.Graph.svg('text').attr('y', '-4px').text(node.id);

              ui.append(svgText);
              
              return ui;
            }).placeNode(function(nodeUI, pos) {
                // 'g' element doesn't have convenient (x,y) attributes, instead
                // we have to deal with transforms: http://www.w3.org/TR/SVG/coords.html#SVGGlobalTransformAttribute
                nodeUI.attr('transform',
                            'translate(' +
                                  (pos.x - nodeSize/2) + ',' + (pos.y - nodeSize/2) +
                            ')');
            });
 	
//var renderer = Viva.Graph.View.renderer(graph);
//renderer.run();

// Render the graph
var renderer = Viva.Graph.View.renderer(graph, {
		graphics : graphics
	});
renderer.run();
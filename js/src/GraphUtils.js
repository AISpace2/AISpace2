export function removeNode(graph, node) {
  var i = graph.nodes.findIndex(n => n === node);
  if (i === -1) { return; }
  graph.nodes.splice(i, 1);

  for (var i = graph.links.length - 1; i >= 0; i--) {
    const edge = graph.links[i];
    if (edge.source === node || edge.target === node) {
      graph.links.splice(i, 1);
    }
  }
}

export function removeEdge(graph, edge) {
  var i = graph.links.findIndex(e => e === edge);
  if (i === -1) { return; }
  graph.links.splice(i, 1);
}

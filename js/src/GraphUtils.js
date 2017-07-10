export function removeNode(graph, node) {
  var i = graph.nodes.findIndex(n => n === node);
  if (i === -1) { return; }
  graph.nodes.splice(i, 1);

  for (var i = graph.edges.length - 1; i >= 0; i--) {
    const edge = graph.edges[i];
    if (edge.source === node || edge.target === node) {
      graph.edges.splice(i, 1);
    }
  }
}

export function removeEdge(graph, edge) {
  var i = graph.edges.findIndex(e => e === edge);
  if (i === -1) { return; }
  graph.edges.splice(i, 1);
}

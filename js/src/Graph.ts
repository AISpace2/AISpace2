import * as shortid from "shortid";

export interface IGraphNode {
  id: string;
  name: string;
  type: string;
  x?: number;
  y?: number;
  [key: string]: any;
}

export type CSPNodeTypes = "csp:variable" | "csp:constraint";
export interface ICSPGraphNode extends IGraphNode {
  type: CSPNodeTypes;
  domain: number[] | string[];
}

export interface IGraphEdgeJSON {
  source: string;
  target: string;
  id: string;
  name?: string;
  [key: string]: any;
}

export interface IGraphEdge {
  source: IGraphNode;
  target: IGraphNode;
  id: string;
  name?: string;
  type: "edge";
  [key: string]: any;
}

export interface IGraph<
  TNode extends IGraphNode = IGraphNode,
  TEdge extends IGraphEdge = IGraphEdge
> {
  nodes: TNode[];
  edges: TEdge[];
}

export interface IGraphJSON<
  TNode extends IGraphNode = IGraphNode,
  TEdge extends IGraphEdgeJSON = IGraphEdgeJSON
> {
  nodes: TNode[];
  edges: TEdge[];
}

export class Graph<
  TNode extends IGraphNode = IGraphNode,
  TEdge extends IGraphEdge = IGraphEdge
> implements IGraph<TNode, TEdge> {
  public static fromJSON(json: IGraphJSON): Graph {
    const newGraph = {
      edges: [] as IGraphEdge[],
      nodes: [] as IGraphNode[]
    };

    for (const node of Object.values(json.nodes)) {
      newGraph.nodes.push(node);

      if (node.type === "csp:constraint") {
        node.constraint = "lt";
      }
    }

    for (const edge of Object.values(json.edges)) {
      // Find source
      newGraph.edges.push({
        id: edge.id,
        source: newGraph.nodes.find(n => n.id === edge.source)!,
        styles: {},
        target: newGraph.nodes.find(n => n.id === edge.target)!,
        type: "edge"
      });
    }

    return new Graph(newGraph.nodes, newGraph.edges);
  }

  public nodes: TNode[];
  public edges: TEdge[];

  constructor(nodes: TNode[] = [], edges: TEdge[] = []) {
    this.nodes = nodes;
    this.edges = edges;
  }

  public toJSON(): IGraphJSON {
    const nodes: TNode[] = [];
    const edges: IGraphEdgeJSON[] = [];

    for (const node of this.nodes) {
      // Remove x and y properties
      const newNode = Object.assign({}, node);
      delete newNode.x;
      delete newNode.y;

      nodes.push(newNode);
    }

    for (const edge of this.edges) {
      // Re-map each edges pointer to a node to the node's id
      // Note that the edge changes from a IGraphEdge to a IGraphEdgeJSON
      const newEdge = Object.assign({}, edge) as any;
      newEdge.source = newEdge.source.id;
      newEdge.target = newEdge.target.id;

      // Also delete the style property
      delete edge.style;

      edges.push(newEdge);
    }

    return {
      edges,
      nodes
    };
  }

  /**
   * Removes a node from the graph, along with any edges attached to it.
   *
   * If the node is not found in the graph, this function does nothing.
   * @param node The instance of the node to remove.
   */
  public removeNode(node: TNode) {
    const nodeIndex = this.nodes.findIndex(n => n === node);
    if (nodeIndex === -1) {
      return;
    }
    this.nodes.splice(nodeIndex, 1);

    // Remove all edges attached to this node
    for (let i = this.edges.length - 1; i >= 0; i--) {
      const edge = this.edges[i];
      if (edge.source === node || edge.target === node) {
        this.edges.splice(i, 1);
      }
    }
  }

  /**
   * Removes an edge from the graph.
   *
   * If the edge is not found in the graph, this function does nothing.
   * @param edge The instance of the edge to remove.
   */
  public removeEdge(edge: TEdge) {
    const edgeIndex = this.edges.findIndex(e => e === edge);
    if (edgeIndex === -1) {
      return;
    }
    this.edges.splice(edgeIndex, 1);
  }
}

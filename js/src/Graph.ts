export interface IGraphNode {
  /** A identifier for the node that is unique to all other IDs in the graph. */
  id: string;
  /** The name of the node. Used for display purposes. */
  name: string;
  /** A custom string used to track this node's type. */
  type: string;
  /** The x position of the node. */
  x?: number;
  /** The y position of the node. */
  y?: number;
  /** An object that can contain arbitrary properties to influence it's rendering. */
  styles: { [key: string]: any };
  /** Extra properties depending on the node's type. */
  [key: string]: any;
}

export interface IGraphEdge {
  /** A identifier for the node that is unique to all other IDs in the graph. */
  id: string;
  /** The source node for this edge. */
  source: IGraphNode;
  /** The target node for this edge. */
  target: IGraphNode;
  /** The name of the edge, which may be displayed along the edge. */
  name?: string;
  type: "edge";
  /** An object that can contain arbitrary properties to influence it's rendering. */
  styles: { [key: string]: any };
  /** Extra properties depending on the edge's type. */
  [key: string]: any;
}

export type CSPNodeTypes = "csp:variable" | "csp:constraint";
export interface ICSPGraphNode extends IGraphNode {
  type: CSPNodeTypes;
  domain?: number[] | string[];
}

export type SearchNodeTypes = "search:start" | "search:goal" | "search:normal";
export interface ISearchGraphNode extends IGraphNode {
  type: SearchNodeTypes;
  /** The node's heuristic value. Zero by default. Should be non-negative. */
  h: number;
}

export interface ISearchGraphEdge extends IGraphEdge {
  /** The cost associated with taking the edge. */
  cost?: number;
}

export interface IGraphNodeJSON {
  /** A identifier for the node that is unique to all other IDs in the graph. */
  id: string;
  /** The name of the node. Used for display purposes. */
  name: string;
  /** A custom string used to track this node's type. */
  type: string;
  /** Extra properties depending on the node's type. */
  [key: string]: any;
}

export interface IGraphEdgeJSON {
  source: string;
  target: string;
  id: string;
  name?: string;
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
  /**
   * Converts JSON into an instance of the class Graph.
   * @param json The JSON representation of the graph to convert. This may be modified.
   */
  public static fromJSON(json: IGraphJSON): Graph {
    const newGraph = new Graph();

    for (const node of Object.values(json.nodes)) {
      newGraph.addNode(node);
    }

    for (const edge of Object.values(json.edges)) {
      if (edge.styles == null) {
        edge.styles = {};
      }

      newGraph.addEdge(edge);
    }

    return newGraph;
  }

  public nodes: TNode[];
  public edges: TEdge[];

  /** A mapping from IDs in the graph to nodes or edges.
   * 
   * This is useful for quick lookups when you have the ID.
   * Assumption: All IDs are unique.
   */
  public idMap: { [id: string]: TNode | TEdge };

  constructor(nodes: TNode[] = [], edges: TEdge[] = []) {
    this.nodes = nodes;
    this.edges = edges;
    this.updateIdMap();
  }

  public toJSON(): IGraphJSON {
    const nodes: TNode[] = [];
    const edges: IGraphEdgeJSON[] = [];

    for (const node of this.nodes) {
      // Remove x and y properties
      const newNode = Object.assign({}, node);
      delete newNode.x;
      delete newNode.y;

      delete newNode.styles;

      nodes.push(newNode);
    }

    for (const edge of this.edges) {
      // Re-map each edges pointer to a node to the node's id
      // Note that the edge changes from a IGraphEdge to a IGraphEdgeJSON
      const newEdge = Object.assign({}, edge) as any;
      newEdge.source = newEdge.source.id;
      newEdge.target = newEdge.target.id;

      // Also delete the style property
      delete newEdge.styles;
      edges.push(newEdge);
    }

    return {
      nodes,
      edges
    };
  }

  /** Adds a node to the graph.
   * 
   * Some properties, like `x`, `y`, and the `styles` object are provided by default.
   * 
   * @param opts An object containing properties conforming to TNode. These will be added to the node.
   */
  public addNode(opts: TNode | IGraphNodeJSON | any) {
    const nodeDefaults = {
      x: 0,
      y: 0,
      styles: {
        rx: 40,
        ry: 30
      }
    };

    this.nodes.push({
      ...nodeDefaults,
      ...opts as any
    });

    this.updateIdMap();
  }

  /** Adds an edge to the graph.
   * 
   * For convenience, `source` and `target` can either be nodes or IDs.
   * However, nodes must already be in the graph.
   * A default `styles` object and `type` is provided.
   * 
   * @param opts An object containing properties conforming to TEdge. These will be added to the edge.
   */
  public addEdge(opts: TEdge | IGraphEdgeJSON | any) {
    let sourceNode = opts.source;
    if (typeof sourceNode === "string") {
      sourceNode = this.nodes.find(n => n.id === sourceNode)!;
    }

    let targetNode = opts.target;
    if (typeof targetNode === "string") {
      targetNode = this.nodes.find(n => n.id === targetNode)!;
    }

    this.edges.push(
      {
        type: "edge",
        styles: {},
        ...opts as any,
        source: sourceNode,
        target: targetNode
      } as TEdge
    );

    this.updateIdMap();
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

    this.updateIdMap();
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
    this.updateIdMap();
  }

  /**
   * Merge the styles object of each node of the previous graph to the new graph.
   * 
   * The reason why this is necessary is that styles are *not*
   * preserved when being converted to Python (since those classes do not know about the visualization),
   * so in order to keep them, we need to take the styles from the previous graph.
   * In this way, applied styles can persist even after being converted to and from JSON.
   * This is only useful when the graph is being updated with more nodes or edges after conversion.
   * If your graph doesn't have nodes or edges added, it is not necessary to use this!
   * 
   * @param prevGraph The styles of the previous graph are merged into the new graph. 
   */
  public mergeStylesFrom(prevGraph: Graph) {
    for (const node of Object.values(this.nodes)) {
      const i = prevGraph.nodes.findIndex(n => n.id === node.id);
      if (i !== -1) {
        // Copy over the styles of the node in the previous graph
        node.styles = prevGraph.nodes[i].styles;
        node.x = prevGraph.nodes[i].x;
        node.y = prevGraph.nodes[i].y;
      }
    }
  }

  /**
   * Generates an ID map based off of the current graph.
   */
  private updateIdMap() {
    const idMap: { [id: string]: TNode | TEdge } = Object.create(null);

    for (const node of this.nodes) {
      idMap[node.id] = node;
    }

    for (const edge of this.edges) {
      idMap[edge.id] = edge;
    }

    this.idMap = idMap;
  }
}

/**
 * Helper function to serialize a graph. Used by Jupyter widgets.
 * 
 * @param graph The graph to serialize into JSON.
 */
export function serializeGraph(graph: Graph) {
  if (graph == null) {
    return null;
  }
  return graph.toJSON();
}

/**
 * Helper function to deserialize a graph. Used by Jupyter widgets.
 * 
 * @param json The JSON to deserialize into a Graph.
 */
export function deserializeGraph(json: IGraphJSON) {
  if (json == null) {
    return null;
  }
  return Graph.fromJSON(json) as Graph<ISearchGraphNode, ISearchGraphEdge>;
}

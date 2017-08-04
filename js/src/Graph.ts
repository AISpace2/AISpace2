import * as shortid from "shortid";

export interface IGraphNode {
  id: string;
  name: string;
  type: string;
  x?: number;
  y?: number;
  /** An object that can contain arbitrary properties to influence it's rendering. */
  styles: { [key: string]: any };
  [key: string]: any;
}

export interface IGraphEdge {
  source: IGraphNode;
  target: IGraphNode;
  id: string;
  name?: string;
  type: "edge";
  /** An object that can contain arbitrary properties to influence it's rendering. */

  styles: { [key: string]: any };
  [key: string]: any;
}

export type CSPNodeTypes = "csp:variable" | "csp:constraint";
export interface ICSPGraphNode extends IGraphNode {
  type: CSPNodeTypes;
  domain: number[] | string[];
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
   * @param json The JSON representation of the graph to convert.
   * @param prevGraph If provided, the styles of the previous graph are merged
   * into the new graph. The reason why this is necessary is that styles are *not*
   * preserved when being converted to Python (since those classes do not know about the visualization),
   * so in order to keep them, we need to take the styles from the previous graph.
   * In this way, applied styles can persist even after being converted to and from JSON.
   * This is only needed when the graph is being updated with more nodes or edges after conversion.
   */
  public static fromJSON(json: IGraphJSON, prevGraph?: Graph): Graph {
    const newGraph = {
      edges: [] as IGraphEdge[],
      nodes: [] as IGraphNode[]
    };

    const nodeDefaults = {
      x: 0,
      y: 0,
      styles: {
        rx: 40,
        ry: 30
      }
    };

    for (const node of Object.values(json.nodes)) {
      let newNode = { ...nodeDefaults, ...node };

      if (prevGraph != null) {
        // Copy over the styles of the node in the previous graph
        const i = prevGraph.nodes.findIndex(n => n.id === node.id);
        if (i !== -1) {
          newNode = {
            ...node,
            styles: { ...prevGraph.nodes[i].styles },
            x: prevGraph.nodes[i].x,
            y: prevGraph.nodes[i].y
          };
        }
      }
      newGraph.nodes.push(newNode);
    }

    for (const edge of Object.values(json.edges)) {
      // Find source
      newGraph.edges.push({
        ...edge,
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

  /** A mapping from IDs in the graph to nodes or edges.
   * 
   * This is useful for quick lookups when you have the ID.
   * Assumption: All IDs are unique.
   */
  public idMap: { [id: string]: TNode | TEdge };

  constructor(nodes: TNode[] = [], edges: TEdge[] = []) {
    this.nodes = nodes;
    this.edges = edges;
    this.idMap = this.generateIdMap();
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
      delete newEdge.styles;

      edges.push(newEdge);
    }

    return {
      edges,
      nodes
    };
  }

  /** Adds a node to the graph.
   * @param opts An object containing properties conforming to TNode. Default values are added.
   */
  public addNode(opts: {}) {
    this.nodes.push(
      {
        id: shortid.generate(),
        styles: {},
        ...opts
      } as TNode
    );
  }

  /** Adds an edge to the graph.
   * @param opts An object containing properties conforming to TEdge. Default values are added.
   */
  public addEdge(opts: {}) {
    this.edges.push(
      {
        id: shortid.generate(),
        styles: {},
        ...opts
      } as TEdge
    );
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

  /**
   * Generates an ID map based off of the current graph.
   * @returns An ID map, where the keys are IDs and values are either nodes or edges.
   */
  private generateIdMap() {
    const idMap: { [id: string]: TNode | TEdge } = Object.create(null);

    for (const node of this.nodes) {
      idMap[node.id] = node;
    }

    for (const edge of this.edges) {
      idMap[edge.id] = edge;
    }

    return idMap;
  }
}

import * as d3 from "d3";
import { IGraph, IGraphEdge, IGraphNode } from "./Graph";

/**
 * Layout parameters used for laying out the graph.
 */
export interface IGraphLayoutParams {
  /** The available width for the graph. */
  width: number;
  /** The available height for the graph. */
  height: number;
}

/**
 * Lays out a graph by giving nodes x and y properties.
 */
export interface IGraphLayoutEngine {
  /**
   * Performs one-time setup before layout.
   *
   * This function is only called once before the graph is drawn for the first time.
   * If your graph layout algorithm never requires relayout when the graph is updated,
   * perhaps because nodes will be created at mouse position, you may assign
   * x and y positions as properties to each node datum right here.
   */
  setup(graph: IGraph, layoutParams: IGraphLayoutParams, opts?: {}): void;

  /**
   * Re-layouts the graph as a result of graph changes.
   *
   * This function is not called initially for the first render.
   * You may call this function from the setup function if necessary.
   *
   * You should update the x and y properties of each node datum.
   */
  relayout(graph: IGraph, layoutParams: IGraphLayoutParams, opts?: {}): void;
}

/**
 * Lays out a graph using D3's force layout simulation.
 */
export const d3ForceLayoutEngine: IGraphLayoutEngine = {
  relayout: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    return;
  },
  setup: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    /**
     * We will work with a copy of the graph to prevent D3 from adding
     * various additional properties, such as `vx` and `fy`, to our nodes.
     * Later, we'll copy over only the final x and y properties that we're interested in.
     */
    const graphCopy: IGraph = JSON.parse(JSON.stringify(graph));
    const forceSimulation = d3
      .forceSimulation(graphCopy.nodes)
      .force(
        "link",
        d3
          .forceLink()
          .id((node: IGraphEdge) => node.id)
          .links(graphCopy.edges)
          .distance(35)
          .strength(0.6)
      )
      .force("charge", d3.forceManyBody().strength(-30))
      .force(
        "center",
        d3.forceCenter(layoutParams.width / 2, layoutParams.height / 2)
      )
      .force("collision", d3.forceCollide(75))
      .stop();

    const edgePadding = 50;

    // Run simulation synchronously the default number of times (300)
    for (let i = 0, ticksToSimulate = 300; i < ticksToSimulate; i++) {
      forceSimulation.tick();

      // Bound nodes to SVG
      graphCopy.nodes.forEach(node => {
        node.x = Math.max(
          edgePadding,
          Math.min(layoutParams.width - edgePadding, node.x!)
        );
        node.y = Math.max(
          edgePadding,
          Math.min(layoutParams.height - edgePadding, node.y!)
        );
      });
    }

    // Copy over x and y positions onto original graph once simulation is finished
    graphCopy.nodes.forEach((node, i) => {
      graph.nodes[i].x = node.x;
      graph.nodes[i].y = node.y;
    });
  }
};

/**
 * Lays out a graph using D3's tree layout. All nodes of the same depth are placed at the same level.
 */
export const d3TreeLayoutEngine: IGraphLayoutEngine = {
  relayout: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    return;
  },
  setup: (
    graph: IGraph,
    layoutParams: IGraphLayoutParams,
    opts: { root?: IGraphNode } = {}
  ) => {
    /** Maps IDs to nodes */
    const nodeMap: { [key: string]: IGraphNode } = {};
    for (const node of graph.nodes) {
      nodeMap[node.id] = node;
    }

    interface IHierarchyNode {
      node: IGraphNode;
      children: IHierarchyNode[];
    }

    let rootNode = graph.nodes[0];
    if (opts.root != null) {
      rootNode = opts.root;
    }

    const rootData = {
      node: rootNode,
      children: []
    } as IHierarchyNode;

    /** Map node IDs to their data in the hierarchy. Can quickly add children to parent. */
    const map = {
      [rootNode.id]: rootData
    };

    for (const edge of graph.edges) {
      if (!(edge.target.id in map)) {
        const data = {
          node: nodeMap[edge.target.id],
          children: []
        };

        map[edge.target.id] = data;
      }

      // Parent not in map
      if (!(edge.source.id in map)) {
        const data = {
          node: nodeMap[edge.source.id],
          children: []
        };

        map[edge.source.id] = data;
      }

      // Add target to source's children
      map[edge.source.id].children.push(map[edge.target.id]);
    }

    const treeLayout = d3.tree();
    const root = d3.hierarchy(rootData);
    treeLayout(root); // Sets x and y positions, in [0, 1] range

    let maxDepth = 0;
    root.descendants().forEach(n => {
      if (n.depth > maxDepth) {
        maxDepth = n.depth;
      }
    });

    /**
     * Tree layout has a tendency to fill the y-axis, e.g. if you have a parent and a child node,
     * it will place the parent at the top and child at the bottom. This takes up more space then is often necessary.
     * To make this look better, we divide the available height into `maxDepth + 1` equal sections,
     * and place the nodes along those dividing lines. This tends to look better, while still filling
     * the whole area when the depth is high enough.
     */
    const heightDivision = layoutParams.height / (maxDepth + 2);

    root.each((n: d3.HierarchyPointNode<IHierarchyNode>) => {
      n.data.node.x = n.x * layoutParams.width;
      n.data.node.y =
        n.y * (layoutParams.height - heightDivision - heightDivision) +
        heightDivision;
    });
  }
};

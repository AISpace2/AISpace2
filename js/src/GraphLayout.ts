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
   * 
   * When the promise is resolved, the nodes of the graph will have assigned x, y positions.
   */
  setup(
    graph: IGraph,
    layoutParams: IGraphLayoutParams,
    opts?: {}
  ): Promise<void>;

  /**
   * Re-layouts the graph as a result of graph changes.
   *
   * This function is not called initially for the first render.
   * You may call this function from the setup function if necessary.
   * When the promise is resolved, the nodes of the graph will have assigned x, y positions.
   * 
   * You should update the x and y properties of each node datum.
   */
  relayout(
    graph: IGraph,
    layoutParams: IGraphLayoutParams,
    opts?: {}
  ): Promise<void>;
}

/**
 * Lays out a graph using D3's force layout simulation.
 */
export const d3ForceLayoutEngine: IGraphLayoutEngine = {
  relayout: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    return Promise.resolve();
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
        d3.forceLink().id((node: IGraphEdge) => node.id).links(graphCopy.edges)
      )
      .force("charge", d3.forceManyBody().strength(-35))
      .force(
        "center",
        d3.forceCenter(layoutParams.width / 2, layoutParams.height / 2)
      )
      .force("collision", d3.forceCollide(60))
      .stop();

    const edgePadding = 50;

    return new Promise((resolve, reject) => {
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

      resolve();
    });
  }
};

/**
 * Lays out a graph using D3's tree layout. All nodes of the same depth are placed at the same level.
 */
export const d3TreeLayoutEngine: IGraphLayoutEngine = {
  relayout: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    return Promise.resolve();
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
        } as IHierarchyNode;

        map[edge.target.id] = data;
      }

      // Parent not in map
      if (!(edge.source.id in map)) {
        const data = {
          node: nodeMap[edge.source.id],
          children: []
        } as IHierarchyNode;

        map[edge.source.id] = data;
      }

      if (
        map[edge.target.id].children.some(c => c.node.id === edge.source.id)
      ) {
        // There is already an arrow the other way
        // Note that while this prevents endless loops, the tree layout is not designed
        // to work with general graphs, and thus the resulting layout may be very odd
        continue;
      }

      // Add target to source's children
      map[edge.source.id].children.push(map[edge.target.id]);
    }

    return new Promise((resolve, reject) => {
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

      resolve();
    });
  }
};

/*
   This is a test of using cytoscape and it's layouts.
   You must install cytoscape and require it before trying the following.
   Note that some of cytoscape's layouts are asynchronous, which breaks
   the current, synchronous-only layout engine.

export const cytoscapeLayoutEngine: IGraphLayoutEngine = {
  relayout: (graph: IGraph, layoutParams: IGraphLayoutParams, opts = {}) => {
    return;
  },
  setup: (
    graph: IGraph,
    layoutParams: IGraphLayoutParams,
    opts: { name?: string } = {}
  ) => {
    const elements = [];

    for (const node of graph.nodes) {
      elements.push({ data: { id: node.id } });
    }

    for (const edge of graph.edges) {
      elements.push({
        data: { id: edge.id, source: edge.source.id, target: edge.target.id }
      });
    }

    const c = cytoscape({
      elements
    });

    return new Promise((resolve, reject) => {
    c
      .layout({
        name: "dagre",
        boundingBox: {
          x1: 60,
          y1: 60,
          w: layoutParams.width - 120,
          h: layoutParams.height - 120
        },
        fit: true,
        stop() {
          c.nodes().forEach((node: any) => {
            const i = graph.nodes.findIndex(n => n.id === node.id());
            graph.nodes[i].x = node.position().x;
            graph.nodes[i].y = node.position().y;
          });

          resolve();
        }
      })
      .run();
    });
  }
};*/

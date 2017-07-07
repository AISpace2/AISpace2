import * as Backbone from "backbone";
import * as d3 from "d3";
import {
    SimulationLinkDatum,
    SimulationNodeDatum,
} from "d3-force";
import {
    Graph,
    IGraph,
    IGraphEdge,
    IGraphNode,
} from "./Graph";

export default class GraphVisualizer {
    /** The width of the graph. */
    public width: number;
    /** The height of the graph. */
    public height: number;
    /** The normal width of the line to draw. */
    public lineWidth: number = 2.0;
    /** Callback whenever the graph has updated. */
    public onUpdate?: (graph: IGraph) => void;

    /** The graph being drawn. */
    protected graph: Graph;
    /** The root element the graph is drawn in. */
    protected rootEl: HTMLElement;
    /** Represents the root SVG element where the graph is drawn. */
    protected svg: d3.Selection<any, any, any, any>;
    /** A group where all links are drawn. */
    protected edgeContainer: d3.Selection<any, IGraphEdge, any, any>;
    /** A group where all nodes are drawn. */
    protected nodeContainer: d3.Selection<any, IGraphNode, any, any>;

    constructor(graph: Graph) {
        this.graph = graph;
    }

    public render(targetEl: HTMLElement) {
        this.rootEl = targetEl;
        this.width = targetEl.clientWidth;
        this.height = this.width * 0.5;

        // Remove all children of target element to make this function idempotent
        d3.select(targetEl).selectAll("*").remove();

        this.svg = d3.select(targetEl)
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height);

        this.edgeContainer = this.svg.append("g")
            .attr("class", "links");

        this.nodeContainer = this.svg.append("g")
            .attr("class", "nodes");

        this.layoutEngine.setup(this.graph, this);

        this.update();
        this.graphEvents();
    }

    public toJSON() {
        return this.graph;
    }

    /**
     * Updates the graph by re-binding to the data, re-rendering nodes and edges, and re-binding events.
     */
    public update() {
        if (this.onUpdate != null) {
            this.onUpdate(this.graph);
        }

        this.layoutEngine.relayout(this.graph, this);
        this.renderLinks();
        this.renderNodes();
        this.nodeEvents();
        this.edgeEvents();
    }

    /**
     * One-time setup for events relating to the overall graph.
     *
     * @see nodeEvents
     * @see linkEvents
     */
    protected graphEvents() {
        return;
    }

    /**
     * Configuration of events for nodes in the graph. Called every time the graph is updated.
     */
    protected nodeEvents() {
        return;
    }

    /**
     * Configuration of events for edges in the graph. Called every time the graph is updated.
     */
    protected edgeEvents() {
        return;
    }

    protected renderNodes() {
        if (this.rootEl == null) {
            return;
        }

        const updateSelection = this.nodeContainer
            .selectAll("g")
            .data(Object.values(this.graph.nodes), (d: IGraphNode) => d.id);

        const newSelection = updateSelection.enter().append("g");

        newSelection
            .call(d3.drag<any, IGraphNode>()
                .on("drag", (d, i, arr) => {
                    d.x = d3.event.x;
                    d.y = d3.event.y;

                    this.update();
                }));

        newSelection.append("circle")
            .attr("r", 30)
            .attr("fill", "white")
            .attr("stroke", "black");

        newSelection.append("text")
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .text((d) => d.name);

        updateSelection.merge(newSelection)
            .attr("transform", (d) => `translate(${d.x!}, ${d.y!})`);

        updateSelection.exit().remove();
    }

    protected renderLinks() {
        if (this.rootEl == null) {
            return;
        }

        const updateSelection = this.edgeContainer
            .selectAll("line")
            .data(Object.values(this.graph.edges), (d: IGraphEdge) => d.id);

        updateSelection.enter().append("line")
            .merge(updateSelection)
            .attr("stroke-width", this.lineWidth)
            .attr("stroke", "black")
            .attr("x1", (d) => this.graph.nodes[d.source].x!)
            .attr("y1", (d) => this.graph.nodes[d.source].y!)
            .attr("x2", (d) => this.graph.nodes[d.dest].x!)
            .attr("y2", (d) => this.graph.nodes[d.dest].y!);

        updateSelection.exit().remove();
    }

    /**
     * The layout engine used for laying out this graph.
     */
    get layoutEngine() {
        return d3ForceLayoutEngine;
    }
}

/**
 * Layouts a graph by giving nodes x and y properties.
 */
interface IGraphLayoutEngine {
    /**
     * Performs one-time setup before layout.
     *
     * This function is only called once before the graph is drawn for the first time.
     * If your graph layout algorithm never requires relayout when the graph is updated,
     * perhaps because nodes will be created at mouse position, you may assign
     * x and y positions as properties to each node datum right here.
     */
    setup(graph: Graph, visualizer: GraphVisualizer): void;

    /**
     * Re-layouts the graph as a result of graph changes.
     *
     * This function is not called initially for the first render.
     * You may call this function from the setup function if necessary.
     *
     * You should update the x and y properties of each node datum.
     */
    relayout(graph: Graph, visualizer: GraphVisualizer): void;
}

/**
 * Layouts a graph using the results of D3's force layout.
 */
export const d3ForceLayoutEngine: IGraphLayoutEngine = {
    relayout: (g: Graph, visualizer: GraphVisualizer) => { return; },
    setup: (graph: Graph, visualizer: GraphVisualizer) => {
        /**
         * D3's force layout expects an object of the form
         * {
         *      nodes: [],
         *      links: []
         * }
         *
         * We will work with a copy of the graph to prevent D3 from adding
         * various additional properties, such as `vx` and `fy`, to our nodes.
         * Later, we'll copy over only the final x and y properties that we're interested in.
         */
        const graphCopy: IGraph = JSON.parse(JSON.stringify(graph));
        const nodes = Object.values(graphCopy.nodes);
        const links = [];
        for (const edge of Object.values(graphCopy.edges)) {
            links.push({ source: edge.source, target: edge.dest });
        }

        const d3Graph = { links, nodes };
        const forceSimulation = d3.forceSimulation(d3Graph.nodes)
            .force("link", d3.forceLink()
                .id((node: IGraphEdge) => node.id)
                .links(d3Graph.links)
                .distance(35)
                .strength(0.6))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(visualizer.width / 2, visualizer.height / 2))
            .force("collision", d3.forceCollide(75))
            .stop();

        // Run simulation synchronously the default number of times (300)
        for (let i = 0, ticksToSimulate = 300; i < ticksToSimulate; i++) {
            forceSimulation.tick();

            // Bound nodes to SVG
            nodes.forEach((node) => {
                node.x = Math.max(30, Math.min(visualizer.width - 30, node.x!));
                node.y = Math.max(30, Math.min(visualizer.height - 30, node.y!));
            });
        }

        // Copy over x and y positions onto original graph once simulation is finished
        d3Graph.nodes.forEach((node) => {
            const graphNode = graph.nodes[node.id];
            graphNode.x = node.x;
            graphNode.y = node.y;
        });
    },
};

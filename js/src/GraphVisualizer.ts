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

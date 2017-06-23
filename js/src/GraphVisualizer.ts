import * as Backbone from "backbone";
import * as d3 from "d3";
import {
    SimulationLinkDatum,
    SimulationNodeDatum,
} from "d3-force";
import {
    IGraphEdgeJSON,
    IGraphJSON,
    IGraphNodeJSON,
} from "./Graph";

export default class GraphVisualizer {
    public lineWidth: number = 2.0;
    /** The root element the graph is drawn in. */
    protected rootEl: HTMLElement;
    protected graph: IGraphJSON;
    /** A group where all links are drawn. */
    protected linkContainer: d3.Selection<any, SimulationLinkDatum<SimulationNodeDatum> & IGraphEdgeJSON, any, any>;
    /** A group where all nodes are drawn. */
    protected nodeContainer: d3.Selection<any, SimulationNodeDatum & IGraphNodeJSON, any, any>;
    /** The normal width of the line to draw. */
    private width: number;
    private height: number;
    /** Represents the root SVG element where the graph is drawn. */
    private svg: d3.Selection<any, any, any, any>;

    public render(graph: IGraphJSON, targetEl: HTMLElement) {
        this.graph = graph;
        this.rootEl = targetEl;
        this.width = targetEl.clientWidth;
        this.height = this.width * 0.5;

        // Remove all children of target element to make this function idempotent
        d3.select(targetEl).selectAll("*").remove();

        this.svg = d3.select(targetEl)
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height);

        // Enable zoom and pan behaviour
        this.svg.append("rect")
            .attr("width", this.width)
            .attr("height", this.height)
            .style("fill", "none")
            .style("pointer-events", "all")
            .call(d3.zoom()
                .scaleExtent([1, 2.5])
                .on("zoom", () => {
                    this.linkContainer.attr("transform", d3.event.transform);
                    this.nodeContainer.attr("transform", d3.event.transform);
                }));

        // Called whenever node/link positions are updated (either by the force simulation or by dragging)
        const onTick = () => {
            this.linkContainer
                .selectAll("line")
                .data(this.graph.links, (d: IGraphEdgeJSON) => d.id)
                .attr("x1", (d) => ((d.source as SimulationNodeDatum).x) as number)
                .attr("y1", (d) => ((d.source as SimulationNodeDatum).y) as number)
                .attr("x2", (d) => ((d.target as SimulationNodeDatum).x) as number)
                .attr("y2", (d) => ((d.target as SimulationNodeDatum).y) as number);

            this.nodeContainer
                .selectAll("g")
                .data(this.graph.nodes, (d: IGraphNodeJSON) => d.id)
                .each((d) => {
                    d.x = Math.max(30, Math.min(this.width - 30, d.x));
                    d.y = Math.max(30, Math.min(this.height - 30, d.y));
                })
                .attr("transform", (d: SimulationNodeDatum) => `translate(${d.x}, ${d.y})`);
        };

        const forceSimulation = d3.forceSimulation(graph.nodes)
            .force("link", d3.forceLink()
                .id((node: IGraphNodeJSON) => node.id)
                .links(graph.links)
                .distance(35)
                .strength(0.6))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide(75))
            .on("tick", onTick)
            .stop();

        this.linkContainer = this.svg.append("g")
            .attr("class", "links");

        this.nodeContainer = this.svg.append("g")
            .attr("class", "nodes");

        this.update();
        this.graphEvents();
        this.nodeEvents();
        this.linkEvents();

        // Run simulation synchronously instead of asynchronously to prevent visual jitter
        for (let i = 0, ticksToSimulate = 300; i < ticksToSimulate; i++) {
            forceSimulation.tick();
            onTick();
        }

        // Fix all nodes, to prevent them from being moved by further simulations
        this.nodeContainer
            .selectAll("g")
            .data(this.graph.nodes, (d: IGraphNodeJSON) => d.id)
            .each((d: SimulationNodeDatum) => {
                d.fx = d.x;
                d.fy = d.y;
            });

        // Enable dragging of nodes
        this.nodeContainer
            .selectAll("g")
            .data(this.graph.nodes, (d: IGraphNodeJSON) => d.id)
            .call(d3.drag()
                .on("start", () => {
                    // The 'simulation' must be started even though all the node positions are fixed,
                    // or the node positions will not be updated
                    forceSimulation.alphaTarget(0.3).restart();
                })
                .on("drag", (d: SimulationNodeDatum) => {
                    d.fx = Math.max(30, Math.min(this.width - 30, d3.event.x));
                    d.fy = Math.max(30, Math.min(this.height - 30, d3.event.y));
                })
                .on("end", () => {
                    forceSimulation.stop();
                }) as any);
    }

    /**
     * One-time setup for events relating to the overall graph.
     *
     * @see nodeEvents
     * @see linkEvents
     */
    public graphEvents() {
        return;
    }

    /**
     * One-time setup for events relating to nodes.
     */
    public nodeEvents() {
        return;
    }

    /**
     * One-time setup for events relating to links.
     */
    public linkEvents() {
        return;
    }

    public renderNodes() {
        const updateSelection = this.nodeContainer
            .selectAll("g")
            .data(this.graph.nodes, (d: IGraphNodeJSON) => d.id);

        updateSelection.enter().append("circle")
            .attr("r", 30)
            .attr("fill", "white")
            .attr("stroke", "black");

        updateSelection.enter().append("text")
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .merge(updateSelection)
            .text((d) => d.name);
    }

    public renderLinks() {
        const updateSelection = this.linkContainer
            .selectAll("line")
            .data(this.graph.links, (d: IGraphEdgeJSON) => d.id);

        updateSelection.enter().append("line")
            .merge(updateSelection)
            .attr("stroke-width", this.lineWidth)
            .attr("stroke", "black");
    }

    /**
     * Updates the graph by re-binding to the data and re-rendering nodes and edges.
     */
    protected update() {
        this.renderLinks();
        this.renderNodes();
    }
}

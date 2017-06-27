import * as d3 from "d3";
import * as shortid from "shortid";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import { Graph, IGraphEdge, IGraphNode } from "./Graph";

export default class GraphBuilder extends CSPGraphVisualizer {
    private selectedElement: IGraphNode | IGraphEdge | null;

    constructor(graph: Graph) {
        super(graph);
        this.lineWidth = 5;
    }

    public graphEvents() {
        d3.select(this.rootEl).on("keydown", () => {
            if (d3.event.keyCode === 46) {
                d3.event.preventDefault();

                if (this.selectedElement != null) {
                    this.graph.removeNode(this.selectedElement.id);
                    delete this.graph.edges[this.selectedElement.id];

                    this.selectedElement = null;
                    this.update();
                }
            }
        });

        d3.select(this.rootEl).on("dblclick", () => {
            const [x, y] = d3.mouse(this.rootEl);
            this.createNode(x, y);
        });
    }

    public nodeEvents() {
        super.nodeEvents();

        this.nodeContainer.selectAll("g")
            .on("click", (d: IGraphNode) => {
                if (d3.event.defaultPrevented) {
                    return;
                }

                if (d !== this.selectedElement) {
                    this.selectedElement = d;
                } else {
                    this.selectedElement = null;
                }

                this.update();
            });
    }

    public edgeEvents() {
        super.edgeEvents();

        this.edgeContainer.selectAll("line")
            .on("click", (d: IGraphEdge) => {
                d3.event.stopPropagation();

                if (d !== this.selectedElement) {
                    this.selectedElement = d;
                } else {
                    this.selectedElement = null;
                }

                this.update();
            });
    }

    public renderNodes() {
        super.renderNodes();

        this.nodeContainer.selectAll("g")
            .filter((d: IGraphNode) => d === this.selectedElement)
            .select(":first-child").attr("fill", "pink");

        this.nodeContainer.selectAll("g")
            .filter((d: IGraphNode) => d !== this.selectedElement)
            .select(":first-child").attr("fill", "white");

        this.edgeContainer.selectAll("line")
            .filter((d: IGraphEdge) => d === this.selectedElement)
            .attr("stroke", "pink");

        this.edgeContainer.selectAll("line")
            .filter((d: IGraphEdge) => d !== this.selectedElement)
            .attr("stroke", "black");
    }

    private createNode(x: number, y: number) {
        const id = shortid.generate();
        this.graph.nodes[id] = {
            domain: ["1"],
            id,
            name: "???",
            type: "csp:variable",
            x,
            y,
        };

        this.update();
    }
}

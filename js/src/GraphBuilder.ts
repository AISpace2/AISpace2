import * as d3 from "d3";
import * as shortid from "shortid";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import { IGraphEdgeJSON, IGraphNodeJSON } from "./Graph";

export default class GraphBuilder extends CSPGraphVisualizer {
    private selectedElement: IGraphNodeJSON | IGraphEdgeJSON | null;

    constructor() {
        super();
        this.lineWidth = 5;
    }

    public graphEvents() {
        d3.select(this.rootEl).on("keydown", () => {
            if (d3.event.keyCode === 46) {
                d3.event.preventDefault();

                if (this.selectedElement != null) {
                    this.graph.nodes = this.graph.nodes.filter((node) => node !== this.selectedElement);
                    this.graph.links = this.graph.links.filter((link) => {
                        return link !== this.selectedElement &&
                            (link.source as any) !== this.selectedElement &&
                            (link.target as any) !== this.selectedElement;
                    });

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
            .on("click", (d: IGraphNodeJSON) => {
                d3.event.stopPropagation();

                if (d !== this.selectedElement) {
                    this.selectedElement = d;
                } else {
                    this.selectedElement = null;
                }

                this.update();
            });
    }

    public linkEvents() {
        super.linkEvents();

        this.linkContainer.selectAll("line")
            .on("click", (d: IGraphEdgeJSON) => {
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
            .filter((d: IGraphNodeJSON) => d === this.selectedElement)
            .select(":first-child").attr("fill", "pink");

        this.linkContainer.selectAll("line")
            .filter((d: IGraphEdgeJSON) => d === this.selectedElement)
            .attr("stroke", "pink");
    }

    private createNode(x: number, y: number) {
        this.graph.nodes.push({
            domain: ["1"],
            fx: x, fy: y,
            id: shortid.generate(),
            name: "???",
            type: "csp:variable",
            vx: 0, vy: 0,
            x, y,
        });

        this.forceSim.alphaTarget(0.3).restart();
        this.update();
    }
}

import * as d3 from "d3";
import * as shortid from "shortid";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import { Graph, IGraphEdge, IGraphNode } from "./Graph";

export default class GraphBuilder extends CSPGraphVisualizer {
    private static readonly DELETE_KEYS = [8, 46];

    /** The element that is currently selected and subject to actions like delete. */
    private selectedElement: IGraphNode | IGraphEdge | null;
    /** The selection representing the edge currently being created. */
    private tempEdge: d3.Selection<any, any, any, any>;
    /** True if an edge is in the process of being created. */
    private isCreatingEdge = false;
    /** Holds the node that the mouse is over at any given point of time.
     * null if the mouse is not over a node.
     */
    private nodeMousedOver: IGraphNode | null;

    private controlEl: HTMLElement;

    constructor(graph: Graph) {
        super(graph);
        this.lineWidth = 5;
    }

    public render(targetEl: HTMLElement) {
        const div1 = document.createElement("div");
        div1.setAttribute("tabindex", "0");
        targetEl.appendChild(div1);

        const div2 = document.createElement("div");
        div2.setAttribute("id", "graph-builder-controls");
        div2.innerHTML = "Name: <input type='text' id='input-name' /> Value: <input type='text' id='input-value' />";
        targetEl.appendChild(div2);
        document.getElementById("input-name").onchange = (e) => {
            if (this.selectedElement) {
                this.selectedElement.name = e.target.value;
                this.update();
            }
        };
        document.getElementById("input-value").onchange = (e) => {
            if (this.selectedElement && this.selectedElement.type === "csp:variable") {
                this.selectedElement.domain = e.target.value.split(",").map((a) => parseInt(a, 10));
                this.update();
            }
        };
        this.controlEl = div2;
        super.render(div1);

        this.tempEdge = this.svg.append("line")
            .attr("stroke", "black")
            .attr("stroke-width", 5)
            .lower();
    }

    public graphEvents() {
        d3.select(this.rootEl).on("keydown", () => {
            if (GraphBuilder.DELETE_KEYS.includes(d3.event.keyCode)) {
                d3.event.preventDefault();

                if (this.selectedElement != null) {
                    // This is either a node or edge, but we just try both for convenience
                    // As long as the id's don't overlap, this is safe
                    this.graph.removeNode(this.selectedElement.id);
                    delete this.graph.edges[this.selectedElement.id];

                    this.selectedElement = null;
                    this.update();
                }
            }
        });

        d3.select(this.rootEl).on("dblclick", () => {
            if (d3.event.shiftKey) {
                const [x, y] = d3.mouse(this.rootEl);
                this.createNode(x, y);
            }
        });
    }

    public nodeEvents() {
        super.nodeEvents();

        this.nodeContainer.selectAll("g")
            .on("click", (d: IGraphNode) => {
                if (d3.event.defaultPrevented) {
                    return;
                }

                this.selectedElement = d !== this.selectedElement ? d : null;
                this.update();

                if (this.selectedElement && this.selectedElement.type === "csp:variable") {
                    document.getElementById("input-name")!.value = this.selectedElement.name;
                    document.getElementById("input-value")!.value = this.selectedElement.domain;
                } else {
                    document.getElementById("input-name")!.value = "";
                    document.getElementById("input-value")!.value = "";
                }
            })
            .on("mouseover", (d: IGraphNode) => {
                this.nodeMousedOver = d;
            })
            .on("mouseout", (d: IGraphNode) => {
                if (this.nodeMousedOver === d) {
                    this.nodeMousedOver = null;
                }
            })
            .call(d3.drag<any, IGraphNode>()
                .on("start", () => {
                    this.isCreatingEdge = d3.event.sourceEvent.shiftKey;

                    if (this.isCreatingEdge) {
                        this.tempEdge
                            .attr("x1", d3.event.x)
                            .attr("y1", d3.event.y)
                            .attr("x2", d3.event.x)
                            .attr("y2", d3.event.y);
                        this.tempEdge.attr("style", "display: block;");
                    }
                })
                .on("drag", (d) => {
                    if (!this.isCreatingEdge) {
                        d.x = d3.event.x;
                        d.y = d3.event.y;

                        this.update();
                    } else {
                        const [x, y] = d3.mouse(this.rootEl);
                        this.tempEdge
                            .attr("x2", x)
                            .attr("y2", y);
                    }
                })
                .on("end", (initialNode) => {
                    if (this.isCreatingEdge && this.nodeMousedOver != null) {
                        this.tempEdge
                            .attr("x2", this.nodeMousedOver.x!)
                            .attr("y2", this.nodeMousedOver.y!);

                        // Only add the edge if the edge doesn't already exist, and isn't an edge to itself
                        if (initialNode.id !== this.nodeMousedOver.id &&
                            !this.graph.edgeExistsBetween(initialNode.id, this.nodeMousedOver.id)) {
                            this.graph.addEdge(initialNode.id, this.nodeMousedOver.id);
                            this.update();
                        }
                    }

                    this.tempEdge.attr("style", "display: none;");
                }));
    }

    public edgeEvents() {
        super.edgeEvents();

        this.edgeContainer.selectAll("line")
            .on("click", (d: IGraphEdge) => {
                d3.event.stopPropagation();
                this.selectedElement = d !== this.selectedElement ? d : null;
                document.getElementById("input-name")!.value = "";
                document.getElementById("input-value")!.value = "";
                this.update();
            });
    }

    public renderNodes() {
        super.renderNodes();

        this.nodeContainer.selectAll("g")
            .select(":first-child")
            .attr("fill", "white")
            .filter((d: IGraphNode) => d === this.selectedElement)
            .attr("fill", "pink");

        this.edgeContainer.selectAll("line")
            .attr("stroke", "black")
            .filter((d: IGraphEdge) => d === this.selectedElement)
            .attr("stroke", "pink");
    }

    private createNode(x: number, y: number) {
        const id = shortid.generate();
        this.graph.nodes[id] = {
            domain: [5],
            id,
            name: "???",
            type: "csp:variable",
            x,
            y,
        };

        this.update();
    }
}

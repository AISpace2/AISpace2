import * as d3 from "d3";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import { IGraphNode } from "./Graph";

export default class GraphBuilder extends CSPGraphVisualizer {
    private selectedNode: IGraphNode | null;

    public graphEvents() {
        d3.select(this.rootEl).on("keydown", () => {
            if (d3.event.keyCode === 46) {
                if (this.selectedNode != null) {
                    this.graph.nodes = this.graph.nodes.filter((node) => node !== this.selectedNode);
                    this.graph.links = this.graph.links.filter((link) => {
                        return (link.source as any) !== this.selectedNode && (link.target as any) !== this.selectedNode;
                    });

                    this.selectedNode = null;
                    this.update();
                }
            }
        });
    }

    public nodeEvents() {
        super.nodeEvents();

        this.nodeContainer.selectAll("g")
            .on("click", (d: IGraphNode) => {
                if (d !== this.selectedNode) {
                    this.selectedNode = d;
                } else {
                    this.selectedNode = null;
                }

                this.update();
            });
    }

    public renderNodes() {
        super.renderNodes();

        this.nodeContainer.selectAll("g")
            .filter((d: IGraphNode) => d === this.selectedNode)
            .select(":first-child").attr("fill", "pink");
    }
}

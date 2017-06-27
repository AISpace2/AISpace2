import * as d3 from "d3";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import {
    ICSPGraphNode,
    IGraphEdge,
    IGraphNode,
} from "./Graph";

export default class CSPGraphInteractor extends CSPGraphVisualizer {
    /** Callback whenever an arc is clicked. */
    public onArcClicked?: (varId: string, constId: string) => void;

    public nodeEvents() {
        super.nodeEvents();

        this.nodeContainer.selectAll("g").on("mouseover", function() {
            const groupSelection = d3.select(this);
            groupSelection.select("rect").attr("fill", "black");
            groupSelection.select("ellipse").attr("fill", "black");
            groupSelection.selectAll("text").attr("fill", "white");
        });

        this.nodeContainer.selectAll("g").on("mouseout", function() {
            const groupSelection = d3.select(this);
            groupSelection.select("rect").attr("fill", "white");
            groupSelection.select("ellipse").attr("fill", "white");
            groupSelection.selectAll("text").attr("fill", "black");
        });
    }

    public edgeEvents() {
        super.edgeEvents();

        const that = this;
        this.edgeContainer.selectAll("line").on("mouseover", function() {
            d3.select(this).attr("stroke-width", that.lineWidth + 5);
        });

        this.edgeContainer.selectAll("line").on("mouseout", function() {
            d3.select(this).attr("stroke-width", that.lineWidth);
        });

        this.edgeContainer.selectAll("line").on("click", (d: IGraphEdge) => {
            if (this.onArcClicked != null) {
                this.onArcClicked(this.graph.nodes[d.source].name, this.graph.nodes[d.dest].idx);
            }
        });
    }

    /**
     * Visually highlights the arc by giving it the corresponding style and colour.
     * @param arcId The ID of the arc (that connects a variable node and constraint) to highlight.
     *              If null, then all arcs will be higlighted.
     * @param style Sets the line width of the arc.
     * @param colour The colour of the arc. Any HTML colour string is valid, hex or named.
     *               If null, then the colour will be left unchange (i.e. same colour as before)
     */
    public highlightArc(arcId: string, style: "normal" | "bold", colour: string | null = null) {
        if (arcId != null) {
            const selectedLink = this.graph.edges[arcId];
            selectedLink.style = style;
            selectedLink.colour = colour || selectedLink.colour;
        } else {
            Object.values(this.graph.edges).forEach((edge) => {
                edge.style = style;
                edge.colour = colour || edge.colour;
            });
        }

        this.update();
    }

    /**
     * Sets the variable node identified by its ID to the corresponding domain.
     * @param nodeId The ID of the node whose domain is to be set. This node must be a variable node.
     * @param domain The new domain of the variable node.
     */
    public setDomain(nodeId: string, domain: string[]) {
        const sel = d3.select(`[id='${nodeId}']`);
        (sel.data()[0] as ICSPGraphNode).domain = domain;
        this.update();
    }
}

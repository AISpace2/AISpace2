import * as d3 from "d3";
import CSPGraphVisualizer from "./CSPGraphVisualizer";
import {
    ICSPGraphJSON,
    ICSPGraphNodeJSON,
    IGraphJSON,
    IGraphNodeJSON,
    IStyledGraphEdgeJSON,
} from "./Graph";

export default class CSPGraphInteractor extends CSPGraphVisualizer {
    /** Callback whenever an arc is clicked. */
    public onArcClicked?: (varId: string, constId: string) => void;
    /** Callback whenever a variable node is clicked. */
    public onVarClicked?: (varId: string) => void;

    public renderNodes() {
        super.renderNodes();

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

        this.nodeContainer.selectAll("g")
            .filter((d: ICSPGraphNodeJSON) => d.type === "csp:variable")
            .on("click", (d: ICSPGraphNodeJSON) => {
                if (this.onVarClicked != null) {
                    this.onVarClicked(d.name);
                }
            });
    }

    public renderLinks() {
        super.renderLinks();

        const that = this;
        this.linkContainer.selectAll("line").on("mouseover", function() {
            d3.select(this).attr("stroke-width", that.lineWidth + 5);
        });

        this.linkContainer.selectAll("line").on("mouseout", function() {
            d3.select(this).attr("stroke-width", that.lineWidth);
        });

        this.linkContainer.selectAll("line").on("click", (d: IStyledGraphEdgeJSON) => {
            if (this.onArcClicked != null) {
                this.onArcClicked((d.source as any as IGraphNodeJSON).name, (d.target as any).idx);
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
            const selectedLink = this.graph.links.find((link) => link.id === arcId) as IStyledGraphEdgeJSON;
            selectedLink.style = style;
            selectedLink.colour = colour || selectedLink.colour;
        } else {
            this.graph.links.forEach((link: IStyledGraphEdgeJSON) => {
                link.style = style;
                link.colour = colour || link.colour;
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
        (sel.data()[0] as ICSPGraphNodeJSON).domain = domain;
        this.update();
    }
}

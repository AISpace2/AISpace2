import {
    ICSPGraphJSON,
    ICSPGraphNodeJSON,
    IGraphJSON,
    IGraphNodeJSON,
    IStyledGraphEdgeJSON,
} from "./Graph";
import GraphVisualizer from "./GraphVisualizer";

export default class CSPGraphVisualizer extends GraphVisualizer {
    protected graph: ICSPGraphJSON;

    public renderNodes() {
        const updateSelection = this.nodeContainer
            .selectAll("g")
            .data(this.graph.nodes);

        const enterSelection = updateSelection
            .enter().append("g")
            .attr("id", (d) => d.id);

        const variableSelection = enterSelection.filter((d) => d.type === "csp:variable");
        const constraintSelection = enterSelection.filter((d) => d.type === "csp:constraint");

        variableSelection
            .append("ellipse")
            .attr("rx", 50)
            .attr("ry", 30)
            .attr("fill", "white")
            .attr("stroke", "black");

        constraintSelection
            .append("rect")
            .attr("width", 80)
            .attr("height", 40)
            .attr("x", -40)
            .attr("y", -20)
            .attr("fill", "white")
            .attr("stroke", "black");

        variableSelection.append("text")
            .text((d) => d.name)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .attr("y", -10);

        constraintSelection.append("text")
            .text((d) => d.name)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle");

        variableSelection
            .append("text")
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .attr("y", 10)
            .attr("class", "domain");

        updateSelection.merge(variableSelection)
            .selectAll(".domain")
            .text((d: ICSPGraphNodeJSON) => `{${d.domain.join()}}`);
    }

    public renderLinks() {
        const updateSelection = this.linkContainer
            .selectAll("line")
            .data(this.graph.links);

        updateSelection.enter().append("line")
            .merge(updateSelection)
            .attr("stroke-width", (d: IStyledGraphEdgeJSON) => d.style === "bold" ? this.lineWidth + 5 : this.lineWidth)
            .attr("stroke", (d: IStyledGraphEdgeJSON) => (d.colour != null) ? d.colour : "black");
    }
}

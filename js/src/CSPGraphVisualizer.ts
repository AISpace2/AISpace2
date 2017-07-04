import * as d3 from "d3";
import {
    Graph,
    ICSPGraphNode,
    IGraphEdge,
} from "./Graph";
import GraphVisualizer from "./GraphVisualizer";

export default class CSPGraphVisualizer extends GraphVisualizer {
    protected graph: Graph<ICSPGraphNode>;

    public renderNodes() {
        const updateSelection = this.nodeContainer
            .selectAll("g")
            .data(Object.values(this.graph.nodes), (node: ICSPGraphNode) => node.id);

        const enterSelection = updateSelection
            .enter().append("g")
            .attr("id", (d) => d.id);

        enterSelection
            .call(d3.drag<any, ICSPGraphNode>()
                .on("drag", (d, i, arr) => {
                    d.x = d3.event.x;
                    d.y = d3.event.y;

                    this.update();
                }));

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
            .attr("class", "name")
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

        const mergedSelection = updateSelection.merge(enterSelection);
        mergedSelection.attr("transform", (d) => `translate(${d.x!}, ${d.y!})`);
        mergedSelection.selectAll(".name").text((d) => d.name);
        mergedSelection.selectAll(".domain").text((d: ICSPGraphNode) => `{${d.domain.join()}}`);

        updateSelection.exit().remove();
    }

    public renderLinks() {
        super.renderLinks();

        const updateSelection = this.edgeContainer
            .selectAll("line")
            .data(Object.values(this.graph.edges), (d: IGraphEdge) => d.id);

        updateSelection.enter().append("line")
            .merge(updateSelection)
            .attr("stroke-width", (d: IGraphEdge) => d.style === "bold" ? this.lineWidth + 5 : this.lineWidth)
            .attr("stroke", (d: IGraphEdge) => (d.colour != null) ? d.colour : "black");

        updateSelection.exit().remove();
    }
}

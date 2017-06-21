import {
    CSPGraphJSON,
    GraphNodeJSON,
    CSPGraphNodeJSON,
    GraphJSON,
    StyledGraphEdgeJSON
} from './Graph';
import * as d3 from 'd3';
import {
    SimulationLinkDatum,
    SimulationNodeDatum
} from 'd3-force';
import * as Backbone from 'backbone';

export default class GraphVisualizer {
    protected graph: GraphJSON;
    width: number;
    height: number;
    /** Represents the root SVG element where the graph is drawn. */
    svg: d3.Selection<any, any, any, any>;
    /** A group where all links are drawn. */
    linkContainer: d3.Selection<any, SimulationLinkDatum<SimulationNodeDatum> & StyledGraphEdgeJSON, any, any>;
    /** A group where all nodes are drawn. */
    nodeContainer: d3.Selection<any, SimulationNodeDatum & GraphNodeJSON, any, any>;
    /** The normal width of the line to draw. */
    lineWidth: number = 2.0;

    render(graph: GraphJSON, targetEl: HTMLElement) {
        this.graph = graph;
        this.width = targetEl.clientWidth;
        this.height = this.width * 0.5;

        // Remove all children of target element to make this function idempotent
        d3.select(targetEl).selectAll('*').remove();

        this.svg = d3.select(targetEl)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        // Enable zoom and pan behaviour
        this.svg.append('rect')
            .attr('width', this.width)
            .attr('height', this.height)
            .style('fill', 'none')
            .style('pointer-events', 'all')
            .call(d3.zoom()
                .scaleExtent([1, 2.5])
                .on('zoom', () => {
                    this.linkContainer.attr('transform', d3.event.transform);
                    this.nodeContainer.attr('transform', d3.event.transform);
                }));

        // Called whenever node/link positions are updated (either by the force simulation or by dragging)
        const onTick = () => {
            this.linkContainer
                .selectAll('line')
                .data(this.graph.links)
                .attr('x1', d => ((d.source as SimulationNodeDatum).x) as number)
                .attr('y1', d => ((d.source as SimulationNodeDatum).y) as number)
                .attr('x2', d => ((d.target as SimulationNodeDatum).x) as number)
                .attr('y2', d => ((d.target as SimulationNodeDatum).y) as number);

            this.nodeContainer
                .selectAll('g')
                .data(this.graph.nodes)
                .each(d => {
                    d.x = Math.max(30, Math.min(this.width - 30, d.x));
                    d.y = Math.max(30, Math.min(this.height - 30, d.y));
                })
                .attr('transform', (d: SimulationNodeDatum) => `translate(${d.x}, ${d.y})`);
        };

        const forceSimulation = d3.forceSimulation(graph.nodes)
            .force('link', d3.forceLink()
                .id((node: GraphNodeJSON) => node.id)
                .links(graph.links)
                .distance(35)
                .strength(0.6))
            .force('charge', d3.forceManyBody().strength(-30))
            .force('center', d3.forceCenter(this.width / 2, this.height / 2))
            .force('collision', d3.forceCollide(75))
            .on('tick', onTick)
            .stop();

        this.linkContainer = this.svg.append('g')
            .attr('class', 'links');

        this.nodeContainer = this.svg.append('g')
            .attr('class', 'nodes');

        this.update();

        // Run simulation synchronously instead of asynchronously to prevent visual jitter
        for (let i = 0, ticksToSimulate = 300; i < ticksToSimulate; i++) {
            forceSimulation.tick();
            onTick();
        }

        // Fix all nodes, to prevent them from being moved by further simulations
        this.nodeContainer
            .selectAll('g')
            .data(this.graph.nodes)
            .each((d: SimulationNodeDatum) => {
                d.fx = d.x;
                d.fy = d.y;
            });

        // Enable dragging of nodes
        this.nodeContainer
            .selectAll('g')
            .data(this.graph.nodes)
            .call(<any>d3.drag()
                .on('start', () => {
                    // The 'simulation' must be started even though all the node positions are fixed,
                    // or the node positions will not be updated
                    forceSimulation.alphaTarget(0.3).restart();
                })
                .on('drag', (d: SimulationNodeDatum) => {
                    d.fx = Math.max(30, Math.min(this.width - 30, d3.event.x));
                    d.fy = Math.max(30, Math.min(this.height - 30, d3.event.y));
                })
                .on('end', () => {
                    forceSimulation.stop();
                }));
    }

    renderNodes() {
        const updateSelection = this.nodeContainer
            .selectAll('g')
            .data(this.graph.nodes);

        updateSelection.enter().append('circle')
            .attr('r', 30)
            .attr('fill', 'white')
            .attr('stroke', 'black');

        updateSelection.enter().append('text')
            .attr('text-anchor', 'middle')
            .attr('alignment-baseline', 'middle')
            .merge(updateSelection)
            .text(d => d.name);
    }

    renderLinks() {
        const updateSelection = this.linkContainer
            .selectAll('line')
            .data(this.graph.links);

        updateSelection.enter().append('line')
            .merge(updateSelection)
            .attr('stroke-width', this.lineWidth)
            .attr('stroke', 'black');
    }

    /**
    * Updates the graph by re-binding to the data and re-rendering nodes and edges.
    */
    update() {
        this.renderLinks();
        this.renderNodes();
    }
}

export class CSPGraphVisualizer extends GraphVisualizer {
    protected graph: CSPGraphJSON;

    renderNodes() {
        const updateSelection = this.nodeContainer
            .selectAll('g')
            .data(this.graph.nodes);

        const enterSelection = updateSelection
            .enter().append('g')
            .attr('id', d => d.id);

        const variableSelection = enterSelection.filter(d => d.type === 'csp:variable');
        const constraintSelection = enterSelection.filter(d => d.type === 'csp:constraint');

        variableSelection
            .append('ellipse')
            .attr('rx', 50)
            .attr('ry', 30)
            .attr('fill', 'white')
            .attr('stroke', 'black');

        constraintSelection
            .append('rect')
            .attr('width', 80)
            .attr('height', 40)
            .attr('x', -40)
            .attr('y', -20)
            .attr('fill', 'white')
            .attr('stroke', 'black');

        variableSelection.append('text')
            .text(d => d.name)
            .attr('text-anchor', 'middle')
            .attr('alignment-baseline', 'middle')
            .attr('y', -10);

        constraintSelection.append('text')
            .text(d => d.name)
            .attr('text-anchor', 'middle')
            .attr('alignment-baseline', 'middle');

        variableSelection
            .append('text')
            .attr('text-anchor', 'middle')
            .attr('alignment-baseline', 'middle')
            .attr('y', 10)
            .attr('class', 'domain');

        updateSelection.merge(variableSelection)
            .selectAll('.domain')
            .text((d: CSPGraphNodeJSON) => `{${d.domain.join()}}`);
    }

    renderLinks() {
        const updateSelection = this.linkContainer
            .selectAll('line')
            .data(this.graph.links);

        updateSelection.enter().append('line')
            .merge(updateSelection)
            .attr('stroke-width', (d: StyledGraphEdgeJSON) => d.style === 'bold' ? this.lineWidth + 5 : this.lineWidth)
            .attr('stroke', (d: StyledGraphEdgeJSON) => (d.colour != null) ? d.colour : 'black');
    }
}


export class CSPGraphInteractor extends CSPGraphVisualizer {
    /** Callback whenever an arc is clicked. */
    onArcClicked?: (varId: string, constId: string) => void;

    renderNodes() {
        super.renderNodes();

        this.nodeContainer.selectAll('g').on('mouseover', function () {
            const groupSelection = d3.select(this);
            groupSelection.select('rect').attr('fill', 'black');
            groupSelection.select('ellipse').attr('fill', 'black');
            groupSelection.selectAll('text').attr('fill', 'white');
        });

        this.nodeContainer.selectAll('g').on('mouseout', function () {
            const groupSelection = d3.select(this);
            groupSelection.select('rect').attr('fill', 'white');
            groupSelection.select('ellipse').attr('fill', 'white');
            groupSelection.selectAll('text').attr('fill', 'black');
        });

        this.nodeContainer.selectAll('g').on('dblclick', function () {
            const groupSelection = d3.select(this);

        });
    }

    renderLinks() {
        super.renderLinks();

        const that = this;
        this.linkContainer.selectAll('line').on('mouseover', function () {
            d3.select(this).attr('stroke-width', that.lineWidth + 5);
        });

        this.linkContainer.selectAll('line').on('mouseout', function () {
            d3.select(this).attr('stroke-width', that.lineWidth);
        });

        this.linkContainer.selectAll('line').on('click', (d: StyledGraphEdgeJSON) => {
            if (this.onArcClicked != null) {
                this.onArcClicked((d.source as any as GraphNodeJSON).name, (d.target as any).idx);
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
    highlightArc(arcId: string, style: 'normal' | 'bold', colour: string | null = null) {
        if (arcId != null) {
            const link = this.graph.links.find(link => link.id === arcId) as StyledGraphEdgeJSON;
            link.style = style;
            link.colour = colour || link.colour;
        } else {
            this.graph.links.forEach((link: StyledGraphEdgeJSON) => {
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
    setDomain(nodeId: string, domain: string[]) {
        let sel = d3.select(`[id='${nodeId}']`);
        (sel.data()[0] as CSPGraphNodeJSON).domain = domain;
        this.update();
    }
}
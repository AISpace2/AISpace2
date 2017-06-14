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
    width: number;
    height: number;
    protected graph: GraphJSON;
    /** Represents the root SVG element where the graph is drawn. */
    svg: d3.Selection<any, any, any, any>;
    /** A group where all links are drawn. */
    linkContainer: d3.Selection<any, any, any, any>;
    /** A group where all nodes are drawn. */
    nodeContainer: d3.Selection<any, SimulationNodeDatum & GraphNodeJSON, any, any>;
    lineWidth: number = 2.0;

    render(graph: GraphJSON, targetEl: HTMLElement) {
        this.graph = graph;

        // Ensures the target element is in the DOM (essentially document.ready) so we can get its width
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
                .attr('x1', (d: SimulationLinkDatum<GraphNodeJSON>) => (d.source as SimulationNodeDatum).x)
                .attr('y1', (d: SimulationLinkDatum<GraphNodeJSON>) => (d.source as SimulationNodeDatum).y)
                .attr('x2', (d: SimulationLinkDatum<GraphNodeJSON>) => (d.target as SimulationNodeDatum).x)
                .attr('y2', (d: SimulationLinkDatum<GraphNodeJSON>) => (d.target as SimulationNodeDatum).y);

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

        updateSelection.merge(enterSelection)
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
            .attr('stroke', (d: StyledGraphEdgeJSON) => (d.colour != null && d.colour !== 'na') ? d.colour : 'black');
    }
}


export class CSPGraphInteractor extends CSPGraphVisualizer {
    eventBus: Backbone.Events;

    constructor(eventBus: Backbone.Events) {
        super();
        this.eventBus = eventBus;
    }

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

        this.nodeContainer.selectAll('g').on('dblclick', function() {
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
            this.eventBus.trigger('constraint:click', {
                constId: (d.target as any).idx,
                varId: (d.source as any as GraphNodeJSON).name
            });
        });
    }

    highlightArc(varName: string, consName: string, style: 'normal' | 'bold', colour: string) {
        if (varName === 'all' && consName === 'all') {
            this.graph.links.forEach((link: StyledGraphEdgeJSON) => {
                link.style = style;
                link.colour = colour;
            });

            this.update();
            return;
        }

        let constraint = this.graph.nodes.find(el => el.name === consName);

        if (constraint != null) {
            let link = (this.graph.links as StyledGraphEdgeJSON[]).filter(link => (link.target as any as GraphNodeJSON).id === constraint.id)
                .find(link => (link.source as any as GraphNodeJSON).name === varName);

            link.style = style;
            if (colour !== 'na') {
                link.colour = colour;
            }

            this.update();
        }
    }

    setDomain(varName: string, domain: string[]) {
        let node = this.graph.nodes.find(node => node.name === varName);

        let sel = d3.select(`[id='${node.id}']`);
        (sel.data()[0] as CSPGraphNodeJSON).domain = domain;
        this.update();
    }
}
const shortid = require('shortid');

export class Graph {
    description: string;
    private _nodes: {[key: string]: GraphNode};
    private _edges: {[key: string]: CompactGraphEdge};

    constructor() {
        this._nodes = {};
        this._edges = {};
    }

    addNode(node: GraphNode) {
        this._nodes[node.id] = node;
        return this;
    }

    removeNode(node: GraphNode) {
        delete this._nodes[node.id];
        return this;
    }

    addEdge(edge: GraphEdge): this;
    addEdge(node1: GraphNode, node2: GraphNode, id?: string): this;
    addEdge(node1Id: string, node2Id: string, id?: string): this;
    addEdge(p1: any, p2?: any, p3?: any) {
        if (p1 instanceof GraphEdge) {
            this.addNode(p1.source);
            this.addNode(p1.target);
            this._edges[p1.id] = { id: p1.id, sourceId: p1.source.id, targetId: p1.target.id };
        } else if (p1 instanceof GraphNode) {
            this.addEdge(new GraphEdge(p1, p2, p3));
        } else if (typeof p1 === 'string') {
            const node1 = this._nodes[p1];
            const node2 = this._nodes[p2];
            this.addEdge(new GraphEdge(node1, node2, p3));
        }

        return this;
    }

    removeEdge(edge: GraphEdge) {
        delete this._edges[edge.id];
        return this;
    }

    *nodes() {
        for (let id of Object.keys(this._nodes)) {
            yield this._nodes[id];
        }
    }

    *edges(): IterableIterator<GraphEdge> {
        for (let id of Object.keys(this._edges)) {
            const compactEdge = this._edges[id];
            yield new GraphEdge(this._nodes[compactEdge.sourceId], this._nodes[compactEdge.targetId], compactEdge.id);
        }
    }
}

export class GraphNode {
    id: string;
    name: string;
    type: string;

    constructor(id: string = shortid.generate()) {
        this.id = id;
    }

    serializeToJSON(): GraphNodeJSON {
        return { id: this.id, name: this.name, type: 'default' };
    }
}

export type CSPNodeTypes = 'csp:variable' | 'csp:constraint';
export class CSPGraphNode extends GraphNode {
    type: CSPNodeTypes;

    constructor(type: CSPNodeTypes, id?: string) {
        super(id);
        this.type = type;
    }

    serializeToJSON(): GraphNodeJSON {
        return {
            ...super.serializeToJSON(),
            type: this.type
        };
    }
}

type CompactGraphEdge = { id: string, sourceId: string, targetId: string };

class GraphEdge {
    source: GraphNode;
    target: GraphNode;
    id: string;

    constructor(source: GraphNode, target: GraphNode, id: string = shortid.generate()) {
        this.source = source;
        this.target = target;
        this.id = id;
    }

    serializeToJSON(): GraphEdgeJSON {
        return { id: this.id, source: this.source.id, target: this.target.id };
    }
}

export interface GraphJSON {
    nodes: GraphNodeJSON[]
    links: GraphEdgeJSON[]
}

export interface GraphNodeJSON {
    id: string
    name: string
    type: string
    [key: string]: any
}

export interface CSPGraphNodeJSON extends GraphNodeJSON {
    domain: string[];
}

export interface CSPGraphJSON {
    nodes: CSPGraphNodeJSON[]
    links: GraphEdgeJSON[]
}

export interface GraphEdgeJSON {
    id: string
    source: string
    target: string
    name: string;
}


interface GraphExporter {
    exportGraph(graph: Graph): any;
}

export class JSONGraphExporter implements GraphExporter {
    exportGraph(graph: Graph): GraphJSON {
        let json: GraphJSON = { nodes: [], links: [] };

        for (let node of graph.nodes()) {
            json.nodes.push(node.serializeToJSON())
        }

        for (let edge of graph.edges()) {
            json.links.push(edge.serializeToJSON())
        }

        return json;
    }
}

interface GraphImporter {
    importGraph(graph: string | object): Graph
}

export class JSONGraphImporter implements GraphImporter {
    importGraph(g: GraphJSON): Graph {
        let graph = new Graph();
        for (let node of g.nodes) {
            if (node.type === 'csp:constraint') {
                const gNode = new CSPGraphNode('csp:constraint', node.id);
                gNode.name = node.name;
                graph.addNode(gNode);
            } else if (node.type === 'csp:variable') {
                const gNode = new CSPGraphNode('csp:variable', node.id);
                gNode.name = node.name;
                graph.addNode(gNode);
            }
        }

        for (let edge of g.links) {
            graph.addEdge(edge.source, edge.target);
        }

        return graph;
    }
}

let a = new CSPGraphNode('csp:variable');
a.name = 'A';
let b = new CSPGraphNode('csp:variable');
b.name = 'B';
let c = new CSPGraphNode('csp:variable');
c.name = 'C';

let altb = new CSPGraphNode('csp:constraint');
altb.name = 'A < B';
let bltc = new CSPGraphNode('csp:constraint');
bltc.name = 'B < C';

let aaltb = new GraphEdge(a, altb);
let altbb = new GraphEdge(b, altb);

let bbltc = new GraphEdge(b, bltc);
let bltcc = new GraphEdge(c, bltc);

export const csp1 = new Graph()
    .addEdge(aaltb)
    .addEdge(altbb)
    .addEdge(bbltc)
    .addEdge(bltcc);
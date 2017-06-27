import * as shortid from "shortid";

export interface IGraphNode {
    id: string;
    name: string;
    type: string;
    x?: number;
    y?: number;
    [key: string]: any;
}

export type CSPNodeTypes = "csp:variable" | "csp:constraint";
export interface ICSPGraphNode extends IGraphNode {
    type: CSPNodeTypes;
    domain: number[] | string[];
}

export interface IGraphEdge {
    source: string;
    dest: string;
    id: string;
    name?: string;
    [key: string]: any;
}

export interface IGraph<TNode extends IGraphNode = IGraphNode, TEdge extends IGraphEdge = IGraphEdge> {
    nodes: { [key: string]: TNode };
    edges: { [key: string]: TEdge };
}

export class Graph<TNode extends IGraphNode = IGraphNode, TEdge extends IGraphEdge = IGraphEdge>
    implements IGraph<TNode, TEdge> {

    public static fromJSON(json: IGraph): Graph {
        return new Graph(json.nodes, json.edges);
    }

    public nodes: { [key: string]: TNode };
    public edges: { [key: string]: TEdge };

    constructor(nodes: { [key: string]: TNode } = Object.create(null),
                edges: { [key: string]: TEdge } = Object.create(null)) {
        this.nodes = nodes;
        this.edges = edges;
    }

    /**
     * Returns true if an edge exists in the graph that connects the two nodes.
     *
     * Note that this function is invariant to the order in which nodes are passed.
     *
     * @param node1Id The id of the first node of the possible edge.
     * @param node2Id The id of the second node of the possible edge.
     */
    public edgeExistsBetween(node1Id: string, node2Id: string) {
        for (const edge of Object.values(this.edges)) {
            if ((edge.source === node1Id && edge.dest === node2Id) ||
                (edge.source === node2Id && edge.dest === node1Id)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Adds an edge to the graph connecting two nodes. If either node is not already in the graph,
     * this function returns false, and the graph is unmodified.
     *
     * @param node1Id The source of the edge.
     * @param node2Id The destination of the edge.
     * @param opts Other properties that will be added to the edge.
     */
    public addEdge(node1Id: string, node2Id: string, opts: object = {}) {
        if (this.nodes[node1Id] == null || this.nodes[node2Id] == null) {
            return false;
        }

        const edgeId = shortid.generate();
        const edge = {
            dest: node2Id,
            id: edgeId,
            source: node1Id,
            ...opts,
        } as TEdge;
        this.edges[edgeId] = edge;

        return true;
    }

    /**
     * Removes a node from the graph, along with any edges attached to it.
     * @param nodeId The id of the node to remove.
     */
    public removeNode(nodeId: string) {
        delete this.nodes[nodeId];

        for (const edge of Object.values(this.edges)) {
            if (edge.source === nodeId || edge.dest === nodeId) {
                delete this.edges[edge.id];
            }
        }
    }

    public toJSON(): IGraph {
        return {
            edges: this.edges,
            nodes: this.nodes,
        };
    }
}

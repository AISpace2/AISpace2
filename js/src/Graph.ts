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
    domain: string[];
}

export interface IGraphEdge {
    source: string;
    dest: string;
    id: string;
    name: string;
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

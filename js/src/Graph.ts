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

export interface IGraphEdgeJSON {
    source: string;
    dest: string;
    id: string;
    name?: string;
    [key: string]: any;
}

export interface IGraphEdge {
    source: IGraphNode;
    target: IGraphNode;
    id: string;
    name?: string;
    [key: string]: any;
}

export interface IGraph<TNode extends IGraphNode = IGraphNode, TEdge extends IGraphEdge = IGraphEdge> {
    nodes: TNode[];
    edges: TEdge[];
}

export class Graph<TNode extends IGraphNode = IGraphNode, TEdge extends IGraphEdge = IGraphEdge>
    implements IGraph<TNode, TEdge> {

    public static fromJSON(json: any): Graph {
        const newGraph = {
            edges: [] as any[],
            nodes: [] as IGraphNode[],
        };

        for (const node of Object.values(json.nodes)) {
            newGraph.nodes.push(node);

            if (node.type === "csp:constraint") {
                node.constraint = "lt";
            }
        }

        for (const edge of Object.values(json.edges)) {
            // Find source
            newGraph.edges.push({
                id: edge.id,
                source: json.nodes[edge.source],
                style: {} ,
                target: json.nodes[edge.dest],
            });
        }

        return new Graph(newGraph.nodes, newGraph.edges);
    }

    public nodes: TNode[];
    public edges: TEdge[];

    constructor(nodes: TNode[] = [],
                edges: TEdge[] = []) {
        this.nodes = nodes;
        this.edges = edges;
    }

    public toJSON(): IGraph {
        return {
            edges: this.edges,
            nodes: this.nodes,
        };
    }
}

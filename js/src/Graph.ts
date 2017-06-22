export interface IGraphNode {
    id: string;
    name: string;
    type: string;
}

export type CSPNodeTypes = "csp:variable" | "csp:constraint";
export interface ICSPGraphNode extends IGraphNode {
    type: CSPNodeTypes;
}

interface IGraphEdge {
    source: IGraphNode;
    target: IGraphNode;
    id: string;
    name: string;
}

export interface IGraphJSON {
    nodes: IGraphNodeJSON[];
    links: IGraphEdgeJSON[];
}

export interface IGraphNodeJSON {
    id: string;
    name: string;
    type: string;
    [key: string]: any;
}

export interface ICSPGraphNodeJSON extends IGraphNodeJSON {
    type: "csp:variable" | "csp:constraint";
    domain: string[];
}

export interface ICSPGraphJSON {
    nodes: ICSPGraphNodeJSON[];
    links: IGraphEdgeJSON[];
}

export interface IGraphEdgeJSON {
    id: string;
    source: string;
    target: string;
    name: string;
}

export interface IStyledGraphEdgeJSON extends IGraphEdgeJSON {
    style: string | null;
    colour: string | null;
}

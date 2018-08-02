import BayesNode from "./BayesNode";

export default class BayesNet {
  public graph: [BayesNode];

  constructor(graph: [BayesNode]) {
    this.graph = graph;
  }
}

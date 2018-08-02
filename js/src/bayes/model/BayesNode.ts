import CPTCell from "./CPTCell";

export default class BayesNode {
  public name: string;
  public parents: [string];
  public domain: [any];
  public cptTable: [CPTCell];

  constructor(
    name: string,
    parents: [string],
    domain: [any],
    cptTable: [CPTCell]
  ) {
    this.name = name;
    this.parents = parents;
    this.domain = domain;
    this.cptTable = cptTable;
  }
}

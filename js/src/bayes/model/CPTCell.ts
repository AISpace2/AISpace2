// Conditional Probability Table Unit Class
import Evidence from "./Evidence";

export default class CPTCell {
  public evidences: [Evidence];
  public trueProbability: number;
  public falseProbability: number;

  constructor(e: [Evidence]) {
    this.evidences = e;
  }
}

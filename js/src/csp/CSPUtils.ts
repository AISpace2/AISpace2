import { ICSPGraphNode } from "../Graph";

/** Returns a formatted string representing the domain of a variable node. */
export function domainText(node: ICSPGraphNode) {
  return `{${node.domain!.join(",")}}`;
}

/** Returns a formatted string representing the constraint of a constraint node. */
export function constraintText(node: ICSPGraphNode) {
  if (node.name != null) {
    if (node.constraintParents?.length != null && node.constraintParents?.length !== 0) {
      var cp = node.constraintParents.join(", ");
      
      return `${node.name} (${cp})`;
    }
    return `${node.name} (?)`;
  }


  return "N/A";
}

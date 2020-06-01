import { ICSPGraphNode } from "../Graph";

/** Returns a formatted string representing the domain of a variable node. */
export function domainText(node: ICSPGraphNode) {
  if(typeof node.domain![0] === "string"){
    return `string: ${node.domain!.join(", ")}`;
  } else if(typeof node.domain![0] === "number"){
    return `number: ${node.domain!.join(", ")}`;
  } else {
    return `boolean: ${node.domain!.join(", ")}`
  }
}

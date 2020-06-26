import { ICSPGraphNode } from "../Graph";

/** Returns a formatted string representing the domain of a variable node. */
export function domainText(node: ICSPGraphNode) {
  if(typeof node.domain![0] === "string"){
    var domaintemp: string[]
    domaintemp = []
    for (let i = 0; i < node.domain!.length; i++) {
      const element = node.domain![i];
      var temp = `"` + element + `"`
      console.log(temp)
      domaintemp.push(temp)      
    }
    return ` {${domaintemp.join(", ")}} `;
  } else if(typeof node.domain![0] === "number"){
    return ` {${node.domain!.join(", ")}} `;
  } else if(typeof node.domain![0] === "boolean"){
    return ` {${node.domain!.join(", ")}} `;
  } else {
    return ` {${node.domain!.join(", ")}} `;
  }
}


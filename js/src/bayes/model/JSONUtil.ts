import BayesNode from "./BayesNode";
import CPTCell from "./CPTCell";
import Evidence from "./Evidence";

export default class JSONUtil {

  public toJSON(bayes: BayesNode) {

  }

  public static fromJSON(json: object) {

    // example node: {
    //        "name": "Alarm",
    //        "domain": ["True", "False"]
    // }
    for (let node of json.node) {
      

    }

    // example p: {
    //         "name": "Alarm",
    //         "parents": ["Fire, Tamper"],
    //         "evidences": [((0.9999, 0.0001), (0.15, 0.85)), ((0.01, 0.99), (0.5, 0.5))]
    // }
    for (let p of json.probability) {

    }
    return
  }
}







// from bayesjsonbridge.py
// JSON EXAMPLE
// {
//     "node": [{"name": "Alarm", "domain": ["True", "False"]},
//              {"name": "Fire", "domain": ["True", "False"]}],
//
//     "probability": [{
//         "name": "Alarm",
//         "parents": ["Fire, Tamper"],
//         "evidences": [((0.9999, 0.0001), (0.15, 0.85)), ((0.01, 0.99), (0.5, 0.5))]
// }]}


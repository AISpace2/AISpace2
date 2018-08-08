from aipython.probGraphicalModels import Belief_network
from aipython.probFactors import Prob
from aipython.probVariables import Variable

def bayes_to_json(bayesNet, widget_model=None):
    # Converts a Python Belief_network instance to a dictionary representable as JSON.
    #
    # Args:
    #     bayesNet (aipython.probGraphicalModels): The Belief_network instance to convert to a dictionary.
    #     widget_model: Instance of widget model passed by ipywidgets during conversion. Never used; you can ignore it.
    #
    # Returns:
    #     (dict or None):
    #         A Belief_network that is representable in JSON. None if no bayesNet was provided.
    #         This means the dictionary has no references to object instances.
    # Args:
    #     variables: list of Variable (Variable from probVariables.py)
    # Returns:
    #     List of variable dictionary
    def parseNode(variables, factors):
        nodes = [{'id': str(hash(var.name)),
                  'name': var.name,
                  'domain': var.domain,
                  'parents': [],
                  'evidences': []
                  } for var in variables]

        nodesMap = {node["name"]: index for index, node in enumerate(nodes)}

        for f in factors:
            nodeForF = nodes[nodesMap[f.child.name]]
            nodeForF["parents"] = [p.name for p in f.parents]
            nodeForF["evidences"] = f.values

        return nodes

    # Args:
    #     factors: list of Prob (Prob from probFactors.py)
    # Example Constructor: Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])
    # Returns:
    #     List of probability dictionary
    def parseProbability(factors):
        # returns evidences array of tuples
        edges = []


        for prob in factors:
            for parent in prob.parents:
                edge = {
                    #'name': prob.child.name,
                    'source': str(hash(parent.name)),
                    'target': str(hash(prob.child.name)),
                    'id': str(hash(parent.name+prob.child.name))
                }
                edges.append(edge)

        return edges

    if not bayesNet:
        return None

    bayes = {"nodes": parseNode(bayesNet.variables, bayesNet.factors),
             "edges": parseProbability(bayesNet.factors)}

    return bayes

def json_to_bayes_problem(json, widget_model=None):
    if not json:
        return None

    listOfVars = [Variable(var["name"], var["domain"]) for var in json["nodes"]]

    # extra data for easy name to Variable object search for Probability
    dictionary = [{var.name: var} for var in listOfVars]
    listOfProb = []

    for node in json["nodes"]:
        primaryObj = dictionary[node["name"]]
        parentsObj = [dictionary[name] for name in node["parents"]]
        listOfProb.append(Prob(primaryObj, parentsObj, node["evidences"]))

    return Belief_network(listOfVars, listOfProb)

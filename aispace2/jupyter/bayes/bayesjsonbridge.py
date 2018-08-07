from aipython.probGraphicalModels import Belief_network
from aipython.probFactors import Prob
from aipython.probVariables import Variable

# Example output
# {
#     "node": [{"name": "Alarm", "domain": ["True", "False"]},
#              {"name": "Fire", "domain": ["True", "False"]}],
#
#     "probability": [{
#         "name": "Alarm",
#         "parents": ["Fire, Tamper"],
#         "evidences": [0.9999, 0.0001, 0.15, 0.85, 0.01, 0.99, 0.5, 0.5]
# }]}
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
    # Example Output: [{"name": "Alarm", "domain": [True, False]}
    def parseNode(variables):
        return [{'id': str(hash(var.name)), 'name': var.name, 'domain': var.domain} for var in variables]

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
        # return [{
        #     "id":
        #     "name": prob.child.name,
        #     "parents": [p.name for p in prob.parents],
        #     "evidences": prob.values,
        # } for prob in factors]

    if not bayesNet:
        return None

    #node_map = {str(n): str(hash(n.name)) for n in bayesNet.variables}
    bayes = {"nodes": parseNode(bayesNet.variables),
             "edges": parseProbability(bayesNet.factors)}

    return bayes

# TODO
def json_to_bayes_problem(json, widget_model=None):
    if not json:
        return None

    listOfVars = [Variable(var["name"], var["domain"]) for var in json["node"]]

    # extra data for easy name to Variable object search for Probability
    dictionary = [{var.name: var} for var in listOfVars]
    listOfProb = []

    for prob in json["probability"]:
        primaryObj = dictionary[prob["name"]]
        parentsObj = [dictionary[name] for name in prob["parents"]]
        listOfProb.append(Prob(primaryObj, parentsObj, prob["evidences"]))

    listOfVars = [Variable(var["name"], var["domain"]) for var in json["node"]]
    return Belief_network(listOfVars, listOfProb)

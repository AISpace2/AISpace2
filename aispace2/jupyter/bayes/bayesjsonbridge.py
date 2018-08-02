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
#         "evidences": [((0.9999, 0.0001), (0.15, 0.85)), ((0.01, 0.99), (0.5, 0.5))]
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
        return [{"name": var.name, "domain": var.domain} for var in variables]

    # Args:
    #     factors: list of Prob (Prob from probFactors.py)
    # Example Constructor: Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])
    # Returns:
    #     List of probability dictionary
    # Example Output: [{
    #     #         "name": "Alarm",
    #     #         "parents": ["Fire, Tamper"],
    #     #         "evidences": [((0.9999, 0.0001), (0.15, 0.85)), ((0.01, 0.99), (0.5, 0.5))],
    #     # }]
    def parseProbability(factors):
        # returns evidences array of tuples
        def parseCPT(cpt, numOfParents):
            for i in range(numOfParents):
                cpt = list(zip(cpt, cpt[1:]))[::2]
            return cpt

        return [{
            "name": prob.child.name,
            "parents": [p.name for p in prob.parents],
            "evidences": parseCPT(prob.values, len(prob.parents))
        } for prob in factors]

    if not bayesNet:
        return None

    bayes = {"node": parseNode(bayesNet.variables),
             "probability": parseProbability(bayesNet.factors)}

    return bayes

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
        listOfCP = prob["evidences"]

        # flatten the list of variable size tuples based on number of parents
        for i in range(len(prob["parents"])):
            listOfCP = list(sum(listOfCP, ()))

        listOfProb.append(Prob(primaryObj, parentsObj, listOfCP))

    listOfVars = [Variable(var["name"], var["domain"]) for var in json["node"]]
    return Belief_network(listOfVars, listOfProb)





    # JSON EXAMPLE
    # {
    #     "node": [{"name": "Alarm", "domain": ["True", "False"]},
    #              {"name": "Fire", "domain": ["True", "False"]}],
    #
    #     "probability": [{
    #         "name": "Alarm",
    #         "parents": ["Fire, Tamper"],
    #         "evidences": [((0.9999, 0.0001), (0.15, 0.85)), ((0.01, 0.99), (0.5, 0.5))]
    # }]}

    # USAGE INSTANCE OF PYTHON GRAPH
    # boolean = [False, True]
    # A = Variable("A", boolean)
    # B = Variable("B", boolean)
    # C = Variable("C", boolean)
    #
    # f_a = Prob(A, [], [0.4, 0.6])
    # f_b = Prob(B, [A], [0.9, 0.1, 0.2, 0.8])
    # f_c = Prob(C, [B], [0.5, 0.5, 0.3, 0.7])
    #
    # Belief_network([A, B, C], [f_a, f_b, f_c])

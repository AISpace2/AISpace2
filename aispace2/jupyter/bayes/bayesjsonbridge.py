from aipython.probGraphicalModels import Belief_network
from aipython.probFactors import Prob
from aipython.probVariables import Variable

def bayes_problem_to_json(bayesNet, widget_model=None):
    """Converts a Python Belief_network instance to a dictionary representable as JSON.

    Args:
       bayesNet (aipython.probGraphicalModels): The Belief_network instance to convert to a dictionary.
        widget_model: Instance of widget model passed by ipywidgets during conversion. Never used; you can ignore it.

    Returns:
        (dict or None):
            A Belief_network that is representable in JSON. None if no bayesNet was provided.
            This means the dictionary has no references to object instances.
    Args:
        variables: list of Variable (Variable from probVariables.py)
    Returns:
        List of variable dictionary"""
    def parseNode(variables, factors):
        nodes = []
        for var in variables:
           nodes.append({
                'id': str(hash(var.name)),
                'name': var.name,
                'domain': var.domain,
                'parents': [],
                'evidences': []
           })
           if var.name in bayesNet.positions:
               nodes[-1]['x'] = bayesNet.positions[var.name][0]
               nodes[-1]['y'] = bayesNet.positions[var.name][1]

        nodesMap = {node["name"]: index for index, node in enumerate(nodes)}

        for f in factors:
            nodeForF = nodes[nodesMap[f.child.name]]
            nodeForF["parents"] = [p.name for p in f.parents]
            nodeForF["evidences"] = f.values

        return nodes

    def parseProbability(factors):
        """Args:
           factors: list of Prob (Prob from probFactors.py)
           Example Constructor: Prob(Re,[Le],[0.99, 0.01, 0.25, 0.75])
           Returns: List of probability dictionary"""

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

def bayes_problem_to_python_code(problem):
    """Converts the JSON representation of a Belief_network into Python code.
    Example:
        ::
            >>> bayes_problem_to_python_code(problem)
            'from aipython.probGraphicalModels import Belief_network
             from aipython.probVariables import Variable
             from aipython.probFactors import Prob
            problem = Belief_network([Variable("A",boolean),Variable("B",boolean)],
                [Prob(Variable("A",boolean),[],[0.9,0.1]),Prob(Variable("B",boolean),[Variable("A",boolean)],[0.9,0.1,0.05,0.95])'

    Args:
        problem (aipython.probGraphicalModels.Belief_network):
            The bayes problem to convert to Python code.

    Returns:
        (string):
            A string of Python code that, when executed, recinstructs to the bayes problem given.
    """
    var_strings = []
    for variable in problem.vars:
        name = variable.name
        domain = variable.domain
        var_strings.append("Variable({},{})".format(name, domain))

    prob_strings = []
    for prob in problem.listOfProb:
        child = prob.child
        parents = prob.parents
        cpt = prob.cpt
        prob_strings.append("Prob({},{},{})".format(child, parents, cpt))
    positions = problem.positions

    template = """from aipython.probGraphicalModels.Belief_network import Belief_network
from aipython.probVariables import Variable
from aipython.probFactors import Prob\n
bayes_problem = Belief_network(
    vars=[$vars],
    factors=[$probs],
    positions=$positions)"""

    return Template(template).substitute(
        vars=', '.join(var_strings),
        prob=', '.join(prob_strings),
        positions=positions)

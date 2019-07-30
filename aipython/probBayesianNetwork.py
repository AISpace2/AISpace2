from aispace2.jupyter.bayes import Displayable


class Bayesian_Network(Displayable):
    def __init__(self, problem):
        self.problem = problem
        self.decimal_place = 2
        super().__init__()

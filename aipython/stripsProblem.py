# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python3 code Version 0.7.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en


class Strips(object):
    def __init__(self, preconditions, effects):
        """
        defines the STRIPS represtation for an action:
        * preconditions is feature:value dictionary that must hold
        for the action to be carried out
        * effects is a feature:value map that this action makes
        true. The action changes the value of any feature specified
        here, and leaves other properties unchanged.
        """
        self.preconditions = preconditions
        self.effects = effects


class STRIPS_domain(object):
    def __init__(self, feats_vals, strips_map):
        """Problem domain
        feats_vals is a feature:domain dictionary,
                mapping each feature to its domain
        strips_map is an action:strips dictionary,
                mapping each action to its Strips representation
        """
        self.actions = set(strips_map)  # set of all actions
        self.feats_vals = feats_vals
        self.strips_map = strips_map


boolean = {True, False}
delivery_domain = STRIPS_domain(
    {'RLoc': {'cs', 'off', 'lab', 'mr'}, 'RHC': boolean, 'SWC': boolean,
     'MW': boolean, 'RHM': boolean},  # feaures:values dictionary
    {'mc_cs': Strips({'RLoc': 'cs'}, {'RLoc': 'off'}),
     'mc_off': Strips({'RLoc': 'off'}, {'RLoc': 'lab'}),
     'mc_lab': Strips({'RLoc': 'lab'}, {'RLoc': 'mr'}),
     'mc_mr': Strips({'RLoc': 'mr'}, {'RLoc': 'cs'}),
     'mcc_cs': Strips({'RLoc': 'cs'}, {'RLoc': 'mr'}),
     'mcc_off': Strips({'RLoc': 'off'}, {'RLoc': 'cs'}),
     'mcc_lab': Strips({'RLoc': 'lab'}, {'RLoc': 'off'}),
     'mcc_mr': Strips({'RLoc': 'mr'}, {'RLoc': 'lab'}),
     'puc': Strips({'RLoc': 'cs', 'RHC': False}, {'RHC': True}),
     'dc': Strips({'RLoc': 'off', 'RHC': True}, {'RHC': False, 'SWC': False}),
     'pum': Strips({'RLoc': 'mr', 'MW': True}, {'RHM': True, 'MW': False}),
     'dm': Strips({'RLoc': 'off', 'RHM': True}, {'RHM': False})
     })


class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal, positions={}):
        """
        a planning problem consists of
        * a planning domain
        * the initial state
        * a goal
        * positions
        """
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal
        self.positions = positions


strips_delivery1 = Planning_problem(delivery_domain,
                                    {'RLoc': 'lab', 'MW': True, 'SWC': True, 'RHC': False,
                                     'RHM': False},
                                    {'RLoc': 'off'},positions={
                                        'RLoc':(100,100),
                                        'RHC':(100,200),
                                        'SWC':(100,300),
                                        'MW':(100,400),
                                        'RHM':(100,500),
                                        'action':(200,300)
                                    })
strips_delivery2 = Planning_problem(delivery_domain,
                                    {'RLoc': 'lab', 'MW': True, 'SWC': True, 'RHC': False,
                                     'RHM': False},
                                    {'SWC': False},positions={
                                        'RLoc':(100,100),
                                        'RHC':(100,200),
                                        'SWC':(100,300),
                                        'MW':(100,400),
                                        'RHM':(100,500),
                                        'action':(200,300)
                                    })
strips_delivery3 = Planning_problem(delivery_domain,
                                    {'RLoc': 'lab', 'MW': True, 'SWC': True, 'RHC': False,
                                     'RHM': False},
                                    {'SWC': False, 'MW': False, 'RHM': False},positions={
                                        'RLoc':(100,100),
                                        'RHC':(100,200),
                                        'SWC':(100,300),
                                        'MW':(100,400),
                                        'RHM':(100,500),
                                        'action':(200,300)
                                    })

# blocks world


def move(x, y, z):
    """string for the move action"""
    return 'move_' + x + '_from_' + y + '_to_' + z


def on(x, y):
    """string for the 'on' feature"""
    return x + '_on_' + y


def clear(x):
    """string for the 'clear' feature"""
    return 'clear_' + x


def create_blocks_world(blocks=['a', 'b', 'c', 'd']):
    blocks_and_table = blocks + ['table']
    stmap = {move(x, y, z): Strips({on(x, y): True, clear(x): True, clear(z): True},
                                   {on(x, z): True, on(x, y): False, clear(y): True, clear(z): False})
             for x in blocks
             for y in blocks_and_table
             for z in blocks
             if x != y and y != z and z != x}
    stmap.update({move(x, y, 'table'): Strips({on(x, y): True, clear(x): True},
                                              {on(x, 'table'): True, on(x, y): False, clear(y): True})
                  for x in blocks
                  for y in blocks
                  if x != y})
    feats_vals = {on(x, y): boolean for x in blocks for y in blocks_and_table}
    feats_vals.update({clear(x): boolean for x in blocks_and_table})
    return STRIPS_domain(feats_vals, stmap)
#Generate Positions From Variables
def create_position(variables):
    positions={}
    i = 0;
    for var in variables.feats_vals:
        positions[var] = (100,i*100);
        i+=1;
    positions['action'] = (200,i*50);
    return positions

blocks1dom = create_blocks_world(['a', 'b', 'c'])
strips_blocks1 = Planning_problem(blocks1dom,
                                  {on('a', 'table'): True, clear('a'): True, clear('b'): True, on('b', 'c'): True,
                                   on('c', 'table'): True, clear('c'): False},  # initial state
                                  {on('a', 'b'): True, on('c', 'a'): True},positions=create_position(blocks1dom))  # goal

blocks2dom = create_blocks_world(['a', 'b', 'c', 'd'])
tower4 = {clear('a'): True, on('a', 'b'): True, clear('b'): False,
          on('b', 'c'): True, clear('c'): False, on('c', 'd'): True,
          clear('b'): False, on('d', 'table'): True}
strips_blocks2 = Planning_problem(blocks2dom,
                                  tower4,  # initial state
                                  {on('d', 'c'): True, on('c', 'b'): True, on('b', 'a'): True},positions=create_position(blocks2dom))  # goal

strips_blocks3 = Planning_problem(blocks2dom,
                                  tower4,  # initial state
                                  {on('d', 'a'): True, on('a', 'b'): True, on('b', 'c'): True},  # goal
                                 positions=create_position(blocks2dom))  

elevator_domain = STRIPS_domain({'Elevator': {'B', 1, 2, 3, 4}, 'Passenger': {'B', 1, 2, 3, 4, 'E'}},
                                {'Goto1': Strips({}, {'Elevator': 1}),
                                 'Goto2': Strips({}, {'Elevator': 2}),
                                 'Goto3': Strips({}, {'Elevator': 3}),
                                 'Goto4': Strips({}, {'Elevator': 4}),
                                 'PickUp': Strips({'Elevator': 1, 'Passenger': 1}, {'Passenger': 'E'}),
                                 'DeopOff': Strips({'Elevator': 4, 'Passenger': 'E'}, {'Passenger': 4})})

strips_elevator = Planning_problem(elevator_domain,
                                   {'Elevator': 'B', 'Passenger': 1},
                                   {'Passenger': 4},
                                   positions={
                                       'Elevator': (100, 200),
                                       'Passenger': (100, 500),
                                       'action': (200, 300)
                                   })

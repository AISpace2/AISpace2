import threading
from functools import partial

from aipython.cspProblem import CSP
from ipywidgets import register
from traitlets import Bool, Dict, Float, Instance, Unicode

from ..stepdomwidget import ReturnableThread, StepDOMWidget
from .cspjsonbridge import (csp_from_json, csp_to_json,
                            generate_csp_graph_mappings)

from ... import __version__

@register
class Displayable(StepDOMWidget):
    """A Jupyter widget for visualizing constraint satisfaction problems (CSPs).

    Handles arc consistency, domain splitting, and stochastic local search (SLS).

    See the accompanying frontend file: `js/src/csp/CSPVisualizer.ts`
    """
    _view_name = Unicode('CSPViewer').tag(sync=True)
    _model_name = Unicode('CSPViewerModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    # The CSP that is synced as a graph to the frontend.
    graph = Instance(
        klass=CSP, allow_none=True).tag(
            sync=True, to_json=csp_to_json, from_json=csp_from_json)

    # Tracks if the visualization has been rendered at least once in the front-end. See the @visualize decorator.
    _previously_rendered = Bool(False).tag(sync=True)

    def __init__(self):
        super().__init__()
        self.visualizer = self

        ##############################
        ### SLS-specific variables ###
        ##############################
        # Tracks if this is the first conflict reported.
        # If so, will also compute non-conflicts to highlight green the first time around.
        self._sls_first_conflict = True

        ##########################################
        ### Arc consistency-specific variables ###
        ##########################################
        # A reference to the arc the user has selected for arc consistency. A tuple of (variable name, Constraint instance).
        self._selected_arc = None
        # True if the user has selected an arc to perform arc-consistency on. Otherwise, an arc is automatically chosen.
        self._has_user_selected_arc = False
        # True if the algorithm is at a point where an arc is waiting to be chosen. Used to filter out extraneous clicks otherwise.
        self._is_waiting_for_arc_selection = False

        ###########################################
        ### Domain splitting-specific variables ###
        ##########################################
        # A reference to the variable the user has selected for domain splitting.
        self._selected_var = None
        # True if the user has selected a var to perform domain splitting on. Otherwise, a variable is automatically chosen.
        self._has_user_selected_var = False
        # True if the algorithm is at a point where a var is waiting to be chosen. Used to filter out extraneous clicks otherwise.
        self._is_waiting_for_var_selection = False
        # The domain the user has chosen as their first split for `_selected_var`.
        self._domain_split = None

        self.graph = self.csp
        (self._domain_map,
         self._edge_map) = generate_csp_graph_mappings(self.csp)

        self._initialize_controls()

    def wait_for_arc_selection(self, to_do):
        """Pauses execution until an arc has been selected and returned.

        If the algorithm is running in auto mode, an arc is returned immediately.
        Otherwise, this function blocks until an arc is selected by the user.

        Args:
            to_do (set): A set of arcs to choose from. This set will be modified.

        Returns:
            (string, Constraint):
                A tuple (var_name, constraint) that represents an arc from `to_do`.
        """
        # Running in Auto mode. Don't block!
        if self.max_display_level == 1:
            return to_do.pop()

        self._is_waiting_for_arc_selection = True
        self._block_for_user_input.wait()

        if self._has_user_selected_arc:
            self._has_user_selected_arc = False
            to_do.discard(self._selected_arc)
            return self._selected_arc

        # User did not select. Return random arc.
        return to_do.pop()

    def wait_for_var_selection(self, iter_var):
        """Pauses execution until a variable has been selected and returned.

        If the user steps instead of clicking on a variable, a random variable is returned.
        Otherwise, the variable clicked by the user is returned, but only if it is a variable
        that can be split on. Otherwise, this function continues waiting.

        Args:
            iter_var (iter): Variables that the user is allowed to split on.

        Returns:
            (string): The variable to split on.
        """
        self._is_waiting_for_var_selection = True
        self._block_for_user_input.wait()
        self.max_display_level = 4
        iter_var = list(iter_var)

        if self._has_user_selected_var:
            self._has_user_selected_var = False
            if self._selected_var in iter_var:
                return self._selected_var
            else:
                return self.wait_for_var_selection(iter_var)

        return iter_var[0]

    def choose_domain_partition(self, domain):
        """Pauses execution until a domain has been split on.

        If the user chooses to not select a domain (clicks 'Cancel'), splits the domain in half.
        Otherwise, the subset of the domain chosen by the user is used as the initial split.

        Args:
            domain (set): Domain of the variable being split on.

        Returns:
            (set): A subset of the domain to be split on first.
        """
        self.send({'action': 'chooseDomainSplit', 'domain': domain})
        self._block_for_user_input.wait()

        if self._domain_split is None:
            # Split in half
            split = len(domain) // 2
            dom1 = set(list(domain)[:split])
            dom2 = domain - dom1
            return dom1, dom2

        split1 = set(self._domain_split)
        split2 = set(domain) - split1
        return split1, split2

    def handle_custom_msgs(self, _, content, buffers=None):
        super().handle_custom_msgs(None, content, buffers)
        event = content.get('event', '')

        if event == 'arc:click':
            """
            Expects a dictionary containing:
                varName (string): The name of the variable connected to this arc.
                constId (string): The id of the constraint connected to this arc.
            """
            if self._is_waiting_for_arc_selection:
                var_name = content.get('varName')
                const = self.csp.constraints[content.get('constId')]
                self.max_display_level = 2

                self._selected_arc = (var_name, const)
                self._has_user_selected_arc = True
                self._block_for_user_input.set()
                self._block_for_user_input.clear()
                self._is_waiting_for_arc_selection = False

        elif event == 'var:click':
            """
            Expects a dictionary containing:
                varName (string): The name of the variable to split on.
            """
            if self._is_waiting_for_var_selection:
                var_name = content.get('varName')
                self._selected_var = var_name
                self._has_user_selected_var = True
                self._block_for_user_input.set()
                self._block_for_user_input.clear()
                self._is_waiting_for_var_selection = False

        elif event == 'domain_split':
            """
            Expects a dictionary containing:
                domain (string[]|None):
                    An array of the elements in the domain to first split on, or None if no choice is made.
                    In this case, splits the domain in half as a default.
            """
            domain = content.get('domain')
            self._domain_split = domain
            self._block_for_user_input.set()
            self._block_for_user_input.clear()

        elif event == 'initial_render':
            queued_func = getattr(self, '_queued_func', None)

            # Run queued function after we know the frontend view exists
            if queued_func:
                func = queued_func['func']
                args = queued_func['args']
                kwargs = queued_func['kwargs']
                self._previously_rendered = True
                self._thread = ReturnableThread(
                    target=func, args=args, kwargs=kwargs)
                self._thread.start()

    def display(self, level, *args, **kwargs):
        should_wait = True

        if args[0] == 'Performing AC with domains':
            should_wait = False
            domains = args[1]
            vars_to_change = []
            domains_to_change = []

            for var, domain in domains.items():
                vars_to_change.append(var)
                domains_to_change.append(domain)

            self._send_set_domains_action(vars_to_change, domains_to_change)

        elif args[0] == 'Domain pruned':
            variable = args[2]
            domain = args[4]
            constraint = args[6]
            self._send_set_domains_action(variable, [domain])

        elif args[0] == "Processing arc (":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_arcs_action(
                (variable, constraint), style='bold', colour=None)

        elif args[0] == 'Domain pruned':
            variable = args[2]
            constraint = args[6]
            self._send_highlight_arcs_action(
                (variable, constraint), style='bold', colour='green')

        elif args[0] == "Arc: (" and args[4] == ") is inconsistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_arcs_action(
                (variable, constraint), style='bold', colour='red')

        elif args[0] == "Arc: (" and args[4] == ") now consistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_arcs_action(
                (variable, constraint), style='normal', colour='green')
            should_wait = False

        elif args[0] == "  adding" and args[2] == "to to_do.":
            if args[1] != "nothing":
                arcs = list(args[1])
                arcs_to_highlight = []

                for arc in arcs:
                    arcs_to_highlight.append((arc[0], arc[1]))

                self._send_highlight_arcs_action(
                    arcs_to_highlight, style='normal', colour='blue')

        #############################
        ### SLS-specific displays ###
        #############################

        elif args[0] == "Initial assignment":
            assignment = args[1]
            for (key, val) in assignment.items():
                self._send_set_domains_action(key, [val])

        elif args[0] == "Assigning" and args[2] == "=":
            var = args[1]
            domain = args[3]
            self._send_set_domains_action(var, [domain])
            self._send_highlight_nodes_action(var, "blue")

        elif args[0] == "Checking":
            node = args[1]
            self._send_highlight_nodes_action(node, "blue")

        elif args[0] == "Still inconsistent":
            const = args[1]
            nodes_to_highlight = {const}
            arcs_to_highlight = []

            for var in const.scope:
                nodes_to_highlight.add(var)
                arcs_to_highlight.append((var, const))

            self._send_highlight_nodes_action(nodes_to_highlight, "red")
            self._send_highlight_arcs_action(arcs_to_highlight, "bold", "red")

        elif args[0] == "Still consistent":
            const = args[1]
            nodes_to_highlight = {const}
            arcs_to_highlight = []

            for var in const.scope:
                nodes_to_highlight.add(var)
                arcs_to_highlight.append((var, const))

            self._send_highlight_nodes_action(nodes_to_highlight, "green")
            self._send_highlight_arcs_action(arcs_to_highlight, "bold",
                                             "green")

        elif args[0] == "Became consistent":
            const = args[1]
            nodes_to_highlight = {const}
            arcs_to_highlight = []

            for var in const.scope:
                nodes_to_highlight.add(var)
                arcs_to_highlight.append((var, const))

            self._send_highlight_nodes_action(nodes_to_highlight, "green")
            self._send_highlight_arcs_action(arcs_to_highlight, "bold",
                                             "green")

        elif args[0] == "Became inconsistent":
            const = args[1]
            nodes_to_highlight = {const}
            arcs_to_highlight = []

            for var in const.scope:
                nodes_to_highlight.add(var)
                arcs_to_highlight.append((var, const))

            self._send_highlight_nodes_action(nodes_to_highlight, "red")
            self._send_highlight_arcs_action(arcs_to_highlight, "bold", "red")

        elif args[0] == "Conflicts:":
            conflicts = args[1]
            conflict_nodes_to_highlight = set()
            conflict_arcs_to_highlight = []
            non_conflict_nodes_to_highlight = set()
            non_conflict_arcs_to_highlight = []

            if self._sls_first_conflict:
                # Highlight all non-conflicts green
                self._sls_first_conflict = False
                not_conflicts = set(self.csp.constraints) - conflicts

                for not_conflict in not_conflicts:
                    non_conflict_nodes_to_highlight.add(not_conflict)

                    for node in not_conflict.scope:
                        non_conflict_nodes_to_highlight.add(node)
                        non_conflict_arcs_to_highlight.append((node,
                                                               not_conflict))

                self._send_highlight_nodes_action(
                    non_conflict_nodes_to_highlight, "green")
                self._send_highlight_arcs_action(
                    non_conflict_arcs_to_highlight, "bold", "green")

            # Highlight all conflicts red
            for conflict in conflicts:
                conflict_nodes_to_highlight.add(conflict)

                for node in conflict.scope:
                    conflict_nodes_to_highlight.add(node)
                    conflict_arcs_to_highlight.append((node, conflict))

            self._send_highlight_nodes_action(conflict_nodes_to_highlight,
                                              "red")
            self._send_highlight_arcs_action(conflict_arcs_to_highlight,
                                             "bold", "red")

        super().display(level, *args, **dict(kwargs, should_wait=should_wait))

    def _send_highlight_nodes_action(self, vars, colour):
        """Sends a message to the front-end visualization to highlight nodes.

        Args:
            vars (string|string[]): The name(s) of the variables to highlight.
            colour (string|None): A HTML colour string for the stroke of the node.
                Passing in None will keep the existing stroke of the node.
        """

        # We don't want to check if it is iterable because a string is iterable
        if not isinstance(vars, list) and not isinstance(vars, set):
            vars = [vars]

        nodeIds = []
        for var in vars:
            nodeIds.append(self._domain_map[var])

        self.send({
            'action': 'highlightNodes',
            'nodeIds': nodeIds,
            'colour': colour
        })

    def _send_highlight_arcs_action(self, arcs, style='normal', colour=None):
        """Sends a message to the front-end visualization to highlight arcs.

        Args:
            arcs ((string, Constraint)|(string, Constraint)[]): 
                Tuples of (variable name, Constraint instance) that form an arc. 
                For convenience, you do not need to pass a list of tuples of you only have one to highlight.
            style ('normal'|'bold'): Style of the highlight. Applied to every arc passed in.
            colour (string|None): A HTML colour string for the colour of the line.
                Passing in None will keep the existing colour of the arcs.
        """

        if not isinstance(arcs, list):
            arcs = [arcs]

        arc_ids = []
        for arc in arcs:
            arc_ids.append(self._edge_map[arc])

        self.send({
            'action': 'highlightArcs',
            'arcIds': arc_ids,
            'style': style,
            'colour': colour
        })

    def _send_set_domains_action(self, vars, domains):
        """Sends a message to the front-end visualization to set the domains of variables.

        Args:
            vars (string|string[]): The name of the variable(s) whose domain should be changed.
            domains (List[int|string]|List[List[int|string]]): The updated domain of the variable(s).
              If vars is an array, then domain is an array of domains, in the same order.
        """

        is_single_var = False
        if not isinstance(vars, list):
            vars = [vars]
            is_single_var = True

        self.send({
            'action':
            'setDomains',
            'nodeIds': [self._domain_map[var] for var in vars],
            'domains': [list(domain) for domain in domains]
            if not is_single_var else [domains]
        })


def visualize(func_to_delay):
    """Enqueues a function that does not run until the Jupyter widget has rendered.

    Once the Jupyter widget has rendered once, further invocation of the wrapped function
    behave as if unwrapped. Necessary because otherwise, the function runs (and blocks when display is called)
    immediately, before the view has a chance to render
    (and so there is no way to unblock using the step buttons!)

    Args:
        func_to_delay (function): The function to delay.

    Returns: 
        The original function, wrapped such that it will automatically run
        when the Jupyter widget is rendered.
    """

    def wrapper(self, *args, **kwargs):
        if self._previously_rendered is False:
            self._queued_func = {
                'func': partial(func_to_delay, self),
                'args': args,
                'kwargs': kwargs
            }
        else:
            return func_to_delay(self, *args, **kwargs)

    return wrapper

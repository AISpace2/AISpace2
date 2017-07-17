import threading
from time import sleep

from ipywidgets import DOMWidget


class StepDOMWidget(DOMWidget):
    """Base Jupyter widget for visualizations that you can step through.
    
    Attributes:
        sleep_time (int): The minimum time delay between consecutive display calls.
    """

    def __init__(self):
        super().__init__()
        self.on_msg(self.handle_custom_msgs)

        self.sleep_time = 0.2

        # Blocks the visualization when waited on for user input.
        # You MUST wait() on this event only on a background thread!
        self._block_for_user_input = threading.Event()

        # The display level to block on. The visualization will not block on displays > to this.
        self._display_block_level = 4
        self._initialize_controls()

    def _initialize_controls(self):
        """Sets up functions that can be used to control the visualization."""
        def step_through_to_level(desired_level):
            def step():
                self.before_step()
                self._display_block_level = desired_level
                self._block_for_user_input.set()
                self._block_for_user_input.clear()

                # if not self._thread.is_alive():
                #     return_value = self._thread.join()
                #     if not isinstance(return_value, list):
                #         return_value = [return_value]

                # self.send({'action': 'output',
                #         'text': 'Algorithm execution finished. Returned: {}'.format(
                #             ', '.join(str(x) for x in return_value)
                #         )})
            return step

        self._fine_step = step_through_to_level(4)
        self._step = step_through_to_level(2)
        self._auto_step = step_through_to_level(1)

    def before_step(self):
        """Override this to provide custom logic before every (fine/auto) step.
        
        For example, you may reset state variables."""
        pass

    def handle_custom_msgs(self, _, content, buffers=None):
        """Handle messages sent from the front-end."""
        event = content.get('event', '')

        if event == 'fine-step:click':
            self._fine_step()
        elif event == 'step:click':
            self._step()
        elif event == 'auto-step:click':
            self._auto_step()

    def display(self, level, *args, **kwargs):
        """Informs the widget about a new state to update the visualization in response to.

        Args:
            level (int): An integer in [1, 4] that specifies how "important" the message is.
                It may also be interpreted as a level of "specificity".
                1 means very general, such as the algorithm has finished.
                4 means very specific, such as some very minor algorithmic detail.
            *args: Any extra data to help the visualization update.
        """
        text = ' '.join(map(str, args))
        self.send({'action': 'output', 'text': text})

        if level <= self._display_block_level:
            if 'should_wait' in kwargs:
                if not kwargs['should_wait']:
                    return

            self._block_for_user_input.wait()
        else:
            sleep(self.sleep_time)

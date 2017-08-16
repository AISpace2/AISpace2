import threading
from time import sleep

from ipywidgets import DOMWidget
from traitlets import validate


class ReturnableThread(threading.Thread):
    """A thread extended to allow a return value.
    To get the return value, use this thread as normal, but assign it to a variable on creation.
    calling var.join() will return the return value.
    the return value can also be gotten directly via ._return, but this is not safe.
    """

    def __init__(self, *args, **kwargs):
        super(ReturnableThread, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        super().join(timeout)
        return self._return


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
        self.max_display_level = 4
        self._initialize_controls()

    @validate('sleep_time')
    def _validate_sleep_time(self, proposal):
        """Cap sleep_time at a minimum value.

        Too low values freeze the UI, as the messages have no time to be processed.
        """
        sleep_time = proposal['value']
        if sleep_time < 0.05:
            sleep_time = 0.05

        return sleep_time

    def _initialize_controls(self):
        """Sets up functions that can be used to control the visualization."""

        def step_through_to_level(desired_level):
            def step():
                if not hasattr(self, '_thread') or not self._thread:
                    self.send({
                        'action': 'output',
                        'text': 'Run a function to begin stepping.'
                    })

                    return

                self.before_step()
                self.max_display_level = desired_level
                self._block_for_user_input.set()
                self._block_for_user_input.clear()

                # HACK: Allows the thread to die, if it returns.
                # Otherwise, it will only be dead on the next step, not this one.
                sleep(0.1)

                if not self._thread.is_alive():
                    return_value = self._thread.join()

                    if return_value is not None:
                        self.send({
                            'action':
                            'output',
                            'text':
                            'Function returned: {}'.format(str(return_value))
                        })

            return step

        self._fine_step = step_through_to_level(4)
        self._step = step_through_to_level(2)
        self._auto_solve = step_through_to_level(1)

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
        elif event == 'auto-solve:click':
            self._auto_solve()

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

        if level <= self.max_display_level:
            if 'should_wait' in kwargs:
                if not kwargs['should_wait']:
                    return

            self._block_for_user_input.wait()
        else:
            sleep(self.sleep_time)

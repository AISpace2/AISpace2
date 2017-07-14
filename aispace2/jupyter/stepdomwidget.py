import threading
from time import sleep

from ipywidgets import DOMWidget


class StepDOMWidget(DOMWidget):
    """Base class for visualizations that you can step through."""

    def __init__(self):
        super().__init__()
        self.on_msg(self._handle_custom_msgs)
        self._block_for_user_input = threading.Event()
        self._desired_level = 4
        self._controls = {}
        self._initialize_controls()
        self.sleep_time = 0.2

    def _initialize_controls(self):
        """Sets up functions that can be used to control the visualization."""
        def advance_visualization(desired_level):
            def advance():
                self._desired_level = desired_level
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
            return advance

        self._controls = {
            'fine-step': advance_visualization(4),
            'step': advance_visualization(2),
            'auto-step': advance_visualization(1)
        }

    def _handle_custom_msgs(self, _, content, buffers=None):
        event = content.get('event', '')

        if event == 'fine-step:click':
            self._controls['fine-step']()
        elif event == 'step:click':
            self._controls['step']()
        elif event == 'auto-step:click':
            self._controls['auto-step']()

    def display(self, level, *args, **kwargs):
        text = ' '.join(map(str, args))
        self.send({'action': 'output', 'text': text})

        if level <= self._desired_level:
            if 'should_wait' in kwargs:
                if not kwargs['should_wait']:
                    return

            self._block_for_user_input.wait()
        else:
            sleep(self.sleep_time)

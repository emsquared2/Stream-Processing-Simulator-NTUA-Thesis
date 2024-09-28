import os
import sys

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import MagicMock
from topology.node.state.State import State
from topology.node.state.Window import Window


class MockComplexity:
    """
    Mock class for Complexity to simulate cycle calculation based on occurrences.
    """

    def calculate_cycles(self, occurrences: int) -> int:
        # Simulate a complexity calculation based on occurrences O(n^2)
        return occurrences * occurrences


# Manually define keys: 5 key1, 4 key2, 6 key3, and 5 key4
def load_keys():
    return [
        "key1",
        "key4",
        "key1",
        "key3",
        "key2",
        "key2",
        "key3",
        "key4",
        "key2",
        "key3",
        "key1",
        "key2",
        "key1",
        "key3",
        "key3",
        "key4",
        "key1",
        "key4",
        "key4",
        "key3",
    ]


class TestState(unittest.TestCase):

    def setUp(self):
        """
        Set up the State instance with multiple windows for testing process_window.
        """
        # Initialize the state with test parameters
        self.state = State(
            node_id=1, throughput=100, complexity_type="O(n^2)", window_size=10, slide=5
        )

        # Mock the complexity object
        self.state.complexity = MockComplexity()

        # Manually create windows for testing
        self.window1 = Window(start_step=0, window_size=10, slide=5)
        self.window2 = Window(start_step=5, window_size=10, slide=5)
        self.window3 = Window(start_step=10, window_size=10, slide=5)

        # Load keys into window1 (to be processed)
        self.window1.keys = load_keys()
        self.window2.keys = ["key3", "key4"]
        self.window3.keys = ["key7", "key8"]

        # Add the windows to the state
        self.state.windows[0] = self.window1
        self.state.windows[5] = self.window2
        self.state.windows[10] = self.window3

    def test_process_window_with_overdue_keys(self):
        """
        Test processing a window where not all keys can be processed.
        """
        # Set throughput limit to only process part of the window1 keys
        self.state.throughput = 73  # This should only allow some keys to be processed

        # Mock the log_node_info to avoid actual logging during the test
        self.state.node_logger = MagicMock()

        # Process the first window
        _, result_keys = self.state.process_window(
            self.window1, terminal=False, step_cycles=0
        )

        # Assertions:

        # 1. Check the result returned
        # We expect the first 16 keys to be processed so the result will be all the distinct keys in the first 16 keys and in the order they appeared : key1, key4, key3, key2
        self.assertEqual(result_keys, ["key1", "key4", "key3", "key2"])

        # 2. Ensure overdue keys remain in window
        expected_window1_keys = [
            "key1",
            "key4",
            "key4",
            "key3",
        ]
        self.assertEqual(self.state.windows[0].keys, expected_window1_keys)

        # 3. Ensure windows 2 & 3 remain unchanged
        self.assertEqual(self.window2.keys, ["key3", "key4"])
        self.assertEqual(self.window3.keys, ["key7", "key8"])

    def test_process_window_complete(self):
        """
        Test processing a window where all keys can be processed without leftover keys.
        """
        # Set throughput high enough to process all keys
        self.state.throughput = 150

        # Process the first window
        _, result_keys = self.state.process_window(
            self.window1, terminal=False, step_cycles=0
        )

        # Assertions:
        # 1. All keys should be processed
        self.assertEqual(result_keys, ["key1", "key4", "key3", "key2"])

        # 2. The first window should now be empty
        self.assertEqual(self.window1.keys, [])

        # 3. The next windows should remain unchanged
        self.assertEqual(self.window2.keys, ["key3", "key4"])
        self.assertEqual(self.window3.keys, ["key7", "key8"])

    def test_process_window_with_terminal(self):
        """
        Test processing a window in a terminal node where no keys should be passed forward.
        """
        # Set throughput to process all keys
        self.state.throughput = 150

        # Process the first window in a terminal node (terminal=True)
        _, result_keys = self.state.process_window(
            self.window1, terminal=True, step_cycles=0
        )

        # Assertions:
        # 1. No keys should be passed to the next stage (since terminal is True)
        self.assertEqual(result_keys, [])

        # 2. All keys in the window should be processed
        self.assertEqual(self.window1.keys, [])

    def test_update_method(self):
        """
        Test the update method by simulating the process over multiple steps.
        """
        # Initialize the state with test parameters
        state = State(
            node_id=1, throughput=50, complexity_type="O(n^2)", window_size=5, slide=2
        )

        # Mock the complexity object
        state.complexity = MockComplexity()

        # Mock the log_node_info to avoid actual logging during the test
        state.node_logger = MagicMock()
        state.default_logger = MagicMock()

        # Simulate steps with incoming keys
        steps_keys = {
            0: ["key1", "key5", "key2", "key4", "key3"],
            1: ["key3", "key5", "key1", "key4", "key2"],
            2: ["key4", "key1", "key3", "key2", "key5"],
            3: ["key5", "key4", "key2", "key3", "key1"],
            4: ["key4", "key3", "key5", "key1", "key2"],
            5: ["key1", "key3", "key2", "key4", "key5"],
            6: ["key5", "key4", "key1", "key3", "key2"],
            7: [
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
                "key5",
                "key2",
                "key1",
                "key3",
                "key4",
            ],
            8: ["key4", "key1", "key3", "key2", "key5"],
            9: ["key5", "key4", "key2", "key3", "key1"],
            10: ["key4", "key3", "key5", "key1", "key2"],
            11: [],
            12: [],
        }

        processed_keys_over_time = []
        for step in steps_keys:
            keys = steps_keys.get(step, [])
            terminal = False
            processed_keys = state.update(keys, step, terminal)
            processed_keys_over_time.append((step, processed_keys))

            # At step 5, window starting at 0 should be processed
            if step == 5:

                expected_remaining_window_0 = [
                    "key5",
                    "key4",
                    "key2",
                    "key3",
                    "key1",
                    "key4",
                    "key3",
                    "key5",
                    "key1",
                    "key2",
                ]

                self.assertEqual(state.windows[0].keys, expected_remaining_window_0)
                self.assertEqual(state.total_cycles, 45)
                self.assertEqual(state.total_processed, 15)
                expected_window_2 = (
                    steps_keys.get(2, [])
                    + steps_keys.get(3, [])
                    + steps_keys.get(4, [])
                    + steps_keys.get(5, [])
                )
                expected_window_4 = steps_keys.get(4, []) + steps_keys.get(5, [])
                self.assertEqual(state.windows[2].keys, expected_window_2)
                self.assertEqual(state.windows[4].keys, expected_window_4)

            if step == 6:
                self.assertNotIn(0, state.windows)
                self.assertEqual(state.total_cycles, 65)
                self.assertEqual(state.total_processed, 25)

                expected_window_2 = (
                    steps_keys.get(2, [])
                    + steps_keys.get(3, [])
                    + steps_keys.get(4, [])
                    + steps_keys.get(5, [])
                    + steps_keys.get(6, [])
                )
                expected_window_4 = (
                    steps_keys.get(4, [])
                    + steps_keys.get(5, [])
                    + steps_keys.get(6, [])
                )
                expected_window_6 = steps_keys.get(6, [])

                self.assertEqual(state.windows[2].keys, expected_window_2)
                self.assertEqual(state.windows[4].keys, expected_window_4)
                self.assertEqual(state.windows[6].keys, expected_window_6)

            if step == 8:
                self.assertEqual(len(state.windows[4].keys), 50)
                self.assertEqual(len(state.windows[6].keys), 40)
                self.assertEqual(len(state.windows[8].keys), 5)
            if step == 9:
                self.assertEqual(len(state.windows[4].keys), 35)
                self.assertEqual(len(state.windows[6].keys), 45)
                self.assertEqual(len(state.windows[8].keys), 10)
            if step == 10:
                self.assertEqual(len(state.windows[4].keys), 20)
                self.assertEqual(len(state.windows[6].keys), 50)
                self.assertEqual(len(state.windows[8].keys), 15)
                self.assertEqual(len(state.windows[10].keys), 5)
            if step == 11:
                self.assertEqual(len(state.windows[4].keys), 5)
                self.assertEqual(len(state.windows[6].keys), 45)
                self.assertEqual(len(state.windows[8].keys), 15)
                self.assertEqual(len(state.windows[10].keys), 5)
            if step == 12:
                self.assertNotIn(4, state.windows)
                self.assertEqual(len(state.windows[6].keys), 30)
                self.assertEqual(len(state.windows[8].keys), 15)
                self.assertEqual(len(state.windows[10].keys), 5)

        # Check Final Metrics
        self.assertEqual(state.total_keys, 80)
        self.assertEqual(state.total_processed, 120)
        self.assertEqual(state.total_expired, 0)
        self.assertEqual(state.total_cycles, 320)


if __name__ == "__main__":
    unittest.main()

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
        self.window1 = Window(start_step=0, window_size=10)
        self.window2 = Window(start_step=5, window_size=10)
        self.window3 = Window(start_step=10, window_size=10)

        # Load keys into window1 (to be processed) and window2 (where overdue keys will go)
        self.window1.keys = load_keys()
        self.window2.keys = [
            "key3",
            "key4",
            "key4",
            "key3",
            "key5",
        ]  # Pre-existing keys in window2
        self.window3.keys = ["key7", "key8"]

        # Add the windows to the state
        self.state.windows[0] = self.window1
        self.state.windows[5] = self.window2
        self.state.windows[10] = self.window3

    def test_process_window_with_overdue_keys(self):
        """
        Test processing a window where not all keys can be processed, and the remaining keys
        are passed to the next window.
        """
        # Set throughput limit to only process part of the window1 keys
        self.state.throughput = 73  # This should only allow some keys to be processed

        # Mock the log_node_info to avoid actual logging during the test
        self.state.node_logger = MagicMock()

        # Process the first window
        result_keys = self.state.process_window(self.window1, terminal=False)

        # Assertions:

        # 1. Check the result returned
        # We expect the first 9 keys to be processed so the result will all the distinct keys in the first 9 keys: key1, key2, key3, key4
        self.assertEqual(result_keys, ["key1", "key2", "key3", "key4"])

        # 2. Ensure overdue keys were added to window2
        expected_window2_keys = [
            "key3",
            "key4",
            "key4",
            "key3",
            "key5",
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
        ]  # Pre-existing + overdue
        self.assertEqual(self.state.windows[5].keys, expected_window2_keys)

        # 3. Ensure window 3 remains unchanged
        self.assertEqual(self.window3.keys, ["key7", "key8"])

    def test_process_window_complete(self):
        """
        Test processing a window where all keys can be processed without leftover keys.
        """
        # Set throughput high enough to process all keys
        self.state.throughput = 150

        # Process the first window
        result_keys = self.state.process_window(self.window1, terminal=False)

        # Assertions:
        # 1. All keys should be processed
        self.assertEqual(result_keys, ["key1", "key2", "key3", "key4"])

        # 2. The first window should now be empty
        self.assertEqual(self.window1.keys, [])

        # 3. The next window (window2) should remain unchanged
        self.assertEqual(
            self.state.windows[5].keys,
            [
                "key3",
                "key4",
                "key4",
                "key3",
                "key5",
            ],
        )

    def test_process_window_with_terminal(self):
        """
        Test processing a window in a terminal node where no keys should be passed forward.
        """
        # Set throughput to process all keys
        self.state.throughput = 150

        # Process the first window in a terminal node (terminal=True)
        result_keys = self.state.process_window(self.window1, terminal=True)

        # Assertions:
        # 1. No keys should be passed to the next stage (since terminal is True)
        self.assertEqual(result_keys, [])

        # 2. All keys in the window should be processed
        self.assertEqual(self.window1.keys, [])


if __name__ == "__main__":
    unittest.main()
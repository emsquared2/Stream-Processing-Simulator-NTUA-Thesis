import unittest
from unittest.mock import MagicMock, patch
from topology.node.WorkerNode import StatefulNode


class TestStatefulNode(unittest.TestCase):
    def setUp(self):
        """Initializes a non terminal & a terminal node"""
        self.node_non_terminal = StatefulNode(
            node_id=1,
            throughput=10,
            operation_type="StatelessOperation",
            window_size=5,
            slide=1,
            terminal=False,
        )

        self.node_terminal = StatefulNode(
            node_id=1,
            throughput=10,
            operation_type="StatelessOperation",
            window_size=5,
            slide=1,
            terminal=True,
        )

    @patch("builtins.print")
    def test_emit_keys_called_when_non_terminal_node(self, mock_print):
        """Tests the emitted keys from a window process in a non-terminal node

        Args:
            mock_print (): Function tha simulates and catches the actual print calls
        """
        # Mock emit_keys to check its output / calls
        self.node_non_terminal.emit_keys = MagicMock(
            side_effect=self.node_non_terminal.emit_keys
        )

        # Simulate receiving and processing keys for each step
        for step in range(0, 8):
            keys = [f"key{step}"]
            self.node_non_terminal.receive_and_process(keys, step)

        # Check the print calls made by emit_keys
        expected_print_calls = [
            [],  # Called at step 0
            [],  # Called at step 1
            [],  # Called at step 2
            [],  # Called at step 3
            [],  # Called at step 4
            ["key0", "key1", "key2", "key3", "key4"],  # Called at step 5
            ["key1", "key2", "key3", "key4", "key5"],  # Called at step 6
            ["key2", "key3", "key4", "key5", "key6"],  # Called at step 7
        ]

        # Extract and sort actual calls to print and compare them to the expected calls
        actual_print_calls = [call[0][0] for call in mock_print.call_args_list]
        actual_print_calls_sorted = [sorted(call) for call in actual_print_calls]

        # Compare actual / expected output
        self.assertEqual(actual_print_calls_sorted, expected_print_calls)

    def test_emit_keys_called_when_terminal_node(self):
        """Test for key emittion on terminal node

        Expected: The emit_keys method should no be called.
        """
        self.node_terminal.emit_keys = MagicMock()

        # Simulate receiving and processing keys up to just before the window is full
        for step in range(1, 5):
            keys = [f"key{step}"]
            self.node_terminal.receive_and_process(keys, step)

        # Check that emit_keys was not called
        self.node_terminal.emit_keys.assert_not_called()


if __name__ == "__main__":
    unittest.main()

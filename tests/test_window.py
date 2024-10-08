import unittest

from topology.node.state.Window import Window


class MockOperation:
    """
    Mock class for Operation to simulate cycle calculation based on occurrences.
    """

    def calculate_cycles(self, occurrences: int) -> int:
        # Simulate a operation calculation based on occurrences NestedLoop
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


class TestWindow(unittest.TestCase):
    def setUp(self):
        """
        Create a test window and operation object for use in tests.
        """
        self.window = Window(start_step=0, window_size=10, slide=5)
        self.operation = MockOperation()

    def test_process_within_throughput(self):
        """
        Test processing all keys within throughput limit.
        """
        self.window.keys = load_keys()

        throughput = 150  # High enough to process all keys

        # Call the process method
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.operation, step_cycles=0
        )

        # Assertions:

        # All 20 keys should be processed
        self.assertEqual(processed_keys, 20)
        # 25 + 16 + 36 + 25 = 102 cycles should be used
        self.assertEqual(cycles, 102)
        # Check processed key counts
        self.assertDictEqual(
            processed_key_count, {"key1": 5, "key2": 4, "key3": 6, "key4": 5}
        )
        # Window should be empty after processing
        self.assertEqual(self.window.keys, [])

    def test_process_with_throughput_limit(self):
        """
        Test processing keys where throughput limit is reached mid-way.
        """
        self.window.keys = load_keys()

        throughput = 73  # Set a low throughput to force incomplete processing

        # Call the process method
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.operation, step_cycles=0
        )

        # Assertions:

        # 4 key1 + 4 key2 + 5key3 + 3 key4 = 16 processed keys
        self.assertEqual(processed_keys, 16)
        # 16 (key1) + 16 (key2) + 25 (key3) + 9 (key4) = 66 cycles should be used
        # Next key is key1 so we would have 5 key1 instead of 4 so the cost would have been 66 + (25 - 16) = 75 > 73
        self.assertEqual(cycles, 66)
        # Processed key counts for first <processed_keys> = 16 keys --> ["key1", "key4", "key1", "key3", "key2", "key2", "key3", "key4", "key2", "key3", "key1", "key2", "key1", "key3", "key3", "key4"]
        self.assertDictEqual(
            processed_key_count, {"key1": 4, "key2": 4, "key3": 5, "key4": 3}
        )
        # Assert remaining unprocessed keys
        expected_remaining_keys = [
            "key1",
            "key4",
            "key4",
            "key3",
        ]
        self.assertEqual(self.window.keys, expected_remaining_keys)

    def test_process_empty_window(self):
        """
        Test processing an empty window.
        """
        self.window.keys = []  # Explicitly set to an empty window
        throughput = 100

        # Call the process method on an empty window
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.operation, step_cycles=0
        )

        # Assertions
        self.assertEqual(processed_keys, 0)  # No keys processed
        self.assertEqual(cycles, 0)  # No cycles used
        self.assertDictEqual(processed_key_count, {})  # No key counts

    def test_process_exact_throughput(self):
        """
        Test processing where throughput is exactly enough to process all keys.
        """
        # Add keys to the window
        self.window.keys = load_keys()

        throughput = 102  # Set throughput to be just enough for all keys

        # Call the process method
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.operation, step_cycles=0
        )

        # Assertions
        self.assertEqual(processed_keys, 20)  # All keys should be processed
        self.assertEqual(cycles, throughput)  # Cycles should be equal to throughput
        self.assertDictEqual(
            processed_key_count, {"key1": 5, "key2": 4, "key3": 6, "key4": 5}
        )  # Check key counts
        # Window should be empty
        self.assertEqual(self.window.keys, [])

    def test_process_with_step_cycles(self):
        """
        Test processing when some cycles have already been used.
        """
        self.window.keys = load_keys()

        throughput = 150  # High throughput
        step_cycles = 77  # Already used cycles

        # 77 cycles have already been used, so actual throughput is 150 - 77 = 73, so we expect same results as test_process_with_throughput_limit

        # Call the process method
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.operation, step_cycles
        )

        # Assertions:

        # 4 key1 + 4 key2 + 5key3 + 3 key4 = 16 processed keys
        self.assertEqual(processed_keys, 16)
        # 16 (key1) + 16 (key2) + 25 (key3) + 9 (key4) = 66 cycles should be used
        # Next key is key1 so we would have 5 key1 instead of 4 so the cost would have been 66 + (25 - 16) = 75 > 73
        self.assertEqual(cycles, 66)
        # Processed key counts for first <processed_keys> = 16 keys --> ["key1", "key4", "key1", "key3", "key2", "key2", "key3", "key4", "key2", "key3", "key1", "key2", "key1", "key3", "key3", "key4"]
        self.assertDictEqual(
            processed_key_count, {"key1": 4, "key2": 4, "key3": 5, "key4": 3}
        )
        # Assert remaining unprocessed keys
        expected_remaining_keys = [
            "key1",
            "key4",
            "key4",
            "key3",
        ]
        self.assertEqual(self.window.keys, expected_remaining_keys)


if __name__ == "__main__":
    unittest.main()

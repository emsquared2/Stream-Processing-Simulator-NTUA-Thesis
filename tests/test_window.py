import unittest

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


class TestWindow(unittest.TestCase):

    def setUp(self):
        """
        Create a test window and complexity object for use in tests.
        """
        self.window = Window(start_step=0, window_size=10)
        self.complexity = MockComplexity()

    def test_process_within_throughput(self):
        """
        Test processing all keys within throughput limit.
        """
        self.window.keys = load_keys()

        throughput = 150  # High enough to process all keys

        # Call the process method
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.complexity
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
            throughput, self.complexity
        )

        # Assertions:

        # 5 key1 + 4 key2 = 9 processed keys
        self.assertEqual(processed_keys, 9)
        # 25 (key1) + 16 (key2) = 41 cycles should be used
        self.assertEqual(cycles, 41)
        # Processed key counts for first <processed_keys> = 9 keys --> ["key1", "key4", "key1", "key3", "key2", "key2", "key3", "key4", "key2"]
        self.assertDictEqual(
            processed_key_count, {"key1": 2, "key2": 3, "key3": 2, "key4": 2}
        )
        # Assert remaining unprocessed keys
        expected_remaining_keys = [
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
        self.assertEqual(self.window.keys, expected_remaining_keys)

    def test_process_empty_window(self):
        """
        Test processing an empty window.
        """
        self.window.keys = []  # Explicitly set to an empty window
        throughput = 100

        # Call the process method on an empty window
        processed_keys, cycles, processed_key_count = self.window.process(
            throughput, self.complexity
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
            throughput, self.complexity
        )

        # Assertions
        self.assertEqual(processed_keys, 20)  # All keys should be processed
        self.assertEqual(cycles, throughput)  # Cycles should be equal to throughput
        self.assertDictEqual(
            processed_key_count, {"key1": 5, "key2": 4, "key3": 6, "key4": 5}
        )  # Check key counts
        # Window should be empty
        self.assertEqual(self.window.keys, [])


if __name__ == "__main__":
    unittest.main()

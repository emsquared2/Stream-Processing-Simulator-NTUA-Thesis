import os
import sys

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from keygen.KeyGenerator import KeyGenerator
from utils.ConfigValidator import validate_keygen_config


class TestKeyGenerator(unittest.TestCase):

    def setUp(self):
        self.valid_config = {
            "streams": 1,
            "steps": 5,
            "number_of_keys": 3,
            "arrival_rate": 10,
            "spike_probability": 20,
            "spike_magnitude": 50,
            "distribution": {"type": "uniform"},
        }

    def test_validate_keygen_config(self):
        # Test valid config
        try:
            validate_keygen_config(self.valid_config)
            print("test_validate_keygen_config: Valid config passed")
        except SystemExit:
            self.fail(
                "validate_keygen_config raised SystemExit unexpectedly for a valid config!"
            )

        # Test invalid config: missing keys
        invalid_config_missing_key = {
            "streams": 1,
            "steps": 5,
            "number of keys": 3,
            "arrival rate": 10,
            "spike_probability": 20,
            "spike_magnitude": 50,
            "distribution": {
                "type": "normal",
                "mean": 0,
                # Missing 'stddev'
            },
        }
        with self.assertRaises(SystemExit):
            validate_keygen_config(invalid_config_missing_key)

        # Test invalid config: incorrect value types
        invalid_config_incorrect_type = {
            "streams": 1,
            "steps": "5",  # Should be int
            "number of keys": 3,
            "arrival rate": 10,
            "spike_probability": 20,
            "spike_magnitude": 50,
            "distribution": {"type": "normal", "mean": 0, "stddev": 1},
        }
        with self.assertRaises(SystemExit):
            validate_keygen_config(invalid_config_incorrect_type)

    def test_key_generator(self):
        keygen = KeyGenerator(self.valid_config)

        # Test create_key_array
        keys = keygen.create_key_array(3, key=True)
        self.assertEqual(keys, ["key0", "key1", "key2"])

        # Test adjust_or_create_key_dist
        adjusted_keys = keygen.adjust_or_create_key_dist(keys, swap=True)
        self.assertEqual(len(adjusted_keys), 3)

        # Test replace_step_with_keys
        step = ["0", "1", "0", "2", "0", "1"]
        replaced_step = keygen.replace_step_with_keys(step, ["key0", "key1", "key2"])
        self.assertEqual(
            replaced_step, ["key0", "key1", "key0", "key2", "key0", "key1"]
        )

        # Test generate_step
        generated_step = keygen.generate_step(keys)
        self.assertEqual(len(generated_step), keygen.arrival_rate)

        # Test generate_stream
        keygen.generate_stream("test_output.txt")
        for i in range(self.valid_config["streams"]):
            with open(f"test_output.txt", "r") as f:
                content = f.read()
                self.assertTrue(content)

        # Test generate_input
        keygen.generate_input("test_output.txt")
        for i in range(self.valid_config["streams"]):
            with open(f"test_output{i}.txt", "r") as f:
                content = f.read()
                self.assertTrue(content)


if __name__ == "__main__":
    unittest.main()

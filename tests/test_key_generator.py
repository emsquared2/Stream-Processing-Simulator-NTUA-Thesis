import unittest
from keygen.KeyGenerator import KeyGenerator
from utils.utils import validate_config


class TestKeyGenerator(unittest.TestCase):

    def setUp(self):
        self.valid_config = {
            "streams": 1,
            "steps": 5,
            "number of keys": 3,
            "arrival rate": 10,
            "spike_probability": 20,
            "spike_magnitude": 50,
            "distribution": {"type": "uniform"},
        }

    def test_validate_config(self):
        # Test valid config
        try:
            validate_config(self.valid_config)
            print("test_validate_config: Valid config passed")
        except SystemExit:
            self.fail(
                "validate_config raised SystemExit unexpectedly for a valid config!"
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
            validate_config(invalid_config_missing_key)

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
            validate_config(invalid_config_incorrect_type)

    def test_key_generator(self):
        keygen = KeyGenerator(self.valid_config)

        # Test create_key_array
        keys = keygen.create_key_array(3, key=True)
        self.assertEqual(
            keys, ["key0", "key1", "key2"], f"create_key_array failed: {keys}"
        )

        # Test adjust_or_create_key_dist
        adjusted_keys = keygen.adjust_or_create_key_dist(keys, swap=True)
        self.assertEqual(
            len(adjusted_keys), 3, f"adjust_or_create_key_dist failed: {adjusted_keys}"
        )

        # Test replace_step_with_keys
        step = ["0", "1", "0", "2", "0", "1"]
        replaced_step = keygen.replace_step_with_keys(step, ["key0", "key1", "key2"])
        self.assertEqual(
            replaced_step,
            ["key0", "key1", "key0", "key2", "key0", "key1"],
            f"replace_step_with_keys failed: {replaced_step}",
        )

        # Test generate_step
        generated_step = keygen.generate_step(keys)
        self.assertEqual(
            len(generated_step),
            keygen.arrival_rate,
            f"generate_step failed: {generated_step}",
        )

        # Test generate_stream
        try:
            keygen.generate_stream("test_output.txt")
        except Exception as e:
            self.fail(f"generate_stream raised Exception unexpectedly: {e}")

        # Test generate_input
        try:
            keygen.generate_input("test_output.txt")
        except Exception as e:
            self.fail(f"generate_input raised Exception unexpectedly: {e}")


if __name__ == "__main__":
    unittest.main()

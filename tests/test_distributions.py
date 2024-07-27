import unittest
from keygen.distributions.normal import NormalDistribution
from keygen.distributions.uniform import UniformDistribution
import numpy as np


class TestDistributions(unittest.TestCase):

    def setUp(self):
        self.keys = ["key1", "key2", "key3", "key4", "key5"]
        self.arrival_rate = 10000

    def _check_key_counts(self, generated_keys, expected_key_set):
        """Helper method to check key counts and frequencies."""
        print(f"Generated {len(generated_keys)} keys.")

        self.assertEqual(
            len(generated_keys),
            self.arrival_rate,
            f"Expected {self.arrival_rate} keys but got {len(generated_keys)}",
        )

        # Check that all generated keys are in the provided list of keys
        invalid_keys = [key for key in generated_keys if key not in expected_key_set]
        self.assertFalse(invalid_keys, f"Generated invalid keys: {invalid_keys}")

    def _check_frequencies(self, key_counts, expected_frequency, tolerance=0.01):
        """Helper method to check the frequencies of the keys."""
        frequencies = np.array(list(key_counts.values())) / self.arrival_rate
        print(f"Key frequencies: {frequencies}")

        for frequency in frequencies:
            self.assertAlmostEqual(
                frequency,
                expected_frequency,
                delta=tolerance,
                msg=f"Expected frequency {expected_frequency}, but got {frequency}",
            )

    def test_normal_distribution(self):
        test_cases = [
            (0, 1),  # mean=0, stddev=1
            (5, 2),  # mean=5, stddev=2
            (-3, 1.5),  # mean=-3, stddev=1.5
        ]

        for mean, stddev in test_cases:
            with self.subTest(mean=mean, stddev=stddev):
                distribution = NormalDistribution(self.keys, mean, stddev)
                generated_keys = distribution.generate(self.arrival_rate)
                print(
                    f"Generated keys (Normal Distribution, mean={mean}, stddev={stddev}): {generated_keys[:10]}..."
                )  # Print only the first 10 keys for brevity

                self._check_key_counts(generated_keys, self.keys)

                # Calculate frequencies and check their sum
                key_counts = {key: generated_keys.count(key) for key in self.keys}
                frequencies = np.array(list(key_counts.values())) / self.arrival_rate
                print(
                    f"Frequencies (Normal Distribution, mean={mean}, stddev={stddev}): {frequencies}"
                )

                self.assertAlmostEqual(
                    np.sum(frequencies),
                    1,
                    places=2,
                    msg=f"Frequencies do not sum to 1: {frequencies}",
                )

    def test_uniform_distribution(self):
        distribution = UniformDistribution(self.keys)
        generated_keys = distribution.generate(self.arrival_rate)
        print(
            f"Generated keys (Uniform Distribution): {generated_keys[:10]}..."
        )  # Print only the first 10 keys for brevity

        self._check_key_counts(generated_keys, self.keys)

        # Calculate frequencies and check that they are close to uniform
        key_counts = {key: generated_keys.count(key) for key in self.keys}
        expected_frequency = 1 / len(self.keys)
        print(f"Expected frequency: {expected_frequency}")

        self._check_frequencies(key_counts, expected_frequency)


if __name__ == "__main__":
    unittest.main(verbosity=2)

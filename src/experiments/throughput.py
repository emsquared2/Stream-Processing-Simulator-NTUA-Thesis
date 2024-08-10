from pathlib import Path
import time
from experiment import run_experiment


def main():
    # Define the configuration and base output file paths
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    config_file = project_root / "config.json"
    base_output_dir = project_root / "input/stream_output/throughput"
    base_output_file = base_output_dir / "throughput"

    # Create the output directory if it does not exist
    base_output_dir.mkdir(parents=True, exist_ok=True)

    # Define the range of throughput values to test
    throughput_values = [500, 1000, 1500, 2000, 2500]

    # Run the experiment for each throughput value
    for throughput in throughput_values:
        output_file = f"{base_output_file}_{throughput}_stream_"
        print(f"Running experiment with throughput={throughput}")
        run_experiment(config_file, output_file, throughput=throughput)

        time.sleep(1)


if __name__ == "__main__":
    main()

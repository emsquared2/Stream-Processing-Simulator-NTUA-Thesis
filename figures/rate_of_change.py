import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


def collect_load_data_from_logs(log_folder, nodes):
    all_node_loads = []
    steps = []

    for node in nodes:
        log_filename = f"log_{node}.log"
        log_path = os.path.join(log_folder, log_filename)

        # Check if the log file exists for the node
        if os.path.exists(log_path):
            node_steps, _, _, node_loads, _, _ = parse_log_file(log_path)

            # Ensure steps are consistent
            if not steps:
                steps = node_steps

            all_node_loads.append(node_loads)
        else:
            print(f"Log file for node '{node}' not found: {log_filename}")

    return steps, all_node_loads


# Function to calculate the average load across nodes for each time step
def calculate_average_load(all_node_loads):
    all_node_loads = np.array(all_node_loads)  # Convert to a NumPy array
    avg_loads = np.mean(
        all_node_loads, axis=0
    )  # Compute the mean load across all nodes
    return avg_loads


# Provide the folder path containing log files
log_folder_3workers = "../experiments/topology2/Scenario5/3workers/log_topology2_2"
log_folder_4workers = "../experiments/topology2/Scenario5/4workers/log_topology2_2"
log_folder_6workers = "../experiments/topology2/Scenario5/6workers/log_topology2_2"

# Worker configurations
nodes_3workers = ["node7", "node8", "node9"]
nodes_4workers = ["node7", "node8", "node9", "node10"]
nodes_6workers = ["node7", "node8", "node9", "node10", "node11", "node12"]

# List of colors and marker styles for the lines
color_list = ["blue", "green", "red"]
line_styles = ["-", "-", "-"]

# List of worker configurations to iterate over
worker_configs = [
    ("3 Workers", log_folder_3workers, nodes_3workers),
    ("4 Workers", log_folder_4workers, nodes_4workers),
    ("6 Workers", log_folder_6workers, nodes_6workers),
]

# Initialize data for rate of change
rate_of_change_data = {}

# Collect data for all configurations
for idx, (label, log_folder, nodes) in enumerate(worker_configs):
    # Collect node loads from the log files for the specific worker configuration
    steps, all_node_loads = collect_load_data_from_logs(log_folder, nodes)

    if not all_node_loads:
        continue  # Skip if no load data is found

    # Calculate the average load across all nodes
    avg_loads = calculate_average_load(all_node_loads)

    # Calculate rate of change (delta)
    delta_loads = np.diff(avg_loads)
    smoothed_delta_loads = gaussian_filter1d(delta_loads, sigma=3)  # Increase smoothing
    rate_of_change_data[label] = (steps[:-1], smoothed_delta_loads)

### Plot Rate of Change (Delta Plot) ###

plt.figure(figsize=(12, 6))

for idx, (label, (steps_delta, delta_loads)) in enumerate(rate_of_change_data.items()):
    # Plot the rate of change with markers
    plt.plot(
        steps_delta,
        delta_loads,
        label=f"Rate of Change: {label}",
        color=color_list[idx % len(color_list)],
        linestyle=line_styles[idx % len(line_styles)],
        linewidth=2,
        markersize=5,  # Adjust marker size
    )

    # Highlight local extrema (max/min) and display values in the same color as the line
    local_max = np.argmax(delta_loads)
    local_min = np.argmin(delta_loads)

    # Plot circles for max and crosses for min with same color as the line
    plt.scatter(
        steps_delta[local_max],
        delta_loads[local_max],
        color=color_list[idx % len(color_list)],
        s=100,
        marker="o",  # Circle for max
        zorder=5,
    )
    plt.scatter(
        steps_delta[local_min],
        delta_loads[local_min],
        color=color_list[idx % len(color_list)],
        s=100,
        marker="x",  # Cross for min
        zorder=5,
    )

    # Adjust annotations for specific configurations
    if label == "4 Workers":
        # Display the max value higher and the min more to the right
        plt.text(
            steps_delta[local_max],
            delta_loads[local_max] + 1.1,  # Move higher
            f"{delta_loads[local_max]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )
        plt.text(
            steps_delta[local_min] + 3,  # Move more to the right
            delta_loads[local_min] - 1,
            f"{delta_loads[local_min]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )
    elif label == "6 Workers":
        # Display the max value more to the right
        plt.text(
            steps_delta[local_max] + 5.7,  # Move to the right
            delta_loads[local_max] + 0.5,
            f"{delta_loads[local_max]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )
        plt.text(
            steps_delta[local_min] + 2.5,  # Move more to the right
            delta_loads[local_min] - 1,
            f"{delta_loads[local_min]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )
    else:
        # Default behavior for other configurations
        plt.text(
            steps_delta[local_max],
            delta_loads[local_max] + 0.5,
            f"{delta_loads[local_max]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )
        plt.text(
            steps_delta[local_min],
            delta_loads[local_min] - 0.8,
            f"{delta_loads[local_min]:.2f}",
            color="black",
            fontsize=10,
            fontweight="bold",
            ha="center",
        )

# Add title and labels with increased font sizes
plt.title("Rate of Change in Load for Each Worker Configuration", fontsize=16)
plt.xlabel("Steps", fontsize=14)
plt.ylabel("Rate of Change in Load (%)", fontsize=14)

# Update the legend to include markers for max and min
plt.legend()

# Customize grid for better readability
plt.grid(True, which="both", linestyle="--", linewidth=0.7, alpha=0.7)

# Save Rate of Change plot
plt.tight_layout()
plt.savefig(
    "../experiments/topology2/Scenario5/load_rate_of_change_with_markers.png", dpi=300
)

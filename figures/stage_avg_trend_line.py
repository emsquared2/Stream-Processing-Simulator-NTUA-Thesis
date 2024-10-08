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

# Create a list of colors to pick from
color_list = ["blue", "green", "red"]

plt.style.use("classic")

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Ensure white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# List of worker configurations to iterate over
worker_configs = [
    ("3 Workers", log_folder_3workers, nodes_3workers),
    ("4 Workers", log_folder_4workers, nodes_4workers),
    ("6 Workers", log_folder_6workers, nodes_6workers),
]

# Iterate over each worker configuration
for idx, (label, log_folder, nodes) in enumerate(worker_configs):
    # Collect node loads from the log files for the specific worker configuration
    steps, all_node_loads = collect_load_data_from_logs(log_folder, nodes)

    if not all_node_loads:
        continue  # Skip if no load data is found

    # Calculate the average load across all nodes
    avg_loads = calculate_average_load(all_node_loads)

    # Apply Gaussian smoothing for a continuous trend line
    smoothed_avg = gaussian_filter1d(avg_loads, sigma=2)

    # Plot the smoothed trend line for this worker configuration
    ax.plot(
        steps,
        smoothed_avg,
        label=f"Avg Load Trend: {label}",
        color=color_list[idx % len(color_list)],
        linewidth=3,
    )

# Add labels and title
ax.set_xlabel("Steps")
ax.set_ylabel("Average Load (%)")
ax.set_title("Average Stage Load Trend for Each Worker Configuration")


# Set x-axis limits to start from 0
ax.set_xlim(left=0)

# Add a legend outside the plot
ax.legend(loc="upper left", framealpha=0.5)

# Add grid for readability
ax.grid(True, which="both", linestyle="--", linewidth=0.5)

# Display the plot with tight layout to adjust for the legend
plt.tight_layout()
plt.savefig(
    "../experiments/topology2/Scenario5/topology2_stage_load.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)
plt.close()

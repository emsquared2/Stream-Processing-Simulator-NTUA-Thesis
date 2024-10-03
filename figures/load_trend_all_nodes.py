import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scipy.ndimage import gaussian_filter1d
from utils.log_parser import parse_log_file


def collect_load_data_from_logs(log_folder, node):
    node_loads = []
    steps = []

    log_filename = f"log_{node}.log"
    log_path = os.path.join(log_folder, log_filename)

    # Check if the log file exists for the node
    if os.path.exists(log_path):
        steps, _, node_loads, _, _ = parse_log_file(log_path)
    else:
        print(f"Log file for node '{node}' not found: {log_filename}")

    return steps, node_loads


# Provide the folder path containing log files
log_folder = "../experiments/Scenario2 - Increasing Arrival Rate/log_20241002205012"

# Provide the list of nodes to read logs for
nodes = ["node1", "node2", "node5", "node6"]  # Update with your actual node names

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Ensure white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Iterate over each node and plot the load trend
for node in nodes:
    # Collect node loads from the log file for the specific node
    steps, node_loads = collect_load_data_from_logs(log_folder, node)

    if not node_loads:
        continue  # Skip if no load data is found for this node

    # Apply Gaussian smoothing for a continuous trend line
    smoothed_avg = gaussian_filter1d(node_loads, sigma=2)

    # Plot the smoothed trend line for this node
    ax.plot(
        steps,
        smoothed_avg,
        label=f"Load Trend: {node}",
        linewidth=2,
    )

# Add labels and title
ax.set_xlabel("Steps")
ax.set_ylabel("Node Load (%)")
ax.set_title("Node Load Percentage Trend Across Nodes")

# Set x-axis limits to start from 0
ax.set_xlim(left=0)

# Add a legend outside the plot
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

# Add grid for readability
ax.grid(True, which="both", linestyle="--", linewidth=0.5)

# Display the plot with tight layout to adjust for the legend
plt.tight_layout()
plt.show()

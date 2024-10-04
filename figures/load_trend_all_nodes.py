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
log_folder = (
    "../experiments/Scenario7 - Scalability/four_workers/Scenario3/topology1_high_pkg/"
)

# Provide the list of nodes to read logs for
# nodes = ["node1", "node2", "node1_aggr", "node4"]
# nodes = ["node1", "node2", "node5"]

# nodes = ["node1", "node2", "node3", "node4", "node9"]
nodes = ["node1", "node2", "node3", "node4", "node6", "node1_aggr"]


# Create a list of colors to pick from
color_list = ["blue", "green", "red", "#b7950b", "#ff7f0e", "magenta", "cyan"]

plt.style.use("classic")

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Ensure white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# # List of marker styles to cycle through for each node
# markers = ["o", "s", "^", "D"]

# # Iterate over each node and plot the load trend
# for idx, node in enumerate(nodes):
#     # Collect node loads from the log file for the specific node
#     steps, node_loads = collect_load_data_from_logs(log_folder, node)

#     if not node_loads:
#         continue  # Skip if no load data is found for this node

#     # Apply Gaussian smoothing for a continuous trend line
#     smoothed_avg = gaussian_filter1d(node_loads, sigma=2)

#     # Plot the smoothed trend line for this node with markers
#     ax.plot(
#         steps,
#         smoothed_avg,
#         label=f"Load Trend: {node}",
#         marker=markers[idx % len(markers)],  # Cycle through markers
#         linewidth=2,
#     )

# Iterate over each node and plot the load trend
for idx, node in enumerate(nodes):
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
        color=color_list[idx % len(color_list)],
        linewidth=3,
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
# ax.grid(True, which="both", linestyle="--", linewidth=0.5)

# Display the plot with tight layout to adjust for the legend
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario7 - Scalability/four_workers/Scenario3/topology_load_high_pkg.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

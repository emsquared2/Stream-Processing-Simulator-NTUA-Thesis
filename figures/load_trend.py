import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file
from scipy.ndimage import gaussian_filter1d


steps, _, node_loads, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/four_workers/Scenario1/topology1/log_node1.log"
)

plt.style.use("classic")

# Apply Gaussian smoothing for a continuous trend line
smoothed_avg = gaussian_filter1d(node_loads, sigma=2)

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Ensure white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Plot the node load percentages as bars
ax.bar(steps, node_loads, color="#2ca02c", label="Node Load (%)")

# Plot the smoothed trend line
ax.plot(
    steps,
    smoothed_avg,
    color="red",
    label="Load Trend Line",
    linewidth=3,
)

# Add labels and title
ax.set_xlabel("Steps")
ax.set_ylabel("Node Load (%)")
ax.set_title("Node Load 1")

# Set x-axis limits to start from 0
ax.set_xlim(left=0)

# Add a legend
ax.legend()

# Add grid for readability (optional)
# ax.grid(True, which="both", linestyle="--", linewidth=0.5)

# Add a legend in the bottom-right corner
ax.legend(loc="lower right")


# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario7 - Scalability/four_workers/Scenario1/load_node1.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

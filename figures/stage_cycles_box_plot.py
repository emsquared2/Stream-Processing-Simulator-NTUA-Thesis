import matplotlib.pyplot as plt
import sys
import os
import numpy as np

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


def add_median_labels(ax, data):
    medians = [np.median(d) for d in data]
    for i, median in enumerate(medians):
        ax.text(
            i + 1.27,
            median,
            f"{median:.2f}",
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=12,
            fontweight="bold",
        )


# Function to calculate stage cycles based on max logic
def calculate_stage_cycles(node1, node2, aggr=None):
    stage_cycles = []
    for i in range(len(node1)):
        max_cycles = max(node1[i], node2[i])  # max(cycles_node1, cycles_node2)
        if aggr:
            max_cycles += aggr[i]  # Add aggregation node cycles if they exist
        stage_cycles.append(max_cycles)
    return stage_cycles


# Load data from log files, slicing to ignore the first 4 steps for each node
_, _, node1_cycles, _, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node1.log"
)
_, _, node2_cycles, _, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node2.log"
)
_, _, node3_cycles, _, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node3.log"
)

_, _, node1_cycles_potc, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node1.log"
)
_, _, node2_cycles_potc, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node2.log"
)
_, _, node3_cycles_potc, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node3.log"
)

_, _, node1_cycles_pkg, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node1.log"
)
_, _, node2_cycles_pkg, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node2.log"
)
_, _, node3_cycles_pkg, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node3.log"
)


# Load aggregation node cycles if they exist
_, _, node1_aggr_cycles, _, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node1_aggr.log"
)

# Compute the stage cycles for each strategy
stage_cycles_hashing = calculate_stage_cycles(node1_cycles[4:], node2_cycles[4:])
stage_cycles_potc = calculate_stage_cycles(node1_cycles_potc[4:], node2_cycles_potc[4:])
stage_cycles_pkg = calculate_stage_cycles(
    node1_cycles_pkg[4:], node2_cycles_pkg[4:], node1_aggr_cycles[4:]
)

# Prepare the data in a list form for boxplot
data = [
    stage_cycles_hashing,
    stage_cycles_potc,
    stage_cycles_pkg,
]

plt.style.use("classic")

# Creating empty labels for each individual node
# node_labels = [""] * len(data)

node_labels = ["Hashing", "PoTC", "PKG"]

# Plotting the boxplot with white background
fig, ax = plt.subplots(
    figsize=(12, 6), facecolor="white"
)  # Set figure background to white
plt.boxplot(data, labels=node_labels)

add_median_labels(ax, data)

# Add central labels for each strategy
# plt.xticks([1, 2, 3], ["Hashing", "PoTC", "PKG"])

# Add titles and labels
plt.title("Stage 1 Processing Cycles Used")
plt.xlabel("Strategies")
plt.ylabel("Cycles per Step")

# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario6 - Partition Strategies/Scenario5 - comparison/stage_cycles_comparison.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


# Function to add median labels just above the median line
def add_median_labels(ax, data):
    medians = [np.median(d) for d in data]
    for i, median in enumerate(medians):
        # Adjust x and y position to place it next to the box
        ax.text(
            i + 1.25,
            median,
            f"{median:.2f}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
            fontweight="bold",
        )


# Three Workers - Stage 2 (dummy data for demo purposes)
_, _, _, node7_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node7.log"
)
_, _, _, node8_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node8.log"
)
_, _, _, node9_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node9.log"
)

# Four Workers - Stage 2
_, _, _, node7_load_4, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/4workers/log_topology2/log_node7.log"
)
_, _, _, node8_load_4, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/4workers/log_topology2/log_node8.log"
)
_, _, _, node9_load_4, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/4workers/log_topology2/log_node9.log"
)
_, _, _, node10_load_4, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/4workers/log_topology2/log_node10.log"
)

# Six Workers - Stage 2
_, _, _, node7_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node7.log"
)
_, _, _, node8_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node8.log"
)
_, _, _, node9_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node9.log"
)
_, _, _, node10_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node10.log"
)
_, _, _, node11_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node11.log"
)
_, _, _, node12_load_6, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/6workers/log_topology2/log_node12.log"
)


# Filter Stage 2 loads to include only steps 8, 11, 14, ...
def filter_stage2_load(load):
    return [load[i] for i in range(8, len(load), 3)]


node7_load_3 = filter_stage2_load(node7_load_3)
node8_load_3 = filter_stage2_load(node8_load_3)
node9_load_3 = filter_stage2_load(node9_load_3)

node7_load_4 = filter_stage2_load(node7_load_4)
node8_load_4 = filter_stage2_load(node8_load_4)
node9_load_4 = filter_stage2_load(node9_load_4)
node10_load_4 = filter_stage2_load(node10_load_4)

node7_load_6 = filter_stage2_load(node7_load_6)
node8_load_6 = filter_stage2_load(node8_load_6)
node9_load_6 = filter_stage2_load(node9_load_6)
node10_load_6 = filter_stage2_load(node10_load_6)
node11_load_6 = filter_stage2_load(node11_load_6)
node12_load_6 = filter_stage2_load(node12_load_6)

# Calculate avg load
stage2_load_3 = [
    (n7 + n8 + n9) / 3 for n7, n8, n9 in zip(node7_load_3, node8_load_3, node9_load_3)
]
stage2_load_4 = [
    (n7 + n8 + n9 + n10) / 4
    for n7, n8, n9, n10 in zip(node7_load_4, node8_load_4, node9_load_4, node10_load_4)
]
stage2_load_6 = [
    (n7 + n8 + n9 + n10 + n11 + n12) / 6
    for n7, n8, n9, n10, n11, n12 in zip(
        node7_load_6,
        node8_load_6,
        node9_load_6,
        node10_load_6,
        node11_load_6,
        node12_load_6,
    )
]

# Calculate max load
stage2_max_load_3 = [
    max(n7, n8, n9) for n7, n8, n9 in zip(node7_load_3, node8_load_3, node9_load_3)
]
stage2_max_load_4 = [
    max(n7, n8, n9, n10)
    for n7, n8, n9, n10 in zip(node7_load_4, node8_load_4, node9_load_4, node10_load_4)
]
stage2_max_load_6 = [
    max(n7, n8, n9, n10, n11, n12)
    for n7, n8, n9, n10, n11, n12 in zip(
        node7_load_6,
        node8_load_6,
        node9_load_6,
        node10_load_6,
        node11_load_6,
        node12_load_6,
    )
]

data_avg = [stage2_load_3, stage2_load_4, stage2_load_6]
data_max = [stage2_max_load_3, stage2_max_load_4, stage2_max_load_6]

# Labels for grouping workers
node_labels = [
    "3 Workers",
    "4 Workers",
    "6 Workers",
]

# Plot for Average Load
plt.style.use("classic")
fig1, ax1 = plt.subplots(figsize=(12, 6), facecolor="white")
ax1.boxplot(data_avg, tick_labels=node_labels, showfliers=False)

# Add titles and labels for avg load plot
ax1.set_title("Average Load of Stage 2 Nodes Across Worker Configurations", fontsize=14)
ax1.set_xlabel("Number of Workers", fontsize=12)
ax1.set_ylabel("Average Load (%)", fontsize=12)

# Set the y-axis limit to add a small margin above 100%
ax1.set_ylim(0, 105)  # Adding a little space above the maximum value

# Add median labels just above the median line
add_median_labels(ax1, data_avg)

# Adjust layout and save avg load plot
plt.tight_layout()
plt.savefig(
    "../experiments/topology2/Scenario1/worker_load_comparison_avg.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

# Plot for Max Load
fig2, ax2 = plt.subplots(figsize=(12, 6), facecolor="white")
ax2.boxplot(data_max, tick_labels=node_labels, showfliers=False)

# Add titles and labels for max load plot
ax2.set_title("Maximum Load of Stage 2 Nodes Across Worker Configurations", fontsize=14)
ax2.set_xlabel("Number of Workers", fontsize=12)
ax2.set_ylabel("Max Load (%)", fontsize=12)

# Set the y-axis limit to add a small margin above 100%
ax2.set_ylim(0, 105)  # Adding a little space above the maximum value

# Add median labels just above the median line
add_median_labels(ax2, data_max)

# Adjust layout and save max load plot
plt.tight_layout()
plt.savefig(
    "../experiments/topology2/Scenario1/worker_load_comparison_max.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

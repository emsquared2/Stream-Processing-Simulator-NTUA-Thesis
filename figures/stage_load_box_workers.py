import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
# import seaborn as sns

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


def remove_consecutive_zeros(data_list):
    # Create a new list to store the filtered data
    filtered_data = []

    # Iterate through the list, tracking the current and previous values
    for i in range(len(data_list)):
        # Add the current element to the filtered list if it's not part of a sequence of two or more zeros
        if not(i > 0 and data_list[i] == 0 and data_list[i-1] == 0):
            filtered_data.append(data_list[i])

    return filtered_data


def add_median_labels(ax, data):
    medians = [np.median(d) for d in data]
    for i, median in enumerate(medians):
        ax.text(
            i + 1.5,
            median,
            f"{median:.2f}",
            horizontalalignment="center",
            verticalalignment="bottom",
            fontsize=12,
            fontweight="bold",
        )


# Load data from log files, slicing to ignore the first 4 steps for each node

# Three Workers - Stage 2
_, _, _, node7_hashing, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node7.log"
)
_, _, _, node8_hashing, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node8.log"
)
_, _, _, node9_hashing, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/log_node9.log"
)

# Four Workers - Stage 2
_, _, _, node7_potc, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node7.log"
)
_, _, _, node8_potc, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node8.log"
)
_, _, _, node9_potc, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/log_node9.log"
)

# Six Workers - Stage 2
_, _, _, node7_pkg, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node7.log"
)
_, _, _, node8_pkg, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node8.log"
)
_, _, _, node9_pkg, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node9.log"
)
# _, _, _, node_aggr_pkg, _, _ = parse_log_file(
#     "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/log_node7_aggr.log"
# )

node7_hashing = node7_hashing[5:]
node8_hashing = node8_hashing[5:]
node9_hashing = node9_hashing[5:]

node7_potc = node7_potc[5:]
node8_potc = node8_potc[5:]
node9_potc = node9_potc[5:]

node7_pkg = node7_pkg[5:]
node8_pkg = node8_pkg[5:]
node9_pkg = node9_pkg[5:]



# Applying the function directly to each data list
node7_hashing = remove_consecutive_zeros(node7_hashing)
node8_hashing = remove_consecutive_zeros(node8_hashing)
node9_hashing = remove_consecutive_zeros(node9_hashing)

node7_potc = remove_consecutive_zeros(node7_potc)
node8_potc = remove_consecutive_zeros(node8_potc)
node9_potc = remove_consecutive_zeros(node9_potc)

node7_pkg = remove_consecutive_zeros(node7_pkg)
node8_pkg = remove_consecutive_zeros(node8_pkg)
node9_pkg = remove_consecutive_zeros(node9_pkg)

# Slicing to ignore the first 4 steps for Stage 1 nodes



# # Filter Stage 2 loads to include only steps 8, 11, 14, ...
# def filter_stage2_load(load):
#     return [load[i] for i in range(8, len(load), 3)]


# node7_hashing = filter_stage2_load(node7_hashing)
# node8_hashing = filter_stage2_load(node8_hashing)
# node9_hashing = filter_stage2_load(node9_hashing)

# node7_potc = filter_stage2_load(node7_potc)
# node8_potc = filter_stage2_load(node8_potc)
# node9_potc = filter_stage2_load(node9_potc)
# node70_potc = filter_stage2_load(node70_potc)

# node7_pkg = filter_stage2_load(node7_pkg)
# node8_pkg = filter_stage2_load(node8_pkg)
# node9_pkg = filter_stage2_load(node9_pkg)
# node70_pkg = filter_stage2_load(node70_pkg)
# node71_pkg = filter_stage2_load(node71_pkg)
# node72_pkg = filter_stage2_load(node72_pkg)

# Calculate the average load for each stage by summing the loads and dividing by the number of nodes
# Stage 1 has 3 nodes for all worker configurations
# stage2_hashing = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_hashing, node8_hashing, node9_hashing)
# ]
# stage2_potc = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_potc, node8_potc, node9_potc)
# ]
# stage2_pkg = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_pkg, node8_pkg, node9_pkg)
# ]

# Stage 2 has 3, 4, and 6 nodes for 3, 4, and 6 workers, respectively
stage2_hashing = [
    (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_hashing, node8_hashing, node9_hashing)
]
stage2_potc = [
    (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_potc, node8_potc, node9_potc)
]
stage2_pkg = [
    (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node7_pkg, node8_pkg, node9_pkg)
]

stage2_max_hashing = [
    max(n1, n2, n3) for n1, n2, n3 in zip(node7_hashing, node8_hashing, node9_hashing)
]
stage2_max_potc = [
    max(n1, n2, n3) for n1, n2, n3 in zip(node7_potc, node8_potc, node9_potc)
]
stage2_max_pkg = [
    max(n1, n2, n3) for n1, n2, n3 in zip(node7_pkg, node8_pkg, node9_pkg)
]

data = [
    stage2_hashing,
    stage2_max_hashing,
    stage2_potc,
    stage2_max_potc,
    stage2_pkg,
    stage2_max_pkg,
    # node_aggr_pkg
]

# Prepare the data in a list form for each number of workers (average of Stage 1 and Stage 2)
# data = [
#     # stage2_hashing,
#     stage2_hashing,  # 3 Workers (Stage 1, Stage 2)
#     # stage2_potc,
#     stage2_potc,  # 4 Workers (Stage 1, Stage 2)
#     # stage2_pkg,
#     stage2_pkg,  # 6 Workers (Stage 1, Stage 2)
# ]

# Labels for grouping workers
node_labels = [
    "hashing avg",
    "hashing max",
    "potc avg",
    "potc max",
    "pkg avg",
    "pkg max",
    # "pkg aggregator"
]

# Plot for Average Load
plt.style.use("classic")
fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")
ax.boxplot(data, labels=node_labels)

ax.set_ylim(0, 105)

# Add central labels for each worker configuration
plt.xticks([1, 2, 3, 4, 5, 6], node_labels)

add_median_labels(ax, data)
# Add titles and labels
plt.title("Average and Max Stage 2 Node Load for hashing, potc, pkg strategies")
plt.xlabel("Partition Strategy")
plt.ylabel("Average and Max Stage 2 Load (%)")

# Adjust layout and save avg load plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario6 - Partition Strategies/Scenario5 - comparison/worker_load_comparison_top2_stage2.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

# # Prepare the data for a violin plot
# sns.violinplot(data)
# plt.xticks([0, 1, 2, 3, 4, 5], node_labels)
# plt.title("Stage 2 Node Load Distribution for Different Worker Configurations")
# plt.ylabel("Node Load (%)")
# plt.xlabel("Number of Workers")
# plt.savefig(
#     "../experiments/Scenario6 - Partition Strategies/scenario1/worker_load_comparison_violin.png",
#     format="png",
#     dpi=300,
#     bbox_inches="tight",
# )

# # Using Seaborn's strip plot
# sns.stripplot(data)
# plt.xticks([0, 1, 2, 3, 4, 5], node_labels)
# plt.title("Individual Node Load Points for Different Worker Configurations")
# plt.ylabel("Node Load (%)")
# plt.xlabel("Number of Workers")
# plt.savefig(
#     "../experiments/Scenario6 - Partition Strategies/scenario1/worker_load_comparison_stripplot.png",
#     format="png",
#     dpi=300,
#     bbox_inches="tight",
# )

# # Plotting a bar plot with error bars (showing confidence intervals)
# sns.barplot(data)
# plt.xticks([0, 1, 2, 3, 4, 5], node_labels)
# plt.savefig(
#     "../experiments/Scenario6 - Partition Strategies/scenario1/worker_load_comparison_bar.png",
#     format="png",
#     dpi=300,
#     bbox_inches="tight",
# )

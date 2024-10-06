import matplotlib.pyplot as plt
import sys
import os
import seaborn as sns

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file

# Load data from log files, slicing to ignore the first 4 steps for each node

# # Three Workers - Stage 1
# _, _, _, node1_load_3, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/3workers/log_topology2/log_node1.log"
# )
# _, _, _, node2_load_3, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/3workers/log_topology2/log_node2.log"
# )
# _, _, _, node3_load_3, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/3workers/log_topology2/log_node3.log"
# )

# Three Workers - Stage 2
_, _, _, node7_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node7.log"
)
_, _, _, node8_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node8.log"
)
_, _, _, node9_load_3, _, _ = parse_log_file(
    "../experiments/topology2/Scenario1/3workers/log_topology2/log_node9.log"
)

# # Four Workers - Stage 1
# _, _, _, node1_load_4, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/4workers/log_topology2/log_node1.log"
# )
# _, _, _, node2_load_4, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/4workers/log_topology2/log_node2.log"
# )
# _, _, _, node3_load_4, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/4workers/log_topology2/log_node3.log"
# )

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

# # Six Workers - Stage 1
# _, _, _, node1_load_6, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/6workers/log_topology2/log_node1.log"
# )
# _, _, _, node2_load_6, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/6workers/log_topology2/log_node2.log"
# )
# _, _, _, node3_load_6, _, _ = parse_log_file(
#     "../experiments/topology2/Scenario1/6workers/log_topology2/log_node3.log"
# )

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

# Slicing to ignore the first 4 steps for Stage 1 nodes
# node1_load_3 = node1_load_3[5:]
# node2_load_3 = node2_load_3[5:]
# node3_load_3 = node3_load_3[5:]

# node1_load_4 = node1_load_4[5:]
# node2_load_4 = node2_load_4[5:]
# node3_load_4 = node3_load_4[5:]

# node1_load_6 = node1_load_6[5:]
# node2_load_6 = node2_load_6[5:]
# node3_load_6 = node3_load_6[5:]


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

# Calculate the average load for each stage by summing the loads and dividing by the number of nodes
# Stage 1 has 3 nodes for all worker configurations
# stage1_load_3 = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node1_load_3, node2_load_3, node3_load_3)
# ]
# stage1_load_4 = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node1_load_4, node2_load_4, node3_load_4)
# ]
# stage1_load_6 = [
#     (n1 + n2 + n3) / 3 for n1, n2, n3 in zip(node1_load_6, node2_load_6, node3_load_6)
# ]

# Stage 2 has 3, 4, and 6 nodes for 3, 4, and 6 workers, respectively
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

data = [
    stage2_load_3,
    stage2_max_load_3,
    stage2_load_4,
    stage2_max_load_4,
    stage2_load_6,
    stage2_max_load_6,
]

# Prepare the data in a list form for each number of workers (average of Stage 1 and Stage 2)
# data = [
#     # stage1_load_3,
#     stage2_load_3,  # 3 Workers (Stage 1, Stage 2)
#     # stage1_load_4,
#     stage2_load_4,  # 4 Workers (Stage 1, Stage 2)
#     # stage1_load_6,
#     stage2_load_6,  # 6 Workers (Stage 1, Stage 2)
# ]

# Labels for grouping workers (centered labels for each worker count with stage differentiation)
node_labels = [
    "3W avg",
    "3W max",
    "4W avg",
    "4W max",
    "4W avg",
    "4W max",
]

# Plotting the boxplot with white background
plt.style.use("classic")
fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")
ax.boxplot(data, tick_labels=node_labels)

# Add central labels for each worker configuration
plt.xticks([1, 2, 3, 4, 5, 6], node_labels)

# Add titles and labels
plt.title("Average and Max Stage 2 Node Load for 3, 4, and 6 Worker Configurations")
plt.xlabel("Number of Workers")
plt.ylabel("Average and Max Stage 2 Load (%)")

# Adjust layout and display the plot
plt.tight_layout()

# Save the plot
plt.savefig(
    "../experiments/topology2/scenario1/worker_load_comparison.png",
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
#     "../experiments/topology2/scenario1/worker_load_comparison_violin.png",
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
#     "../experiments/topology2/scenario1/worker_load_comparison_stripplot.png",
#     format="png",
#     dpi=300,
#     bbox_inches="tight",
# )

# # Plotting a bar plot with error bars (showing confidence intervals)
# sns.barplot(data)
# plt.xticks([0, 1, 2, 3, 4, 5], node_labels)
# plt.savefig(
#     "../experiments/topology2/scenario1/worker_load_comparison_bar.png",
#     format="png",
#     dpi=300,
#     bbox_inches="tight",
# )

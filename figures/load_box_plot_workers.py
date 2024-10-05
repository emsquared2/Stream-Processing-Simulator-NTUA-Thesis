import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file

# Load data from log files, slicing to ignore the first 4 steps for each node

# One Worker
# _, _, node1_load_1, _, _ = parse_log_file(
#     "../experiments/Scenario7 - Scalability/1_worker/Scenario3/topology1/log_node1.log"
# )

# Two Workers
_, _, _, node1_load_2, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/2_workers/Scenario3/topology1/log_node1.log"
)
_, _, _, node2_load_2, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/2_workers/Scenario3/topology1/log_node2.log"
)

# 4 Workers
_, _, _, node1_load_4, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/4_workers/Scenario3/topology1_high_pkg/log_node1.log"
)
_, _, _, node2_load_4, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/4_workers/Scenario3/topology1_high_pkg/log_node2.log"
)
_, _, _, node3_load_4, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/4_workers/Scenario3/topology1_high_pkg/log_node3.log"
)
_, _, _, node4_load_4, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/4_workers/Scenario3/topology1_high_pkg/log_node4.log"
)

# 6 Workers
_, _, _, node1_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node1.log"
)
_, _, _, node2_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node2.log"
)
_, _, _, node3_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node3.log"
)
_, _, _, node4_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node4.log"
)
_, _, _, node5_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node5.log"
)
_, _, _, node6_load_6, _, _ = parse_log_file(
    "../experiments/Scenario7 - Scalability/6_workers/Scenario3/topology1/log_node6.log"
)

# Slicing to ignore the first 4 steps for all nodes
# node1_load_1 = node1_load_1[4:]

node1_load_2 = node1_load_2[4:]
node2_load_2 = node2_load_2[4:]

node1_load_4 = node1_load_4[4:]
node2_load_4 = node2_load_4[4:]
node3_load_4 = node3_load_4[4:]
node4_load_4 = node4_load_4[4:]

node1_load_6 = node1_load_6[4:]
node2_load_6 = node2_load_6[4:]
node3_load_6 = node3_load_6[4:]
node4_load_6 = node4_load_6[4:]
node5_load_6 = node5_load_6[4:]
node6_load_6 = node6_load_6[4:]

# Prepare the data in a list form for each number of workers
data = [
    # node1_load_1,  # One worker
    node1_load_2,
    node2_load_2,  # Two workers
    node1_load_4,
    node2_load_4,
    node3_load_4,
    node4_load_4,  # Four workers
    node1_load_6,
    node2_load_6,
    node3_load_6,
    node4_load_6,
    node5_load_6,
    node6_load_6,  # Six workers
]

plt.style.use("classic")

# Labels for grouping workers (centered labels for each worker count)
node_labels = [""] * len(data)

# Plotting the boxplot with white background
fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")
ax.boxplot(data, tick_labels=node_labels)  # Renamed 'labels' to 'tick_labels'

# Add central labels for each worker configuration
# Adjust positions to center them correctly
plt.xticks([1.5, 3.5, 5.5], ["2 Workers", "4 Workers", "6 Workers"])

# Add titles and labels
plt.title("Node Load Comparison Over Time (Different Number of Workers)")
plt.xlabel("Number of Workers")
plt.ylabel("Node Load (%)")

# Adjust layout and display the plot
plt.tight_layout()

# Save the plot
plt.savefig(
    "../experiments/Scenario7 - Scalability/worker_load_comparison_Scenario3.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

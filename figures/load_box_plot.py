import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file

# Load data from log files, slicing to ignore the first 4 steps for each node
_, _, node1_load_hashing, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varrying Spike/log_topology1_high_spike/log_node1.log"
)
_, _, node2_load_hashing, _, _ = parse_log_file(
    "../experiments/Scenario5 - Varrying Spike/log_topology1_high_spike/log_node2.log"
)

_, _, node1_load_potc, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology1_high/log_node1.log"
)
_, _, node2_load_potc, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology1_high/log_node2.log"
)

_, _, node1_load_pkg, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology1_high/log_node1.log"
)
_, _, node2_load_pkg, _, _ = parse_log_file(
    "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology1_high/log_node2.log"
)
# Prepare the data in a list form
data = [
    node1_load_hashing[4:], node2_load_hashing[4:],
    node1_load_potc[4:], node2_load_potc[4:],
    node1_load_pkg[4:], node2_load_pkg[4:],
]

plt.style.use("classic")

# # Labels for each node
# labels = ["Hashing", "PoTC", "PKG"]

# # Plotting the boxplot
# plt.figure(figsize=(10, 6))
# plt.boxplot(data, labels=labels)
# Creating empty labels for each individual node
node_labels = [""] * len(data)

# Plotting the boxplot
# Plotting the boxplot with white background
fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")# Set figure background to white
plt.boxplot(data, labels=node_labels)

# Add central labels for each strategy
plt.xticks([1.5, 3.5, 5.5], ["Hashing", "PoTC", "PKG"])

# Add titles and labels
plt.title("Node Load Comparison Over Time (Multiple Nodes)")
plt.xlabel("Nodes")
plt.ylabel("Node Load (%)")

# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario6 - Partition Strategies/Scenario5 - comparison/stage1.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)
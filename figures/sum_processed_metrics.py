import os
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


# Function to compute totals for processed, overdue, and expired keys from specific log files
def compute_totals(log_files_dir, selected_logs):
    total_processed = 0
    total_overdue = 0
    total_expired = 0

    # Filter only the selected log files
    for log_file in selected_logs:
        log_path = os.path.join(log_files_dir, log_file)
        if os.path.exists(log_path):
            _, processed_keys, _, _, overdue_keys, expired_keys = parse_log_file(log_path)

            # Sum the keys
            total_processed += sum(processed_keys)
            total_overdue += sum(overdue_keys)
            total_expired += sum(expired_keys)

    return total_processed, total_overdue, total_expired


dir_hashing = "../experiments/Scenario5 - Varying Spike/log_topology2_high_spike/"
dir_potc = "../experiments/Scenario6 - Partition Strategies/potc/Scenario5/topology2_high/"
dir_pkg = "../experiments/Scenario6 - Partition Strategies/pkg/Scenario5/topology2_high/"

# Log files for 2 workers and 4 workers scenarios (specific log files)
log_files_hashing = ["log_node7.log", "log_node8.log", "log_node9.log"]
log_files_potc = ["log_node7.log", "log_node8.log", "log_node9.log"]
log_files_pkg = ["log_node7.log", "log_node8.log", "log_node9.log"]
# log_files_pkg_aggr = ["log_node7_aggr.log"]

# Compute totals for 2 workers
processed_hashing, overdue_hashing, expired_hashing = compute_totals(dir_hashing, log_files_hashing)

# Compute totals for 2 workers
processed_potc, overdue_potc, expired_potc = compute_totals(dir_potc, log_files_potc)

# Compute totals for 4 workers
processed_pkg, overdue_pkg, expired_pkg = compute_totals(dir_pkg, log_files_pkg)

# processed_pkg_aggr, overdue_pkg_aggr, expired_pkg_aggr = compute_totals(dir_pkg, log_files_pkg_aggr)

# Data for plotting
# labels = ["Hashing", "PoTC", "PKG", "PKG Aggregator"]
labels = ["Hashing", "PoTC", "PKG"]
# processed_keys = [processed_hashing, processed_potc, processed_pkg, processed_pkg_aggr]
# overdue_keys = [overdue_hashing, overdue_potc, overdue_pkg, overdue_pkg_aggr]
# expired_keys = [expired_hashing, expired_potc, expired_pkg, expired_pkg_aggr]
processed_keys = [processed_hashing, processed_potc, processed_pkg]
overdue_keys = [overdue_hashing, overdue_potc, overdue_pkg]
expired_keys = [expired_hashing, expired_potc, expired_pkg]

# Plotting
x = np.arange(len(labels))  # the label locations
bar_width = 0.2  # width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bars
p1 = ax.bar(
    x - bar_width, processed_keys, bar_width, label="Processed Keys", color="#1f77b4"
)
p2 = ax.bar(x, overdue_keys, bar_width, label="Overdue Keys", color="#2ca02c")
p3 = ax.bar(
    x + bar_width, expired_keys, bar_width, label="Expired Keys", color="#d62728"
)

# Add some labels and title
ax.set_xlabel("Partition Strategies", fontsize=12)
ax.set_ylabel("Number of Keys", fontsize=12)
ax.set_title("Comparison of Processed, Overdue, and Expired Keys for hashing, potc, pkg strategies", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels)

# Add a legend
ax.legend()

# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario6 - Partition Strategies/Scenario5 - comparison/key_stats_stage2_top2.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

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
            _, processed_keys, _, overdue_keys, expired_keys = parse_log_file(log_path)

            # Sum the keys
            total_processed += sum(processed_keys)
            total_overdue += sum(overdue_keys)
            total_expired += sum(expired_keys)

    return total_processed, total_overdue, total_expired


dir_one_worker = "../experiments/Scenario7 - Scalability/1_worker/Scenario5/topology1/"
dir_two_workers = (
    "../experiments/Scenario7 - Scalability/2_workers/Scenario5/topology1/"
)
dir_four_workers = (
    "../experiments/Scenario7 - Scalability/4_workers/Scenario5/topology1/"
)
dir_six_workers = (
    "../experiments/Scenario7 - Scalability/6_workers/Scenario5/topology1/"
)

# Log files for 2 workers and 4 workers scenarios (specific log files)
log_files_1_worker = ["log_node1.log"]
log_files_2_workers = ["log_node1.log", "log_node2.log"]
log_files_4_workers = [
    "log_node1.log",
    "log_node2.log",
    "log_node3.log",
    "log_node4.log",
]
log_files_6_workers = [
    "log_node1.log",
    "log_node2.log",
    "log_node3.log",
    "log_node4.log",
    "log_node5.log",
    "log_node6.log",
]

# Compute totals for 2 workers
processed_1, overdue_1, expired_1 = compute_totals(dir_one_worker, log_files_1_worker)

# Compute totals for 2 workers
processed_2, overdue_2, expired_2 = compute_totals(dir_two_workers, log_files_2_workers)

# Compute totals for 4 workers
processed_4, overdue_4, expired_4 = compute_totals(
    dir_four_workers, log_files_4_workers
)
# Compute totals for 2 workers
processed_6, overdue_6, expired_6 = compute_totals(dir_six_workers, log_files_6_workers)

# Data for plotting
labels = ["1 Worker", "2 Workers", "4 Workers", "6 Workers"]
processed_keys = [processed_1, processed_2, processed_4, processed_6]
overdue_keys = [overdue_1, overdue_2, overdue_4, overdue_6]
expired_keys = [expired_1, expired_2, expired_4, expired_6]

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
ax.set_xlabel("Number of Workers", fontsize=12)
ax.set_ylabel("Number of Keys", fontsize=12)
ax.set_title(
    "Comparison of Processed, Overdue, and Expired Keys for 1, 2, 4 and 6 Workers",
    fontsize=14,
)
ax.set_xticks(x)
ax.set_xticklabels(labels)

# Add a legend
ax.legend()

# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/Scenario7 - Scalability/workers_comparison_scenario5.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

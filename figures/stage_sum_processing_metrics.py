import os
import numpy as np
import matplotlib.pyplot as plt
import sys

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file


# Function to compute totals for overdue keys from specific log files
def compute_overdue_totals(log_files_dir, selected_logs):
    total_overdue = 0

    # Filter only the selected log files
    for log_file in selected_logs:
        log_path = os.path.join(log_files_dir, log_file)
        if os.path.exists(log_path):
            _, _, _, _, overdue_keys, _ = parse_log_file(log_path)

            # Sum the overdue keys
            total_overdue += sum(overdue_keys)

    return total_overdue


# Directories for different worker configurations
dir_three_workers = "../experiments/topology2/Scenario1/3workers/log_topology2/"
dir_four_workers = "../experiments/topology2/Scenario1/4workers/log_topology2/"
dir_six_workers = "../experiments/topology2/Scenario1/6workers/log_topology2/"

# Log files for 3, 4, and 6 worker configurations
log_files_3_workers = ["log_node7.log", "log_node8.log", "log_node9.log"]
log_files_4_workers = [
    "log_node7.log",
    "log_node8.log",
    "log_node9.log",
    "log_node10.log",
]
log_files_6_workers = [
    "log_node7.log",
    "log_node8.log",
    "log_node9.log",
    "log_node10.log",
    "log_node11.log",
    "log_node12.log",
]

# Compute totals for overdue keys for different worker configurations
overdue_3 = compute_overdue_totals(dir_three_workers, log_files_3_workers)
overdue_4 = compute_overdue_totals(dir_four_workers, log_files_4_workers)
overdue_6 = compute_overdue_totals(dir_six_workers, log_files_6_workers)

# Data for plotting
labels = ["3 Workers", "4 Workers", "6 Workers"]
overdue_keys = [overdue_3, overdue_4, overdue_6]

# Plotting
x = np.arange(len(labels))  # the label locations
bar_width = 0.4  # width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bars for overdue keys only
bars = ax.bar(x, overdue_keys, bar_width, label="Overdue Keys", color="#2ca02c")

# Add labels and title
ax.set_xlabel("Number of Workers", fontsize=12)
ax.set_ylabel("Number of Overdue Keys", fontsize=12)
ax.set_title(
    "Comparison of Overdue Keys for 3, 4, and 6 Workers",
    fontsize=14,
)
ax.set_xticks(x)
ax.set_xticklabels(labels)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{int(height)}",
        ha="center",
        va="bottom",
        fontsize=12,
    )

# Display the plot
plt.tight_layout()
plt.savefig(
    "../experiments/topology2/Scenario1/worker_overdue_keys_comparison.png",
    format="png",
    dpi=300,
    bbox_inches="tight",
)

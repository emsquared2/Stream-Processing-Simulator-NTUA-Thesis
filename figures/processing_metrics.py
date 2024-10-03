import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Get the absolute path to the 'src' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.log_parser import parse_log_file

# Parse log file
steps, processed_keys, _, overdue_keys, expired_keys = parse_log_file(
    "../experiments/Scenario2 - Increasing Arrival Rate/log_20241002211526/log_node1.log"
)

# Use a more modern, clean style for the plot
plt.style.use("classic")

# Adjust overdue and expired keys to match the length of steps
overdue_keys_adjusted = overdue_keys + [0] * (len(steps) - len(overdue_keys))
expired_keys_adjusted = expired_keys + [0] * (len(steps) - len(expired_keys))

# Bar width and indices for stacking bars
bar_width = 0.7
index = np.arange(len(steps))

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Ensure white background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Plot stacked bars for processed, overdue, and expired keys
p1 = ax.bar(index, processed_keys, bar_width, label="Processed Keys", color="#1f77b4")
p2 = ax.bar(
    index,
    overdue_keys_adjusted,
    bar_width,
    bottom=processed_keys,
    label="Overdue Keys",
    color="#2ca02c",
)
p3 = ax.bar(
    index,
    expired_keys_adjusted,
    bar_width,
    bottom=np.array(processed_keys) + np.array(overdue_keys_adjusted),
    label="Expired Keys",
    color="#d62728",
)

# Add labels and title with more elegant fonts
ax.set_xlabel("Steps", fontsize=12)
ax.set_ylabel("Keys Count", fontsize=12)
ax.set_title("Processed, Overdue, and Expired Keys Across Steps", fontsize=14, pad=15)

# Set x-axis limits to start from 0
ax.set_xlim(left=0)

# Add a legend outside the plot
ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=10)

# Add grid for readability and set its transparency
# ax.grid(True, which="both", linestyle="--", linewidth=0.7, alpha=0.7)

# Rotate x-axis labels for better readability and adjust the font size
# plt.xticks(index, steps, rotation=45, ha="right", fontsize=10)

# Ensure tight layout to handle spacing issues
plt.tight_layout()

# Display the plot
plt.show()

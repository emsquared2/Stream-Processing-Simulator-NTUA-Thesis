import matplotlib.pyplot as plt
import numpy as np

# Data for processed, overdue, and expired keys (as provided)
steps_v2 = list(range(50))
processed_keys_v2 = [
    0,
    0,
    0,
    0,
    0,
    215,
    0,
    267,
    0,
    334,
    0,
    416,
    0,
    523,
    0,
    527,
    134,
    526,
    299,
    528,
    492,
    527,
    527,
    595,
    527,
    529,
    568,
    530,
    528,
    601,
    528,
    529,
    528,
    528,
    529,
    529,
    529,
    529,
    528,
    529,
    529,
    529,
    529,
    529,
    529,
    528,
    529,
    529,
    529,
    529,
]
overdue_keys_v2 = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    134,
    299,
    492,
    723,
    196,
    1135,
    608,
    1975,
    1407,
    3188,
    2660,
    4901,
    4373,
    7318,
    6790,
    10087,
    9558,
    12546,
    12017,
    15611,
    15083,
    19437,
    18908,
    24207,
    23678,
    30077,
    29549,
    37209,
    36681,
    45972,
    45443,
    56813,
]
expired_keys_v2 = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    475,
    0,
    1785,
    0,
    2418,
    0,
    3242,
    0,
    4243,
    0,
    5484,
    0,
    7068,
    0,
    9013,
    0,
    11356,
]


plt.style.use("classic")

# Adjust overdue and expired keys to match the length of steps (50 steps)
overdue_keys_v2_adjusted = overdue_keys_v2 + [0] * (
    len(steps_v2) - len(overdue_keys_v2)
)
expired_keys_v2_adjusted = expired_keys_v2 + [0] * (
    len(steps_v2) - len(expired_keys_v2)
)

# Bar width and indices for stacking bars
bar_width = 0.3
index = np.arange(len(steps_v2))

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Plot stacked bars for processed, overdue, and expired keys
p1 = ax.bar(
    index, processed_keys_v2, bar_width, label="Processed Keys", color="lightblue"
)
p2 = ax.bar(
    index,
    overdue_keys_v2_adjusted,
    bar_width,
    bottom=processed_keys_v2,
    label="Overdue Keys",
    color="lightgreen",
)
p3 = ax.bar(
    index,
    expired_keys_v2_adjusted,
    bar_width,
    bottom=np.array(processed_keys_v2) + np.array(overdue_keys_v2_adjusted),
    label="Expired Keys",
    color="lightcoral",
)

# Add labels and title
ax.set_xlabel("Steps")
ax.set_ylabel("Keys Count")
ax.set_title("Processed, Overdue, and Expired Keys Across Steps")

# Add legend
# ax.legend()

# Add grid for readability
# ax.grid(True, which="both", linestyle="--", linewidth=0.5)

# Rotate x-axis labels for better readability
plt.xticks(index, steps_v2, rotation=45)

# Adjust layout and show the plot
# plt.tight_layout()
plt.show()

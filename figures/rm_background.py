from PIL import Image
import numpy as np


def remove_white_background(image_path, output_path, threshold=200):
    # Open the image
    image = Image.open(image_path).convert("RGBA")

    # Convert image to numpy array
    data = np.array(image)

    # Extract the RGB components and alpha channel
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    # Create a mask for pixels that are "close to white"
    mask = (r > threshold) & (g > threshold) & (b > threshold)

    # Set those pixels to be fully transparent
    data[mask] = [0, 0, 0, 0]

    # Convert back to an image
    image_no_bg = Image.fromarray(data, mode="RGBA")

    # Save the output
    image_no_bg.save(output_path)


# Usage
# remove_white_background(
#     "../experiments/Scenario6 - Partition Strategies/Scenario1 - comparison/worker_load_comparison_top2_stage2.png",
#     "../experiments/Scenario6 - Partition Strategies/Scenario1 - comparison/worker_load_comparison_top2_stage2_no_background.png",
# )

remove_white_background(
    "../experiments/topology2/Scenario1/worker_load_comparison_max.png",
    "../experiments/topology2/Scenario1/worker_load_comparison_max_no_background.png",
)
import re


def parse_log_file(file_path):
    # Initialize dictionaries to store data for each step
    steps = set()
    processed_keys = {}
    cycles_per_step = {}
    load_percentages = {}
    overdue_keys = {}
    expired_keys = {}

    # Regular expression to match log entries
    log_pattern = re.compile(
        r"Step (?P<step>\d+) - Processed (?P<processed>\d+) keys using (?P<cycles>\d+) cycles - Node load (?P<load>\d+\.\d+)%"
        r"(?: - Overdue keys: (?P<overdue>\d+))?(?: - Expired keys: (?P<expired>\d+))?"
    )

    # Read the log file
    with open(file_path, "r") as log_file:
        for line in log_file:
            match = log_pattern.search(line)
            if match:
                step = int(match.group("step"))
                processed = int(match.group("processed"))
                cycles = int(match.group("cycles"))
                load = float(match.group("load"))
                overdue = int(match.group("overdue")) if match.group("overdue") else 0
                expired = int(match.group("expired")) if match.group("expired") else 0

                # Add step to the set
                steps.add(step)

                # For each step, sum the processed keys and keep the maximum of other values
                if step in processed_keys:
                    processed_keys[step] += processed  # Sum processed keys
                    cycles_per_step[step] += cycles  # Sum cycles
                    load_percentages[step] = max(
                        load_percentages[step], load
                    )  # Max of load
                    overdue_keys[step] = max(
                        overdue_keys[step], overdue
                    )  # Max of overdue keys
                    expired_keys[step] = max(
                        expired_keys[step], expired
                    )  # Max of expired keys
                else:
                    processed_keys[step] = processed
                    cycles_per_step[step] = cycles
                    load_percentages[step] = load
                    overdue_keys[step] = overdue
                    expired_keys[step] = expired

    # Convert dictionaries to lists sorted by step
    sorted_steps = sorted(steps)
    processed_list = [processed_keys[step] for step in sorted_steps]
    cycles_list = [cycles_per_step[step] for step in sorted_steps]
    load_list = [load_percentages[step] for step in sorted_steps]
    overdue_list = [overdue_keys[step] for step in sorted_steps]
    expired_list = [expired_keys[step] for step in sorted_steps]

    return (
        sorted_steps,
        processed_list,
        cycles_list,
        load_list,
        overdue_list,
        expired_list,
    )

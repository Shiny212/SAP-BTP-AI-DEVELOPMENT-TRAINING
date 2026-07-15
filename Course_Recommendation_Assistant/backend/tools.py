from langchain_core.tools import tool
import re


@tool
def calculate_total_learning_hours(durations: list[str]) -> int:
    """
    Calculate total learning hours from course durations.

    Example:
    ["6 hours", "10 hours", "12 hours"]

    Returns:
    28
    """

    total = 0

    for duration in durations:
        match = re.search(r"\d+", duration)

        if match:
            total += int(match.group())

    return total
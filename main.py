"""OpenBB Metrics."""

import os
import json
import datetime as datetime
from utilities.helpers import (
    get_discord_stats,
    get_github_stats,
    get_google_interest,
    get_google_queries,
    get_google_regions,
    get_headlines_stats,
    get_linkedin_stats,
    get_newsletter_subscribers,
    get_pipy_stats,
    get_reddit_stats,
    get_terminal_downloads,
    get_youtube_stats,
    get_youtube_videos,
)

# pylint: disable=broad-exception-caught


def get_metrics(functions: dict) -> dict:
    """Get metrics."""
    metrics_dict: dict = {}

    for (
        key_name,
        function,
    ) in functions.items():
        try:
            print("Running: " + function.__name__)
            result = function()
            metrics_dict[key_name] = result
        except Exception as e:
            print("Error: " + function.__name__ + " - " + str(e))
            metrics_dict[key_name] = {}

    return metrics_dict


def load_metrics(filepath: str) -> dict:
    """Load existing metrics from a file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    else:
        return {}


def save_metrics(data: dict, filepath: str) -> None:
    """Save metrics to a file."""
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def merge_metrics(existing_metrics: dict, new_results: dict) -> None:
    """Merge new results into existing metrics."""
    for category, data in new_results.items():
        if category not in existing_metrics:
            existing_metrics[category] = []
        existing_metrics[category].append(data)


if __name__ == "__main__":
    metrics_functions = {
        "newsletter": get_newsletter_subscribers,
        "terminal_downloads": get_terminal_downloads,
        "reddit": get_reddit_stats,
        "headlines": get_headlines_stats,
        "youtube_videos": get_youtube_videos,
        "linkedin": get_linkedin_stats,
        "discord": get_discord_stats,
        "github": get_github_stats,
        "youtube": get_youtube_stats,
        "google_regions": get_google_regions,
        "google_queries": get_google_queries,
        "google_interest": get_google_interest,
        "pipy_downloads": get_pipy_stats,
    }

    metrics_filename = "metrics.json"
    existing_data = load_metrics(metrics_filename)
    new_results = get_metrics(metrics_functions)
    merge_metrics(existing_data, new_results)
    save_metrics(existing_data, metrics_filename)

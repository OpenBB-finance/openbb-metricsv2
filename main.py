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
    get_instagram_stats,
    get_linkedin_stats,
    get_newsletter_subscribers,
    get_pipy_stats,
    get_reddit_stats,
    get_terminal_downloads,
    get_twitter_stats,
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


def load_metrics(filepath):
    """Load existing metrics from a file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    else:
        return {}


def save_metrics(data, filepath):
    """Save metrics to a file."""
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def merge_metrics(existing_metrics, new_results):
    """Merge new results into existing metrics."""
    for category, data in new_results.items():
        if category not in existing_metrics:
            existing_metrics[category] = []
        existing_metrics[category].append(data)


if __name__ == "__main__":
    metrics_filename = "metrics.json"
    metrics_functions = {
        "newsletter": get_newsletter_subscribers,
        "terminal_downloads": get_terminal_downloads,
        "twitter": get_twitter_stats,
        "reddit": get_reddit_stats,
        "headlines": get_headlines_stats,
        "youtube_videos": get_youtube_videos,
        "linkedin": get_linkedin_stats,
        "discord": get_discord_stats,
        "github": get_github_stats,
        "youtube": get_youtube_stats,
        "instagram": get_instagram_stats,
        "google_regions": get_google_regions,
        "google_queries": get_google_queries,
        "google_interest": get_google_interest,
        "pipy_downloads": get_pipy_stats,
    }

    # results = get_metrics(metrics_functions)

    # the all.json document is the one we wan't to update by adding the new data from the
    # results dictionary
    # the all.json has the same keys as the results dictionary and is a list of dictionaries
    # so we need to append the new data to the list
    metrics_filename = "metrics.json"

    # Load existing data
    existing_data = load_metrics(metrics_filename)

    # Get new metrics
    new_results = get_metrics(metrics_functions)

    # Merge new metrics into existing
    merge_metrics(existing_data, new_results)

    # Save updated metrics
    save_metrics(existing_data, metrics_filename)

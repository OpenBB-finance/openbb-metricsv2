"""OpenBB Metrics."""

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


if __name__ == "__main__":
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
        "pipy": get_pipy_stats,
    }
    results = get_metrics(metrics_functions)
    with open("metrics.json", "w") as f:
        f.write(str(results))

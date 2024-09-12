"""Helper functions for metrics."""

import logging
from datetime import datetime

import praw
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from pyyoutube import Api

from utilities.config import settings

# pylint: disable=broad-exception-caught, undefined-loop-variable

current_date = int(datetime.timestamp(datetime.now()))


def get_mentions(term: str) -> dict:
    """Get interest over time from google api [Source: google]."""
    try:
        pytrend = TrendReq(timeout=(10, 25))
        pytrend.build_payload(kw_list=[term])
        df = pytrend.interest_over_time()
        df = df.resample("D").sum()
        df = df.drop(columns=["isPartial"])
        df = df.reset_index()
        df["date"] = df["date"].apply(lambda x: int(datetime.timestamp(x)))
        df = df.rename(columns={"openbb": "value"})
        # drop rows with zero values?
        return df.to_dict("records")

    except Exception as e:
        if pytrend.google_rl:
            logging.error("Google returned an error: %s", pytrend.google_rl)
        else:
            logging.error("Error: %s", e)

        return {}


def get_regions(term: str) -> dict:
    """Get interest by region from google api [Source: google]."""
    try:
        pytrend = TrendReq(timeout=(10, 25))
        pytrend.build_payload(kw_list=[term])
        df_regions = pytrend.interest_by_region().sort_values([term], ascending=False)
        df_regions = df_regions.reset_index()
        df_regions = df_regions.rename(columns={"openbb": "value"})
        return df_regions.to_dict("records")

    except Exception as e:
        if pytrend.google_rl:
            logging.error("Google returned an error: %s", pytrend.google_rl)
        else:
            logging.error("Error: %s", e)

        return {}


def get_queries(term: str, limit: int = 10) -> dict:
    """Get related queries from google api [Source: google]."""
    try:
        pytrend = TrendReq(timeout=(10, 25))
        pytrend.build_payload(kw_list=[term])
        df = pytrend.related_queries()
        df = df[term]["top"].head(limit)
        df["value"] = df["value"].apply(lambda x: f"{str(x)}%")
        df = df.reset_index()
        return df.to_dict("records")

    except Exception as e:
        if pytrend.google_rl:
            logging.error("Google returned an error: %s", pytrend.google_rl)
        else:
            logging.error("Error: %s", e)

        return {}


def convert_to_timestamp(date_str: str) -> int:
    """Convert date string to timestamp."""
    return int(datetime.timestamp(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")))


def get_newsletter_subscribers(audience_id: str = "e8ecacb821") -> dict:
    """Get newsletter subscribers."""
    data = requests.get(
        f"https://{settings.MAILCHIMP_ZONE}.api.mailchimp.com/3.0/lists/{audience_id}/members",
        auth=("user", settings.MAILCHIMP_API_KEY),
        timeout=30,
    ).json()
    total_subscribers = data["total_items"]
    result = {"total_subscribers": total_subscribers, "updated_date": current_date}
    return result


def get_terminal_downloads() -> dict:
    """Get terminal download statistics."""
    data = requests.get(
        "https://api.github.com/repos/OpenBB-finance/OpenBB/releases/latest",
        timeout=30,
    ).json()
    version, macos, windows = data["tag_name"], 0, 0
    for installer in data["assets"]:
        # macOS terminal downloads
        if installer["name"].endswith(".dmg"):
            macos += installer["download_count"]

        # windows terminal downloads
        elif installer["name"].endswith(".exe"):
            windows = installer["download_count"]

    result = {
        "tag_name": version,
        "macos": macos,
        "windows": windows,
        "updated_date": current_date,
    }
    return result


# def twitter_bearer_oauth(r):
#     """Method required by bearer token authentication."""
#     r.headers["Authorization"] = f"Bearer {settings.TWITTER_BEARER_TOKEN}"
#     r.headers["User-Agent"] = "v2UserLookupPython"
#     return r


# def connect_to_twitter_endpoint(url: str) -> dict:
#     """Connect to Twitter endpoint."""
#     response = requests.get(url, auth=twitter_bearer_oauth, timeout=30)
#     if response.status_code != 200:
#         return {}
#     return response.json()


# def get_twitter_stats() -> dict:
#     """Get twitter statistics."""
#     url = "https://api.twitter.com/1.1/users/show.json?screen_name=openbb_finance"
#     data = connect_to_twitter_endpoint(url)
#     total_followers = data["followers_count"]

#     url = (
#         "https://api.twitter.com/2/users/1388522440536494081/tweets?tweet.fields=attachments,author_id,created_at,"
#         "public_metrics,source,referenced_tweets"
#     )
#     data = connect_to_twitter_endpoint(url)
#     likes, retweets = 0, 0
#     for i in data["data"]:
#         metrics = i["public_metrics"]
#         if i["created_at"] > str(datetime.utcnow() - timedelta(days=1)):
#             likes += metrics["like_count"]
#             retweets += metrics["retweet_count"]

#     url = "https://api.twitter.com/2/tweets/counts/recent?query=openbb&granularity=hour"
#     data = connect_to_twitter_endpoint(url)
#     mentions = 0
#     for i in data["data"][-24:]:
#         mentions += i["tweet_count"]

#     result = {
#         "total_followers": total_followers,
#         "likes": likes,
#         "retweets": retweets,
#         "mentions": mentions,
#         "updated_date": current_date,
#     }
#     return result


def get_reddit_stats() -> dict:
    """Get reddit statistics."""
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT,
    )
    subreddit = reddit.subreddit("openBB")
    followers = subreddit.subscribers
    result = {"total_followers": followers, "updated_date": current_date}
    return result


def get_google_interest() -> dict:
    """Get google interest."""
    data = get_mentions("openbb")
    result = {"value": data, "updated_date": current_date}
    return result


def get_google_regions():
    """Get google regions."""
    df_regions = get_regions("openbb")
    result = {"value": df_regions, "updated_date": current_date}
    return result


def get_google_queries():
    """Get google queries."""
    df_related = get_queries("openbb")
    result = {"value": df_related, "updated_date": current_date}
    return result


def get_headlines_stats() -> list:
    """Get news headlines statistics."""
    url = f"https://newsapi.org/v2/everything?q=openbb&apiKey={settings.NEWSAPI_TOKEN}"
    data = requests.get(url, timeout=30)
    results = []
    for i in data.json()["articles"]:
        published_date = convert_to_timestamp(i["publishedAt"])
        result = {
            "source": i["source"]["name"],
            "title": i["title"],
            "url": i["url"],
            "published_date": published_date,
        }
        results.append(result)
    return results


def get_youtube_videos() -> dict:
    """Get YouTube OpenBB mentions."""
    url = (
        f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=openbb&publishedAfter=2022-01-01T00%3A00"
        f"%3A00Z&order=date&key={settings.YOUTUBE_TOKEN}"
    )
    data = requests.get(url, timeout=30)
    for i in data.json()["items"]:
        published_date = convert_to_timestamp(i["snippet"]["publishTime"])

    result = {
        "channel": i["snippet"]["channelTitle"],
        "title": i["snippet"]["title"],
        "video_id": i["id"]["videoId"],
        "published_date": published_date,
    }

    return result


def get_linkedin_stats() -> dict:
    """Get Linkedin statistics."""
    url = "https://www.linkedin.com/pages-extensions/FollowCompany?id=76491268&counter=bottom"
    data = requests.get(url, timeout=30)
    soup = BeautifulSoup(data.content, "html.parser")
    follower_count = soup.select_one(".follower-count").text
    followers = int(follower_count.replace(",", ""))
    result = {"total_followers": followers, "updated_date": current_date}
    return result


def get_discord_stats() -> dict:
    """Get Discord statistics."""
    header = {
        "authorization": f"Bot {settings.DISCORD_TOKEN}",
        "Content-Type": "application/json",
    }
    url = "https://discord.com/api/v7/guilds/831165782750789672?with_counts=true"
    data = requests.get(url, headers=header, timeout=30).json()
    total_followers = data["approximate_member_count"]
    active_followers = data["approximate_presence_count"]
    result = {
        "total_members": total_followers,
        "active_members": active_followers,
        "updated_date": current_date,
    }
    return result


def add_page_number(current_url: str) -> str:
    """Add page number to the current URL."""
    current_url, current_page_num = current_url.rsplit("=", 1)
    new_url = current_url + "=" + str(int(current_page_num) + 1)
    return new_url


def get_github_stats() -> dict:
    """Get Github statistics."""
    url = "https://api.github.com/repos/OpenBB-finance/OpenBB/contributors?per_page=100&anon=false&page=1"
    contributors = 0
    data = requests.get(url, timeout=30).json()
    contributors += len(data)
    while len(data) == 100:
        url = add_page_number(url)
        data = requests.get(url, timeout=30).json()
        contributors += len(data)

    url = "https://api.github.com/repos/OpenBB-finance/OpenBB"
    data = requests.get(url, timeout=30).json()
    stars = data["stargazers_count"]
    forks = data["forks_count"]
    issues = data["open_issues_count"]

    url = "https://api.github.com/search/issues?q=repo:OpenBB-finance/OpenBB%20is:issue%20is:closed"
    data = requests.get(url, timeout=30).json()
    closed_issues = data["total_count"]

    url = "https://api.github.com/search/issues?q=repo:OpenBB-finance/OpenBB%20is:pr%20is:open"
    data = requests.get(url, timeout=30).json()
    open_pr = data["total_count"]

    url = "https://api.github.com/search/issues?q=repo:OpenBB-finance/OpenBB%20is:pr%20is:closed"
    data = requests.get(url, timeout=30).json()
    closed_pr = data["total_count"]

    result = {
        "contributors": contributors,
        "stars": stars,
        "forks": forks,
        "open_pr": open_pr,
        "closed_pr": closed_pr,
        "issues": issues,
        "closed_issues": closed_issues,
        "updated_date": current_date,
    }
    return result


def get_youtube_stats() -> dict:
    """Get Youtube statistics."""
    api = Api(api_key=settings.YOUTUBE_TOKEN)

    # Get information from OpenBB channel
    openbb_account = api.get_channel_info(channel_id="UCaeFEx-W16IuxRsHlM1ywBQ")

    subscribers = openbb_account.items[0].statistics.subscriberCount
    total_views = openbb_account.items[0].statistics.viewCount

    result = {
        "subscribers": subscribers,
        "total_views": total_views,
        "updated_date": current_date,
    }
    return result


# def get_instagram_stats() -> dict:
#     """Get Instagram statistics."""
#     insta_loader = Instaloader()
#     insta_loader.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
#     total_followers = Profile.from_username(
#         insta_loader.context, "openbb.finance"
#     ).followers

#     result = {"total_followers": total_followers, "updated_date": current_date}
#     return result


def get_pipy_stats() -> dict:
    """Get PiPy statistics."""
    url = "https://pypistats.org/api/packages/openbb/recent?range=all"
    response = requests.get(url, timeout=30)
    last_day = response.json()["data"]["last_day"]

    result = {"downloads_last_day": last_day, "updated_date": current_date}
    return result

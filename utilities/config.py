"""Configuration file."""

import os

import dotenv


class Settings:
    """Settings class."""

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_URL: str
    POSTGRES_DB: str
    # TWITTER_BEARER_TOKEN: str
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USER_AGENT: str
    NEWSAPI_TOKEN: str
    YOUTUBE_TOKEN: str
    DISCORD_TOKEN: str
    # INSTAGRAM_USERNAME: str
    # INSTAGRAM_PASSWORD: str
    YOUTUBE_TOKEN: str
    MAILCHIMP_API_KEY: str
    MAILCHIMP_ZONE: str


settings = Settings()
dotenv.load_dotenv()
settings.POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
settings.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
settings.POSTGRES_URL = os.getenv("POSTGRES_URL")
settings.POSTGRES_DB = os.getenv("POSTGRES_DB")
settings.REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
settings.REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
settings.REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
settings.NEWSAPI_TOKEN = os.getenv("NEWSAPI_TOKEN")
settings.YOUTUBE_TOKEN = os.getenv("YOUTUBE_TOKEN")
settings.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
settings.YOUTUBE_TOKEN = os.getenv("YOUTUBE_TOKEN")
settings.MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")
settings.MAILCHIMP_ZONE = os.getenv("MAILCHIMP_ZONE")

# These ones below are not our focus at this moment.
# settings.TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
# settings.INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
# settings.INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

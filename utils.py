import os
from dotenv import load_dotenv
import time
from datetime import datetime as dt
import math

load_dotenv()

# Converts the env variable to a string, integer, or boolean based on contents


def env(key: str) -> str or int or bool:

    env_str = os.getenv(key)

    # Boolean Values
    if (env_str.lower() == "true"):
        return True
    if (env_str.lower() == "false"):
        return False

    # Integer Values
    try:
        env_int = int(env_str)
        return env_int

    # String Values
    except ValueError:
        return env_str


def format_time(post_secs: int) -> str:
    date = dt.fromtimestamp(post_secs)

    now_secs = math.floor(time.time())

    secs_passed = now_secs - post_secs
    if (secs_passed < 10):
        return "Just now"

    if (secs_passed < 60):
        return f"{plural_time('second', secs_passed)} ago"

    mins_passed = math.floor(secs_passed / 60)
    if (mins_passed < 60):
        return f"{plural_time('minute', mins_passed)} ago"

    hours_passed = math.floor(mins_passed / 60)
    if (hours_passed < 24):
        return f"{plural_time('hour', hours_passed)} ago"

    days_passed = math.floor(hours_passed / 24)
    if (days_passed < 7):
        return f"{plural_time('day', days_passed)} ago"

    weeks_passed = math.floor(days_passed / 7)
    if (weeks_passed < 5):
        return f"{plural_time('week', weeks_passed)} ago"

    formatted_date = date.strftime("%B %d, %Y")

    return formatted_date


def plural_time(unit, value):
    if value == 1:
        return f"{value} {unit}"

    return f"{value} {unit}s"

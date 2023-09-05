from utils import format_time, env
import time
import math

def test_env():
    print(env("SQL_HOST")) # IP Address (should be string)
    print(type(env("SQL_HOST")))

    print(env("SQL_PORT")) # Port (should be integer)
    print(type(env("SQL_PORT")))

    print(env("SSH_TUNNELING")) # Do tunneling (should be boolean)
    print(type(env("SSH_TUNNELING")))

def test_time():
    NOW = math.floor(time.time())

    print(format_time(NOW - 30))
    print(format_time(NOW - 300))
    print(format_time(NOW - 3600))
    print(format_time(NOW - (3600 * 2)))
    print(format_time(NOW - (3600 * 24)))
    print(format_time(NOW - (3600 * 24) * 3))
    print(format_time(NOW - (3600 * 24) * 8))
    print(format_time(NOW - (3600 * 24) * 17))
    print(format_time(NOW - (3600 * 24) * 200))




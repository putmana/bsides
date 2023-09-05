from utils import env

def test_utils():
    print(env("SQL_HOST")) # IP Address (should be string)
    print(type(env("SQL_HOST")))

    print(env("SQL_PORT")) # Port (should be integer)
    print(type(env("SQL_PORT")))

    print(env("SSH_TUNNELING")) # Do tunneling (should be boolean)
    print(type(env("SSH_TUNNELING")))
import os
from dotenv import load_dotenv

load_dotenv()

# Converts the env variable to a string, integer, or boolean based on contents
def env(key: str) -> str or int or bool:
    
    env_str = os.getenv(key)

    # Boolean Values
    if (env_str.lower() == "true"): return True
    if (env_str.lower() == "false"): return False

    # Integer Values
    try:
        env_int = int(env_str)
        return env_int
    
    # String Values
    except ValueError:
        return env_str


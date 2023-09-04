import os
from dotenv import load_dotenv

load_dotenv()

sqlconfig = {
    'user': os.getenv('SSH_USER'),
    'password': os.getenv('SSH_PASSWORD'),
    'host': os.getenv('SSH_HOST'),
    'port': os.getenv('SSH_PORT'),
    'database': os.getenv('SSH_DATABASE'),
    'use_pure': True
}
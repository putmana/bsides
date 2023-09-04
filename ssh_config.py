import os
from dotenv import load_dotenv

load_dotenv()

sshconfig = {
    'ssh_username': os.getenv('SSH_USER'),
    'ssh_pkey': os.getenv('SSH_PRIVATE_KEY_PATH'),
    'remote_bind_address': (os.getenv('SSH_REMOTE_ADDRESS'), os.getenv('SSH_REMOTE_PORT')),
    'local_bind_address': (os.getenv('SSH_LOCAL_ADDRESS'), os.getenv('SSH_LOCAL_PORT'))
}
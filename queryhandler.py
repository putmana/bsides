# SSH Tunneling Configuration
from sshtunnel import SSHTunnelForwarder

from DBcm import UseDatabase

# Enviromnemt Variables
import os
from dotenv import load_dotenv

load_dotenv()

def run_query(query, args):
    
    # Prepare a function to open the database and run the query
    def execute_query(query, args):
        with UseDatabase({
            'user': os.getenv('SQL_USER'),
            'password': os.getenv('SQL_PASSWORD'),
            'host': os.getenv('SQL_HOST'),
            'port': int(os.getenv('SQL_PORT')),
            'database': os.getenv('SQL_DATABASE'),
            'use_pure': True  
        }) as cursor:
            # Run the query
            print(args)
            cursor.execute(query, args)

            return cursor.fetchall()


    # Tunnel query through SSH if enabled
    if bool(os.getenv("SSH_TUNNELING")):
        print("SSH TUNNELING ENABLED")

        with SSHTunnelForwarder(**{
            'ssh_address_or_host': (
                os.getenv("SSH_HOST"), 
                int(os.getenv("SSH_PORT"))
            ),
            'ssh_username': os.getenv('SSH_USER'),
            'ssh_pkey': os.getenv('SSH_PRIVATE_KEY_PATH'),
            'remote_bind_address': (os.getenv('SSH_REMOTE_BIND_ADDRESS'), int(os.getenv('SSH_REMOTE_BIND_PORT'))),
            'local_bind_address': (os.getenv('SSH_LOCAL_BIND_ADDRESS'), int(os.getenv('SSH_LOCAL_BIND_PORT')))
        }):
            return execute_query(query, args)
    else:
        print("SSH TUNNELING DISABLED")

        return execute_query(query, args)
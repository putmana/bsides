# SSH Tunneling Configuration
from sshtunnel import SSHTunnelForwarder

from DBcm import UseDatabase

from utils import env

def run_query(query, args):
    
    # Prepare a function to open the database and run the query
    def execute_query(query, args):
        with UseDatabase({
            'user': env('SQL_USER'),
            'password': env('SQL_PASSWORD'),
            'host': env('SQL_HOST'),
            'port': env('SQL_PORT'),
            'database': env('SQL_DATABASE'),
            'use_pure': True  
        }) as cursor:
            # Run the query
            print(args)
            cursor.execute(query, args)

            return cursor.fetchall()


    # Tunnel query through SSH if enabled
    if env("SSH_TUNNELING"):
        print("SSH TUNNELING ENABLED")

        with SSHTunnelForwarder(**{
            'ssh_address_or_host': (
                env("SSH_HOST"), 
                env("SSH_PORT")
            ),
            'ssh_username': env('SSH_USER'),
            'ssh_pkey': env('SSH_PRIVATE_KEY_PATH'),
            'remote_bind_address': (env('SSH_REMOTE_BIND_ADDRESS'), env('SSH_REMOTE_BIND_PORT')),
            'local_bind_address': (env('SSH_LOCAL_BIND_ADDRESS'), env('SSH_LOCAL_BIND_PORT'))
        }):
            return execute_query(query, args)
    else:
        print("SSH TUNNELING DISABLED")

        return execute_query(query, args)
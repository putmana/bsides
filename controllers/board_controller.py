from queryhandler import run_query

def fetch_one(board_name):
    query = """
        SELECT
        b.id,
        b.name

        FROM 
        boards as b

        WHERE
        b.name = '%s'
    """ % board_name
    
    results = run_query(query)

    # Return None if the board does not exist
    if len(results) == 0:
        return False
    
    return {
        'id': results[0][0],
        'name': results[0][1]
    }

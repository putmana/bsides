from queryhandler import run_query

def fetch_by_name(board_name):
    query = """
        SELECT
        b.id,
        b.name

        FROM 
        boards as b

        WHERE
        b.name = %s
    """
    
    results = run_query(query, [board_name])

    # Return None if the board does not exist
    if len(results) == 0:
        return False
    
    return {
        'id': results[0][0],
        'name': results[0][1]
    }

from django.conf import settings
from django.db import connection
import jwt


def get_user_id(request):
    payload = jwt.decode(request.headers.get("Authorization"), settings.SECRET_KEY, algorithms=['HS256'])
    return payload.get('user_id')

def execute(sql):
    cursor = connection.cursor()
    return cursor.execute(sql)

def run_query(sql_query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params or [])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def query_to_json(sql_query, params=None):
    """
    Executes an SQL query and returns the results in JSON format.
    
    Args:
        connection_details (dict): Database connection parameters.
        sql_query (str): SQL query to execute.
        params (tuple): Optional parameters for SQL query to prevent SQL injection.

    Returns:
        str: JSON string containing the query results.
    """
    # Connect to the database
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in data]
           
            return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}
    finally:
        connection.close()
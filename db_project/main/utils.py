import psycopg2
from psycopg2 import Error
from django.conf import settings

connection = psycopg2.connect(**settings.PSYCOPG2_CONN)

cursor = connection.cursor()

def run_query(sql_query):
    cursor.execute(sql_query)
    return cursor.fetchall()

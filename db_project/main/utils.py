import psycopg2
from psycopg2 import Error
from django.conf.settings import DATABASES

connection = psycopg2.connect(**DATABASES["default"])

cursor = connection.cursor()

def query(sql_query):
    cursor.execute(sql_query)
    return cursor.fetchall()
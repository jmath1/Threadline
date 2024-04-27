import psycopg2
from psycopg2 import Error
from django.conf import settings

from main.models import Block

connection = psycopg2.connect(**settings.PSYCOPG2_CONN)

cursor = connection.cursor()

def run_query(sql_query):
    cursor.execute(sql_query)
    return cursor.fetchall()

def confirm_location(block_id):
    if Block.objects.get_member_count(block_id) <= 3:
        return True
    return False
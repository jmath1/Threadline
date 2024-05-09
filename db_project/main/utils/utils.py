import os
import re
from functools import wraps

from psycopg2 import sql
from django.conf import settings
from django.db import connection


def execute(sql):
    cursor = connection.cursor()
    return cursor.execute(sql)

def run_query(sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()

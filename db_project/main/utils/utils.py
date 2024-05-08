import os
import re
from functools import wraps

import psycopg2
from django.conf import settings
from django.db import connection


def execute(sql):
    cursor = connection.cursor()
    return cursor.execute(sql)

def run_query(sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()

def sanitize(view_func):
    @wraps(view_func)
    def wrapper(view, request, **kwargs):
        # Sanitize input data
        if isinstance(request.data, dict):
            data = {key: re.sub(r'([^a-zA-Z0-9\s])', r'\\\1', value) for key, value in request.data.items()}
        elif isinstance(request.data, list):
            data = [re.sub(r'([^a-zA-Z0-9\s])', r'\\\1', input_data) for input_data in request.data]
        elif isinstance(request.data, str):
            data = re.sub(r'([^a-zA-Z0-9\s])', r'\\\1', request.data)

        request.san_data = data
        return view_func(view, request, **kwargs)
    return wrapper

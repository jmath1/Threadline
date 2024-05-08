

from typing import Any

from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner
from django.test.utils import setup_databases

from main.utils.utils import execute


class TestRunner(DiscoverRunner):

    # def setup_databases(self, **kwargs):
    #     with open('../sql/table_creation.sql', 'r') as file:
    #         table_creation = file.read()
    #         execute(table_creation)
    #     return setup_databases(self.verbosity, self.interactive, **kwargs)
    
    # def teardown_databases(self, old_config, **kwargs):
        
    #     query =  """
    #         DROP EXTENSION IF EXISTS postgis CASCADE;
	#         DO $$ DECLARE
	# 	        table_rec RECORD;
    #         BEGIN
    #             -- Iterate through all user-defined tables in the current schema
    #             FOR table_rec IN 
    #                 SELECT table_name 
    #                 FROM information_schema.tables 
    #                 WHERE table_schema = 'public'
    #             LOOP
    #                 -- Generate and execute DROP TABLE statement
    #                 EXECUTE format('DROP TABLE IF EXISTS %I CASCADE;', table_rec.table_name);
    #             END LOOP;
    #         END $$; 
    #     """
    #     execute(query)
    #     return super(TestRunner, self).teardown_databases(old_config, **kwargs)
    
    pass
    
from django.core.management import call_command
from django.test.runner import DiscoverRunner


class GISDataTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        # Force migrations during test setup
        setup = super().setup_databases(**kwargs)
        call_command("load_gis_data")
        return setup
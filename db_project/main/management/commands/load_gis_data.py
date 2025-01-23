import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from main.models import Hood

class Command(BaseCommand):
    help = "Load Philadelphia GIS data into the database"

    def handle(self, *args, **kwargs):
        with open("./main/hoods.geojson") as f:
            hoods_data = json.load(f)
            for feature in hoods_data["features"]:
                geom = GEOSGeometry(json.dumps(feature["geometry"]), srid=4326)
                name = feature["properties"].get("LISTNAME", "Unnamed Hood")
                
                hood, created = Hood.objects.get_or_create(
                    name=name,
                    defaults={"polygon": geom},
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created neighborhood: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Neighborhood already exists: {name}"))

        self.stdout.write(self.style.SUCCESS("Finished loading neighborhoods"))
        

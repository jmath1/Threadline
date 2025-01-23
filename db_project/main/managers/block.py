from django.db import models

class BlockManager(models.Manager):

    def get_from_coords(self, coords):
        return self.objects.filter(coords__distance_lte=(coords, models.F('radius')))

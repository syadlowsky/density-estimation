from django.contrib.gis.db import models

class Tower(models.Model):
    """
    geom is voronoi parition, location is center (location of tower)
    """
    category = models.CharField(null=True, blank=True, max_length=100)
    geom = models.PolygonField(srid=4326, null=True, blank=True)
    geom_dist = models.PolygonField(srid=900913, null=True, blank=True)
    location = models.PointField(srid=4326)
    location_dist = models.PointField(srid=900913, null=True, blank=True)
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return "Category: %s, Center: %s" % (self.category, repr(self.location.coords))


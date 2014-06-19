from django.contrib.gis.db import models

class Node(models.Model):
    """
    ID: node id
    NETWORK_ID: network id 
    GEOMSTR: geometry (lat, lng)
    NODE_TYPE: type
    NODE_NAME: name
    """
    geom = models.PointField(srid=4326)
    geom_dist = models.PointField(srid=900913, null=True, blank=True)
    name = models.TextField()
    node_type = models.TextField()

    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return "%s (%s) Type: %s" % (self.name, self.id, self.node_type)

class Link(models.Model):
    """
    ID: Link id
    NETWORK_ID: network id 
    BEG_NODE_ID: beginning node id
    END_NODE_ID:  end node id
    GEOMSTR: geometry points (lat, lng)
    LENGTH: (length in meters)
    LINK_NAME: link name
    LANE_COUNT: number of lanes
    LINK_TYPE: road type
    SPEED_LIMIT: speed limit
    """
    id = models.BigIntegerField(primary_key=True)
    geom = models.LineStringField(srid=4326)
    geom_dist = models.LineStringField(srid=900913, null=True, blank=True)
    beg_node_id = models.BigIntegerField()
    end_node_id = models.BigIntegerField()
    length = models.FloatField()
    name = models.TextField()
    lane_count = models.IntegerField(null=True, blank=True)
    link_type = models.TextField(null=True, blank=True)
    speed_limit = models.IntegerField(null=True, blank=True)

    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return "%s (%s) Type: %s, Length: %7.1f, Lanes: %g, Speed Limit: %g" % (self.name, self.id, self.link_type, self.length, self.lane_count, self.speed_limit or 0.)

class Trajectory(models.Model):
    oid = models.IntegerField(db_index=True)
    ent = models.IntegerField()
    link_id = models.IntegerField() #models.ForeignKey('Link')
    lane_index = models.IntegerField()
    location = models.PointField(srid=4326)
    location_dist = models.PointField(srid=900913)
    step_time = models.TimeField(db_index=True)

    objects = models.GeoManager()

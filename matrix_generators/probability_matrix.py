# TODO: import Tower, Link objects

def area_in_region(tower_id, link_id):
    tower = Tower.objects.get(id=tower_id)
    link = Link.objects.get(id=link_id)
    query = """
    SELECT l.lane_count, ST_Length(ST_Intersection(l.geom_dist, t.geom_dist)), l.link_type
    FROM orm_tower t, orm_link l
    WHERE t.id = %s AND l.id = %s
    """

def links_in_region(tower_id):
    tower = Tower.objects.get(id=tower_id)
    query = """
    SELECT el.index, l.lane_count, ST_Length(ST_Intersection(l.geom_dist, t.geom_dist)), l.link_type
    FROM orm_tower t, orm_link l, orm_experimentlink el
    WHERE t.id = %s AND ST_Intersects(l.geom, t.geom)
    AND el.link_id = l.id
    """
    # (matrix_index, lane_count, length_in_region, type)

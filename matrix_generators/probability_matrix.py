import os, sys
import numpy as np
from django.db import connection
import logging

from sklearn.preprocessing import normalize

def get_probabilities():
    c = connection.cursor()

    logging.info("Getting weighted areas from database...")
    query = """
    SELECT array(
      (SELECT (CASE WHEN l.link_type='1' THEN 1.0 ELSE 0.5 END)*l.lane_count*ST_Length(ST_Intersection(l.geom_dist, t.geom_dist)) AS length
       FROM cell_data_tower t
       ORDER BY t.id)
    ) AS cell_areas
    FROM microsim_link l
    ORDER BY l.id
    """
    c.execute(query)
    rows = [[x or 0.0 for x in r[0]] for r in c]

    logging.info("Converting areas into a probability matrix...")
    tower_to_link_matrix = np.array(rows) # column is a tower
    return normalize(tower_to_link_matrix, 'l1', axis=0)

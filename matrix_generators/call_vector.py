import os, sys
import numpy as np
from django.db import connection

def get_counts_in_tower(start_time, interval):
    c = connection.cursor()

    query = """
    SELECT COUNT(traj.oid)
    FROM cell_data_tower tower, mivehdetailedtrajectory traj
    WHERE traj.timesta >= %s AND traj.timesta <= %s
    AND ST_Contains(tower.geom, traj.location)
    GROUP BY tower.id
    ORDER BY tower.id
    """

    c.execute(query, (start_time, start_time+interval))
    tower_counts = [r[0] for r in c]
    
    print tower_counts

import os, sys
import numpy as np
from django.db import connection

def get_counts_in_tower(start_time, interval):
    c = connection.cursor()

    query = """
    SELECT COUNT(DISTINCT traj.timesta)
    FROM mivehdetailedtrajectory traj
    WHERE traj.timesta >= %s AND traj.timesta <= %s
    """
    c.execute(query, (start_time, start_time+interval))
    intervals = float(c.fetchone()[0])

    query = """
    SELECT COUNT(traj.oid)
    FROM cell_data_tower tower
    LEFT OUTER JOIN mivehdetailedtrajectory traj
    ON (ST_Contains(tower.geom, traj.location))
    WHERE traj.timesta >= %s AND traj.timesta <= %s
    GROUP BY tower.id
    ORDER BY tower.id
    """
    c.execute(query, (start_time, start_time+interval))

    tower_counts = [r[0]/intervals for r in c]
    
    return np.array([np.random.poisson(interval*count/396.0) for count in tower_counts]) # off by a factor of 10 in denominator for efficiency

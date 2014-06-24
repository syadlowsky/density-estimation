import os, sys
import numpy as np
import logging
from django.db import connection

def get_counts_in_tower(start_time, interval, use_call_model=False):
    c = connection.cursor()

    logging.info("Counting time slices in interval given")
    query = """
    SELECT COUNT(DISTINCT traj.timesta)
    FROM mivehdetailedtrajectory traj
    WHERE traj.timesta >= %s AND traj.timesta <= %s
    """
    c.execute(query, (start_time, start_time+interval))
    intervals = float(c.fetchone()[0])

    logging.info("Getting cars in each cell tower for interval")
    query = """
    SELECT (SELECT COUNT(traj.oid)
    FROM mivehdetailedtrajectory traj
    WHERE ST_Contains(tower.geom, traj.location)
    AND traj.timesta >= %s AND traj.timesta <= %s)
    FROM cell_data_tower tower
    ORDER BY tower.id
    """
    c.execute(query, (start_time, start_time+interval))

    tower_counts = [r[0]/intervals for r in c]
    
    logging.info("Computing estimated number of calls made for that number of cars in a cell tower.")
    if use_call_model:
        return np.array([np.random.poisson(interval*count/396.0) for count in tower_counts]) # off by a factor of 10 in denominator for efficiency
    else:
        return np.array(tower_counts)

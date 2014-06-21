from django.db import connection
import pprint
import networkx as nx
import numpy as np
import os, sys

def density_vector(start_time, interval):
    c = connection.cursor()

    query = """
    SELECT COUNT(DISTINCT traj.timesta)
    FROM mivehdetailedtrajectory traj
    WHERE traj.timesta >= %s AND traj.timesta <= %s
    """
    c.execute(query, (start_time, start_time+interval))
    intervals = float(c.fetchone()[0])

    query = """
    SELECT id, ROW_NUMBER() OVER (ORDER BY id)
    FROM microsim_link
    """
    c.execute(query)
    row_numbers = {x[0]: x[1] for x in c}

    query = """
    SELECT traj.sectionId, COUNT(traj.oid)
    FROM mivehdetailedtrajectory traj
    WHERE traj.timesta >= 26589.2 AND traj.timesta <= 26589.2+300
    GROUP BY traj.sectionId                                           
    ORDER BY traj.sectionid;
    """
    c.execute(query, (start_time, start_time+interval))

    link_counts = np.zeros(len(row_numbers.keys()))
    for r in c:
        link_counts[row_numbers[r[0]]] = r[1]
    return link_counts

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
    SELECT 
      (SELECT COUNT(traj.oid)
       FROM mivehdetailedtrajectory traj
       WHERE traj.sectionId = l.id
       AND traj.timesta >= %s AND traj.timesta <= %s)
    FROM microsim_link l
    ORDER BY l.id
    """
    c.execute(query, (start_time, start_time+interval))

    link_counts = np.array([r[0]/intervals for r in c])

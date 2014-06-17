import os
import csv
import logging
import pickle, json
import datetime
from collections import defaultdict

import ipdb

import sqlite3
from django.db import transaction
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, LineString

from lib.console_tools import ConsoleProgress, QueryTools
import models
import solvers

logging.basicConfig(level=logging.DEBUG)

DATA_PATH = 'data'

link_mapping = {
    'id': 'ID',
    'beg_node_id': 'BEG_NODE_ID',
    'end_node_id': 'END_NODE_ID',
    'length': 'LENGTH',
    'name': 'LINK_NAME',
    'lane_count': 'LANE_COUNT',
    'link_type': 'LINK_TYPE',
    'speed_limit': 'SPEED_LIMIT',
}

def import_links(verbose=True):
    ac = transaction.get_autocommit()
    transaction.set_autocommit(False)
    for row in csv.DictReader(open("{0}/Links_I15.csv".format(DATA_PATH))):
        row = {k: v.strip() for k, v in row.iteritems() if v.strip()}
        params = {sensor_mapping_reverse[k]: v for k, v in row.iteritems() if sensor_mapping_reverse.has_key(k)}
        geomstr = row['GEOMSTR']
        point_string = row.split(",,") # I have no idea why there are two commas in the CSV
        params['geom'] = LineString((), srid=4326)
        params['geom_dist'] = Point(float(row['Longitude']), float(row['Latitude']), srid=4326)
        params['location_dist'].transform(900913)
        try:
            sensor = Sensor(**params)
            sensor.save()
        except:
            print params
            raise
    transaction.commit()
    transaction.set_autocommit(ac)

def import_trajectories():
    if QueryTools.query_yes_no("This will take a really long time. Are you sure?", "no"):
        logging.info("Connecting to sqlite3 database.")
        conn = sqlite3.connect(DATA_PATH+'/SANDAG_NETWORK_V8_25_11_2013_MPCRM_test_STEVEN.sqlite')
        conn.row_factory = sqlite3.Row
        ac = transaction.get_autocommit()
        transaction.set_autocommit(False)
        c = conn.cursor()
        logging.info("Counting trajectories.")
        c.execute('SELECT COUNT(*) FROM MIVEHDETAILEDTRAJECTORY;')
        for row in c:
            count = row[0]
        logging.info("Count complete. %s trajectory rows found."%repr(count))
        progress = ConsoleProgress(count, message="Importing SQLite3 into PostGIS")
        c.execute('SELECT * FROM MIVEHDETAILEDTRAJECTORY;')
        for row in c:
            s, ms = divmod(row['timeSta'], 1)
            ms = int(1000*ms)
            s = int(s)
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)
            step_time = datetime.time(h,m,s)

            location = Point(row['xCoord'], row['yCoord'], srid=3718)
            location_dist = location.transform(900913, clone=True)
            location.transform(4326)
            trajectory = models.Trajectory(oid=row['oid'], ent=row['ent'],
                    link_id=row['sectionId'], lane_index=row['laneIndex'],
                    location=location, location_dist=location_dist, step_time=step_time)
            trajectory.save()
            progress.increment_progress()
        transaction.commit()
        progress.finish()
        transaction.set_autocommit(ac)
        c.close()

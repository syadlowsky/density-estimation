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
from django.contrib.gis.geos import Point, LineString, GEOSGeometry

from django.db import connection

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

link_mapping_type = {
    'id': int,
    'beg_node_id': int,
    'end_node_id': int,
    'length': float,
    'name': str,
    'lane_count': int,
    'link_type': str,
    'speed_limit': float,
}

def import_links(verbose=True):
    link_mapping_reverse = {v:k for k, v in link_mapping.iteritems()}
    ac = transaction.get_autocommit()
    transaction.set_autocommit(False)
    for idx, row in enumerate(csv.DictReader(open("{0}/Links_I15.csv".format(DATA_PATH)))):
        try:
            params = {k:v for k, v in row.iteritems() if (k and v)}
            params = {k: link_mapping_type[k](v) for k, v in params.iteritems() if k in link_mapping_type}
            print params
            geomstr = row['geom']
            params['geom'] = GEOSGeometry(geomstr)
            params['geom_dist'] = params['geom'].transform(900913, clone=True)
            link = models.Link(**params)
            link.save()
        except:
            print idx
            print params
            print row
            raise
    transaction.commit()
    transaction.set_autocommit(ac)

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

node_mapping = {
     'ID'        : 'id',
     'NODE_NAME' : 'name',
     'NODE_TYPE' : 'node_type',
}

node_mapping_type = {
    'id': int,
    'name': str,
    'node_type': str,
}

link_mapping = {
    'ID':         'id',
    'BEG_NODE_ID':'beg_node_id',
    'END_NODE_ID':'end_node_id',
    'LENGTH':     'length',
    'LINK_NAME':  'name',
    'LANE_COUNT': 'lane_count',
    'LINK_TYPE':  'link_type',
    'SPEED_LIMIT':'speed_limit',
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

def import_nodes(verbose=True):
    ac = transaction.get_autocommit()
    transaction.set_autocommit(False)
    for idx, row in enumerate(csv.DictReader(open("{0}/Nodes_I15.csv".format(DATA_PATH)))):
        try:
            params = {node_mapping[k]:v for k, v in row.iteritems() if (k and v and k in node_mapping)}
            params = {k: link_mapping_type[k](v) for k, v in params.iteritems() if k in link_mapping_type}
            geomstr = 'SRID=4326;POINT('+row['GEOMSTR']+')'
            params['geom'] = GEOSGeometry(geomstr)
            params['geom_dist'] = params['geom'].transform(900913, clone=True)
            node = models.Node(**params)
            node.save()
        except:
            logging.error("Error parsing on line %d: row is \"%s\" and params extracted are \"%s\"" % (idx+1, params, row))
            transaction.rollback()
            transaction.set_autocommit(ac)
            raise
    transaction.commit()
    transaction.set_autocommit(ac)

def import_links(verbose=True):
    ac = transaction.get_autocommit()
    transaction.set_autocommit(False)
    for idx, row in enumerate(csv.DictReader(open("{0}/Links_I15.csv".format(DATA_PATH)))):
        try:
            params = {k:v for k, v in row.iteritems() if (k and v)}
            params = {k: link_mapping_type[k](v) for k, v in params.iteritems() if k in link_mapping_type}
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

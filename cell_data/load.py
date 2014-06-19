import os
import csv
import logging
import pickle
import json
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos import Point, LineString
from collections import defaultdict
from django.db import transaction
from django.db import connection
import scipy.io as sio
import numpy as np
from models import Tower
from lib.console_progress import ConsoleProgress
from lib import google_lines
import models

logging.basicConfig(level=logging.DEBUG)

def import_cell_towers(verbose=True):
    towers = sio.loadmat("data/tower_locations.mat")
    towers = towers['towers']
    ac = transaction.get_autocommit()
    transaction.set_autocommit(False)
    for location in towers:
        pt = Point(tuple(location), srid=4326)
        wp = Tower(location=pt, location_dist=pt.transform(900913, clone=True), category="From tower_locations.mat")
        wp.save()
    transaction.commit()
    transaction.set_autocommit(ac)

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Link.end_node_id'
        db.alter_column(u'microsim_link', 'end_node_id', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Link.beg_node_id'
        db.alter_column(u'microsim_link', 'beg_node_id', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Link.id'
        db.alter_column(u'microsim_link', 'id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True))

    def backwards(self, orm):

        # Changing field 'Link.end_node_id'
        db.alter_column(u'microsim_link', 'end_node_id', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Link.beg_node_id'
        db.alter_column(u'microsim_link', 'beg_node_id', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Link.id'
        db.alter_column(u'microsim_link', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

    models = {
        u'microsim.link': {
            'Meta': {'object_name': 'Link'},
            'beg_node_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'end_node_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'geom_dist': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '900913', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'lane_count': ('django.db.models.fields.IntegerField', [], {}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'link_type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'speed_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'microsim.node': {
            'Meta': {'object_name': 'Node'},
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'geom_dist': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'node_type': ('django.db.models.fields.TextField', [], {})
        },
        u'microsim.trajectory': {
            'Meta': {'object_name': 'Trajectory'},
            'ent': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_index': ('django.db.models.fields.IntegerField', [], {}),
            'link_id': ('django.db.models.fields.IntegerField', [], {}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_dist': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913'}),
            'oid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'step_time': ('django.db.models.fields.TimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['microsim']
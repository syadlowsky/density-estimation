# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table(u'microsim_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('geom_dist', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('node_type', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'microsim', ['Node'])

        # Adding model 'Link'
        db.create_table(u'microsim_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
            ('geom_dist', self.gf('django.contrib.gis.db.models.fields.LineStringField')(srid=900913, null=True, blank=True)),
            ('beg_node_id', self.gf('django.db.models.fields.IntegerField')()),
            ('end_node_id', self.gf('django.db.models.fields.IntegerField')()),
            ('length', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('lane_count', self.gf('django.db.models.fields.IntegerField')()),
            ('link_type', self.gf('django.db.models.fields.TextField')()),
            ('speed_limit', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'microsim', ['Link'])

        # Adding model 'Trajectory'
        db.create_table(u'microsim_trajectory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oid', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('ent', self.gf('django.db.models.fields.IntegerField')()),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsim.Link'])),
            ('lane_index', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('location_dist', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913)),
            ('step_time', self.gf('django.db.models.fields.TimeField')(db_index=True)),
        ))
        db.send_create_signal(u'microsim', ['Trajectory'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table(u'microsim_node')

        # Deleting model 'Link'
        db.delete_table(u'microsim_link')

        # Deleting model 'Trajectory'
        db.delete_table(u'microsim_trajectory')


    models = {
        u'microsim.link': {
            'Meta': {'object_name': 'Link'},
            'beg_node_id': ('django.db.models.fields.IntegerField', [], {}),
            'end_node_id': ('django.db.models.fields.IntegerField', [], {}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'geom_dist': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '900913', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_count': ('django.db.models.fields.IntegerField', [], {}),
            'length': ('django.db.models.fields.FloatField', [], {}),
            'link_type': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'speed_limit': ('django.db.models.fields.IntegerField', [], {})
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
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsim.Link']"}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_dist': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913'}),
            'oid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'step_time': ('django.db.models.fields.TimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['microsim']
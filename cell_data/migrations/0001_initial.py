# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tower'
        db.create_table(u'cell_data_tower', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('geom_dist', self.gf('django.contrib.gis.db.models.fields.PolygonField')(srid=900913, null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('location_dist', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913, null=True, blank=True)),
        ))
        db.send_create_signal(u'cell_data', ['Tower'])


    def backwards(self, orm):
        # Deleting model 'Tower'
        db.delete_table(u'cell_data_tower')


    models = {
        u'cell_data.tower': {
            'Meta': {'object_name': 'Tower'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'geom_dist': ('django.contrib.gis.db.models.fields.PolygonField', [], {'srid': '900913', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_dist': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cell_data']
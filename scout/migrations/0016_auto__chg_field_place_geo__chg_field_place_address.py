# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Place.geo'
        db.alter_column(u'scout_place', 'geo', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True))

        # Changing field 'Place.address'
        db.alter_column(u'scout_place', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['scout.PostalAddress']))

    def backwards(self, orm):

        # Changing field 'Place.geo'
        db.alter_column(u'scout_place', 'geo', self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0.0 0.0)'))

        # Changing field 'Place.address'
        db.alter_column(u'scout_place', 'address_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['scout.PostalAddress']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bucket.bucket': {
            'Meta': {'object_name': 'Bucket'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buckets_created'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scout.datalayer': {
            'Meta': {'object_name': 'DataLayer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_mapping': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'json_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datalayers'", 'to': u"orm['scout.Map']"})
        },
        u'scout.map': {
            'Meta': {'object_name': 'Map'},
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'map'", 'to': u"orm['bucket.Bucket']"}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'geography': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maps_created'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'tilelayer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maps'", 'to': u"orm['scout.TileLayer']"}),
            'zoom': ('django.db.models.fields.IntegerField', [], {'default': '7'})
        },
        u'scout.marker': {
            'Meta': {'object_name': 'Marker'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'markers'", 'to': u"orm['scout.MarkerCategory']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datalayer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'markers'", 'to': u"orm['scout.DataLayer']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.contrib.gis.db.models.fields.PointField', [], {'geography': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_src': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'scout.markercategory': {
            'Meta': {'object_name': 'MarkerCategory'},
            'icon_color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'icon_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marker_categories'", 'to': u"orm['scout.Map']"}),
            'marker_color': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'scout.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'place'", 'null': 'True', 'to': u"orm['scout.PostalAddress']"}),
            'geo': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scout.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'address_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_office_box_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'scout.tilelayer': {
            'Meta': {'object_name': 'TileLayer'},
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_zoom': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'min_zoom': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url_template': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['scout']
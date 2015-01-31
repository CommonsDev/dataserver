# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Project.begin_date'
        db.alter_column(u'projects_project', 'begin_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Project.location'
        db.alter_column(u'projects_project', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scout.Place'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Project.begin_date'
        raise RuntimeError("Cannot reverse this migration. 'Project.begin_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Project.begin_date'
        db.alter_column(u'projects_project', 'begin_date', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Project.location'
        db.alter_column(u'projects_project', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scout.PostalAddress'], null=True))

    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scout.Place']", 'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectProgress']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'projects.projectprogress': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectProgress'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'progress_range': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectProgressRange']"})
        },
        u'projects.projectprogressrange': {
            'Meta': {'object_name': 'ProjectProgressRange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'scout.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'place'", 'to': u"orm['scout.PostalAddress']"}),
            'geo': ('django.contrib.gis.db.models.fields.PointField', [], {}),
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
        }
    }

    complete_apps = ['projects']
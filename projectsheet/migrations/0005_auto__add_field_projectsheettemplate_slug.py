# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ProjectSheetTemplate.slug'
        db.add_column(u'projectsheet_projectsheettemplate', 'slug',
                      self.gf('autoslug.fields.AutoSlugField')(default='test', unique=True, max_length=50, populate_from='name', unique_with=()),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ProjectSheetTemplate.slug'
        db.delete_column(u'projectsheet_projectsheettemplate', 'slug')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scout.PostalAddress']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'projectsheet.projectsheet': {
            'Meta': {'object_name': 'ProjectSheet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetTemplate']"})
        },
        u'projectsheet.projectsheetquestion': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ProjectSheetQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetTemplate']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projectsheet.projectsheetsuggesteditem': {
            'Meta': {'ordering': "('question__order',)", 'object_name': 'ProjectSheetSuggestedItem'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projectsheet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheet']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetQuestion']"})
        },
        u'projectsheet.projectsheettemplate': {
            'Meta': {'object_name': 'ProjectSheetTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortdesc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        u'scout.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'address_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'address_region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_office_box_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'street_address': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['projectsheet']
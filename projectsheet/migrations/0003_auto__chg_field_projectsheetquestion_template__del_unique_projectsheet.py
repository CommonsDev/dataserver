# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ProjectSheetQuestion', fields ['template']
        db.delete_unique(u'projectsheet_projectsheetquestion', ['template_id'])


        # Changing field 'ProjectSheetQuestion.template'
        db.alter_column(u'projectsheet_projectsheetquestion', 'template_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projectsheet.ProjectSheetTemplate']))

    def backwards(self, orm):

        # Changing field 'ProjectSheetQuestion.template'
        db.alter_column(u'projectsheet_projectsheetquestion', 'template_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projectsheet.ProjectSheetTemplate'], unique=True))
        # Adding unique constraint on 'ProjectSheetQuestion', fields ['template']
        db.create_unique(u'projectsheet_projectsheetquestion', ['template_id'])


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'title'", 'unique_with': '()'}),
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
            'Meta': {'object_name': 'ProjectSheetQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetTemplate']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projectsheet.projectsheetsuggesteditem': {
            'Meta': {'ordering': "('question__order',)", 'object_name': 'ProjectSheetSuggestedItem'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projectsheet': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projectsheet.ProjectSheet']", 'unique': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetQuestion']"})
        },
        u'projectsheet.projectsheettemplate': {
            'Meta': {'object_name': 'ProjectSheetTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortdesc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projectsheet']
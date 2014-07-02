# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectSheetTemplate'
        db.create_table(u'projectsheet_projectsheettemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortdesc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'projectsheet', ['ProjectSheetTemplate'])

        # Adding model 'ProjectSheetQuestion'
        db.create_table(u'projectsheet_projectsheetquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projects.Project'], unique=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'projectsheet', ['ProjectSheetQuestion'])

        # Adding model 'ProjectSheet'
        db.create_table(u'projectsheet_projectsheet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projects.Project'], unique=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projectsheet.ProjectSheetTemplate'])),
        ))
        db.send_create_signal(u'projectsheet', ['ProjectSheet'])

        # Adding model 'ProjectSheetSuggestedItem'
        db.create_table(u'projectsheet_projectsheetsuggesteditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('projectsheet', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['projectsheet.ProjectSheet'], unique=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projectsheet.ProjectSheetQuestion'])),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'projectsheet', ['ProjectSheetSuggestedItem'])


    def backwards(self, orm):
        # Deleting model 'ProjectSheetTemplate'
        db.delete_table(u'projectsheet_projectsheettemplate')

        # Deleting model 'ProjectSheetQuestion'
        db.delete_table(u'projectsheet_projectsheetquestion')

        # Deleting model 'ProjectSheet'
        db.delete_table(u'projectsheet_projectsheet')

        # Deleting model 'ProjectSheetSuggestedItem'
        db.delete_table(u'projectsheet_projectsheetsuggesteditem')


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
            'template': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
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
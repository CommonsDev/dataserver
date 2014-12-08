# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectProgressRange'
        db.create_table(u'projects_projectprogressrange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='name', unique_with=())),
        ))
        db.send_create_signal(u'projects', ['ProjectProgressRange'])

        # Adding model 'ProjectProgress'
        db.create_table(u'projects_projectprogress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('progress_range', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectProgressRange'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'projects', ['ProjectProgress'])

        # Adding field 'Project.progress'
        db.add_column(u'projects_project', 'progress',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectProgress'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ProjectProgressRange'
        db.delete_table(u'projects_projectprogressrange')

        # Deleting model 'ProjectProgress'
        db.delete_table(u'projects_projectprogress')

        # Deleting field 'Project.progress'
        db.delete_column(u'projects_project', 'progress_id')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scout.PostalAddress']", 'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectProgress']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'projects.projectprogress': {
            'Meta': {'object_name': 'ProjectProgress'},
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

    complete_apps = ['projects']
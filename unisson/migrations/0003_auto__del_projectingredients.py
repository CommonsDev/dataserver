# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectIngredients'
        db.delete_table(u'unisson_projectingredients')


    def backwards(self, orm):
        # Adding model 'ProjectIngredients'
        db.create_table(u'unisson_projectingredients', (
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'unisson', ['ProjectIngredients'])


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
        u'unisson.evaluationingredient': {
            'Meta': {'object_name': 'EvaluationIngredient'},
            'adoption': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['unisson.Ingredient']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"})
        },
        u'unisson.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'example': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'interest': ('django.db.models.fields.TextField', [], {}),
            'wikipage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['unisson']
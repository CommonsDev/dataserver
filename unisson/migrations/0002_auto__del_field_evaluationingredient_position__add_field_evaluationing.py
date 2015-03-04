# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EvaluationIngredient.position'
        db.delete_column(u'unisson_evaluationingredient', 'position')

        # Adding field 'EvaluationIngredient.adoption'
        db.add_column(u'unisson_evaluationingredient', 'adoption',
                      self.gf('django.db.models.fields.CharField')(default='NO', max_length=10),
                      keep_default=False)


        # Changing field 'Ingredient.wikipage'
        db.alter_column(u'unisson_ingredient', 'wikipage', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    def backwards(self, orm):
        # Adding field 'EvaluationIngredient.position'
        db.add_column(u'unisson_evaluationingredient', 'position',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'EvaluationIngredient.adoption'
        db.delete_column(u'unisson_evaluationingredient', 'adoption')


        # Changing field 'Ingredient.wikipage'
        db.alter_column(u'unisson_ingredient', 'wikipage', self.gf('django.db.models.fields.TextField')(null=True))

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
        },
        u'unisson.projectingredients': {
            'Meta': {'object_name': 'ProjectIngredients'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"})
        }
    }

    complete_apps = ['unisson']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Thing.price'
        db.add_column(u'thing_thing', 'price',
                      self.gf('django.db.models.fields.TextField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Thing.price'
        db.delete_column(u'thing_thing', 'price')


    models = {
        u'thing.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'thing.thing': {
            'Meta': {'object_name': 'Thing'},
            'available_at': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'things'", 'to': u"orm['thing.Place']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['thing']
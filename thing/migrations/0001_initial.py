# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table(u'thing_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'thing', ['Place'])

        # Adding model 'Thing'
        db.create_table(u'thing_thing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('available_at', self.gf('django.db.models.fields.related.ForeignKey')(related_name='things', to=orm['thing.Place'])),
        ))
        db.send_create_signal(u'thing', ['Thing'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table(u'thing_place')

        # Deleting model 'Thing'
        db.delete_table(u'thing_thing')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['thing']
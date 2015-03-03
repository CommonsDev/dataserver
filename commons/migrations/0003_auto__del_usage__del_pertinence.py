# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Usage'
        db.delete_table(u'commons_usage')

        # Deleting model 'Pertinence'
        db.delete_table(u'commons_pertinence')


    def backwards(self, orm):
        # Adding model 'Usage'
        db.create_table(u'commons_usage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'commons', ['Usage'])

        # Adding model 'Pertinence'
        db.create_table(u'commons_pertinence', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['commons.Usage'])),
        ))
        db.send_create_signal(u'commons', ['Pertinence'])


    models = {
        
    }

    complete_apps = ['commons']
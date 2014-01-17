# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewsPlugin'
        db.create_table(u'cmsplugin_newsplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Des news', max_length=30, blank=True)),
        ))
        db.send_create_signal(u'cms_news', ['NewsPlugin'])

        # Adding model 'NewsEntry'
        db.create_table(u'cms_news_newsentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news_container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='news_entry', to=orm['cms_news.NewsPlugin'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('content', self.gf('djangocms_text_ckeditor.fields.HTMLField')(blank=True)),
            ('news_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'cms_news', ['NewsEntry'])


    def backwards(self, orm):
        # Deleting model 'NewsPlugin'
        db.delete_table(u'cmsplugin_newsplugin')

        # Deleting model 'NewsEntry'
        db.delete_table(u'cms_news_newsentry')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'cms_news.newsentry': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'NewsEntry'},
            'content': ('djangocms_text_ckeditor.fields.HTMLField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'news_entry'", 'to': u"orm['cms_news.NewsPlugin']"}),
            'news_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'cms_news.newsplugin': {
            'Meta': {'object_name': 'NewsPlugin', 'db_table': "u'cmsplugin_newsplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Des news'", 'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['cms_news']
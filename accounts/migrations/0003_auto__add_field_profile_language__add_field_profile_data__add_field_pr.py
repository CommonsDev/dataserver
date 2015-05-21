# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.language'
        db.add_column(u'accounts_profile', 'language',
                      self.gf('django.db.models.fields.CharField')(default='fr', max_length=5),
                      keep_default=False)

        # Adding field 'Profile.data'
        db.add_column(u'accounts_profile', 'data',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.motto'
        db.add_column(u'accounts_profile', 'motto',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.description'
        db.add_column(u'accounts_profile', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.website'
        db.add_column(u'accounts_profile', 'website',
                      self.gf('django.db.models.fields.URLField')(max_length=384, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.location'
        db.add_column(u'accounts_profile', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scout.Place'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.linkedin'
        db.add_column(u'accounts_profile', 'linkedin',
                      self.gf('django.db.models.fields.URLField')(max_length=384, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.twitter'
        db.add_column(u'accounts_profile', 'twitter',
                      self.gf('django.db.models.fields.URLField')(max_length=384, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.facebook'
        db.add_column(u'accounts_profile', 'facebook',
                      self.gf('django.db.models.fields.URLField')(max_length=384, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.language'
        db.delete_column(u'accounts_profile', 'language')

        # Deleting field 'Profile.data'
        db.delete_column(u'accounts_profile', 'data')

        # Deleting field 'Profile.motto'
        db.delete_column(u'accounts_profile', 'motto')

        # Deleting field 'Profile.description'
        db.delete_column(u'accounts_profile', 'description')

        # Deleting field 'Profile.website'
        db.delete_column(u'accounts_profile', 'website')

        # Deleting field 'Profile.location'
        db.delete_column(u'accounts_profile', 'location_id')

        # Deleting field 'Profile.linkedin'
        db.delete_column(u'accounts_profile', 'linkedin')

        # Deleting field 'Profile.twitter'
        db.delete_column(u'accounts_profile', 'twitter')

        # Deleting field 'Profile.facebook'
        db.delete_column(u'accounts_profile', 'facebook')


    models = {
        u'accounts.objectprofilelink': {
            'Meta': {'object_name': 'ObjectProfileLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isValidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'object_id': ('django.db.models.fields.TextField', [], {}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Profile']"})
        },
        u'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'fr'", 'max_length': '5'}),
            'linkedin': ('django.db.models.fields.URLField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scout.Place']", 'null': 'True', 'blank': 'True'}),
            'motto': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '384', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scout.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'place'", 'to': u"orm['scout.PostalAddress']"}),
            'geo': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'scout.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'address_locality': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_region': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_office_box_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['accounts']
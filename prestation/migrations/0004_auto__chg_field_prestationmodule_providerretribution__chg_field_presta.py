# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field commons on 'PrestationModule'
        db.delete_table(db.shorten_name(u'prestation_prestationmodule_commons'))

        # Adding M2M table for field commonsselected on 'PrestationModule'
        m2m_table_name = db.shorten_name(u'prestation_prestationmodule_commonsselected')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prestationmodule', models.ForeignKey(orm[u'prestation.prestationmodule'], null=False)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prestationmodule_id', 'project_id'])


        # Changing field 'PrestationModule.providerretribution'
        db.alter_column(u'prestation_prestationmodule', 'providerretribution', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'PrestationModule.description'
        db.alter_column(u'prestation_prestationmodule', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'PrestationModule.commonsretribution'
        db.alter_column(u'prestation_prestationmodule', 'commonsretribution', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'PrestationModule.provider'
        db.alter_column(u'prestation_prestationmodule', 'provider', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'PrestationModule.providersupport'
        db.alter_column(u'prestation_prestationmodule', 'providersupport', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Adding M2M table for field commons on 'PrestationModule'
        m2m_table_name = db.shorten_name(u'prestation_prestationmodule_commons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prestationmodule', models.ForeignKey(orm[u'prestation.prestationmodule'], null=False)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prestationmodule_id', 'project_id'])

        # Removing M2M table for field commonsselected on 'PrestationModule'
        db.delete_table(db.shorten_name(u'prestation_prestationmodule_commonsselected'))


        # Changing field 'PrestationModule.providerretribution'
        db.alter_column(u'prestation_prestationmodule', 'providerretribution', self.gf('django.db.models.fields.TextField')(default=1))

        # Changing field 'PrestationModule.description'
        db.alter_column(u'prestation_prestationmodule', 'description', self.gf('django.db.models.fields.TextField')(default=0))

        # Changing field 'PrestationModule.commonsretribution'
        db.alter_column(u'prestation_prestationmodule', 'commonsretribution', self.gf('django.db.models.fields.TextField')(default=0))

        # Changing field 'PrestationModule.provider'
        db.alter_column(u'prestation_prestationmodule', 'provider', self.gf('django.db.models.fields.TextField')(default=0))

        # Changing field 'PrestationModule.providersupport'
        db.alter_column(u'prestation_prestationmodule', 'providersupport', self.gf('django.db.models.fields.TextField')(default=0))

    models = {
        u'prestation.prestation': {
            'Meta': {'object_name': 'Prestation'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'modules'", 'symmetrical': 'False', 'to': u"orm['prestation.PrestationModule']"}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'prestation.prestationmodule': {
            'Meta': {'object_name': 'PrestationModule'},
            'commonsretribution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'commonsselected': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['projects.Project']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'providerretribution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'providersupport': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'baseline': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scout.Place']", 'null': 'True', 'blank': 'True'}),
            'progress': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.ProjectProgress']", 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'projects.projectprogress': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectProgress'},
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

    complete_apps = ['prestation']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrestationModule'
        db.create_table(u'prestation_prestationmodule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('provider', self.gf('django.db.models.fields.TextField')()),
            ('providerpayment', self.gf('django.db.models.fields.TextField')()),
            ('providersupport', self.gf('django.db.models.fields.TextField')()),
            ('commonsretribution', self.gf('django.db.models.fields.TextField')()),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'prestation', ['PrestationModule'])

        # Adding M2M table for field commons on 'PrestationModule'
        m2m_table_name = db.shorten_name(u'prestation_prestationmodule_commons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prestationmodule', models.ForeignKey(orm[u'prestation.prestationmodule'], null=False)),
            ('usage', models.ForeignKey(orm[u'commons.usage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prestationmodule_id', 'usage_id'])

        # Adding model 'Prestation'
        db.create_table(u'prestation_prestation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'prestation', ['Prestation'])

        # Adding M2M table for field module on 'Prestation'
        m2m_table_name = db.shorten_name(u'prestation_prestation_module')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('prestation', models.ForeignKey(orm[u'prestation.prestation'], null=False)),
            ('prestationmodule', models.ForeignKey(orm[u'prestation.prestationmodule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['prestation_id', 'prestationmodule_id'])


    def backwards(self, orm):
        # Deleting model 'PrestationModule'
        db.delete_table(u'prestation_prestationmodule')

        # Removing M2M table for field commons on 'PrestationModule'
        db.delete_table(db.shorten_name(u'prestation_prestationmodule_commons'))

        # Deleting model 'Prestation'
        db.delete_table(u'prestation_prestation')

        # Removing M2M table for field module on 'Prestation'
        db.delete_table(db.shorten_name(u'prestation_prestation_module'))


    models = {
        u'commons.pertinence': {
            'Meta': {'object_name': 'Pertinence'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'usage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['commons.Usage']"})
        },
        u'commons.usage': {
            'Meta': {'object_name': 'Usage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Project']", 'through': u"orm['commons.Pertinence']", 'symmetrical': 'False'})
        },
        u'prestation.prestation': {
            'Meta': {'object_name': 'Prestation'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['prestation.PrestationModule']", 'symmetrical': 'False'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'prestation.prestationmodule': {
            'Meta': {'object_name': 'PrestationModule'},
            'commons': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['commons.Usage']", 'symmetrical': 'False'}),
            'commonsretribution': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.TextField', [], {}),
            'providerpayment': ('django.db.models.fields.TextField', [], {}),
            'providersupport': ('django.db.models.fields.TextField', [], {}),
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
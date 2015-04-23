# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProjectSheetSuggestedItem'
        # db.delete_table(u'projectsheet_projectsheetsuggesteditem')

        # Adding model 'HistoricalProjectSheet'
        db.create_table(u'projectsheet_historicalprojectsheet', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('project_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('template_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('bucket_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('cover_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('videos', self.gf('jsonfield.fields.JSONField')(default=None, null=True, blank=True)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')()),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'projectsheet', ['HistoricalProjectSheet'])

        # Adding model 'ProjectSheetQuestionAnswer'
        # db.create_table(u'projectsheet_projectsheetquestionanswer', (
        #     (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        #     ('projectsheet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_answers', to=orm['projectsheet.ProjectSheet'])),
        #     ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['projectsheet.ProjectSheetQuestion'])),
        #     ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
        # ))
        # db.send_create_signal(u'projectsheet', ['ProjectSheetQuestionAnswer'])

        # Adding field 'ProjectSheet.videos'
        # db.add_column(u'projectsheet_projectsheet', 'videos',
        #               self.gf('jsonfield.fields.JSONField')(default=None, null=True, blank=True),
        #               keep_default=False)


    def backwards(self, orm):
        # Adding model 'ProjectSheetSuggestedItem'
        # db.create_table(u'projectsheet_projectsheetsuggesteditem', (
        #     ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
        #     ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projectsheet.ProjectSheetQuestion'])),
        #     ('projectsheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projectsheet.ProjectSheet'])),
        #     (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        # ))
        # db.send_create_signal(u'projectsheet', ['ProjectSheetSuggestedItem'])

        # Deleting model 'HistoricalProjectSheet'
        db.delete_table(u'projectsheet_historicalprojectsheet')

        # Deleting model 'ProjectSheetQuestionAnswer'
        # db.delete_table(u'projectsheet_projectsheetquestionanswer')

        # Deleting field 'ProjectSheet.videos'
        # db.delete_column(u'projectsheet_projectsheet', 'videos')


    models = {
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
        u'bucket.bucket': {
            'Meta': {'object_name': 'Bucket'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buckets_created'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'bucket.bucketfile': {
            'Meta': {'object_name': 'BucketFile'},
            'being_edited_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'editor_of'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['bucket.Bucket']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uploader_of'", 'to': u"orm['auth.User']"}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
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
        u'projectsheet.historicalprojectsheet': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalProjectSheet'},
            'bucket_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'cover_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'project_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'template_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'videos': ('jsonfield.fields.JSONField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'projectsheet.projectsheet': {
            'Meta': {'object_name': 'ProjectSheet'},
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bucket.Bucket']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bucket.BucketFile']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['projects.Project']", 'unique': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projectsheet.ProjectSheetTemplate']"}),
            'videos': ('jsonfield.fields.JSONField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'projectsheet.projectsheetquestion': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ProjectSheetQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['projectsheet.ProjectSheetTemplate']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projectsheet.projectsheetquestionanswer': {
            'Meta': {'ordering': "('question__order',)", 'object_name': 'ProjectSheetQuestionAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projectsheet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_answers'", 'to': u"orm['projectsheet.ProjectSheet']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['projectsheet.ProjectSheetQuestion']"})
        },
        u'projectsheet.projectsheettemplate': {
            'Meta': {'object_name': 'ProjectSheetTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortdesc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['projectsheet']

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Label'
        db.create_table(u'flipflop_label', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'flipflop', ['Label'])

        # Adding model 'Board'
        db.create_table(u'flipflop_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'flipflop', ['Board'])

        # Adding M2M table for field labels on 'Board'
        m2m_table_name = db.shorten_name(u'flipflop_board_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('board', models.ForeignKey(orm[u'flipflop.board'], null=False)),
            ('label', models.ForeignKey(orm[u'flipflop.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['board_id', 'label_id'])

        # Adding model 'List'
        db.create_table(u'flipflop_list', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lists', to=orm['flipflop.Board'])),
        ))
        db.send_create_signal(u'flipflop', ['List'])

        # Adding model 'Card'
        db.create_table(u'flipflop_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submitted_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submitted_cards', to=orm['auth.User'])),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cards', to=orm['flipflop.List'])),
        ))
        db.send_create_signal(u'flipflop', ['Card'])

        # Adding M2M table for field assigned_to on 'Card'
        m2m_table_name = db.shorten_name(u'flipflop_card_assigned_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'flipflop.card'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'user_id'])

        # Adding M2M table for field labels on 'Card'
        m2m_table_name = db.shorten_name(u'flipflop_card_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'flipflop.card'], null=False)),
            ('label', models.ForeignKey(orm[u'flipflop.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'label_id'])

        # Adding model 'Task'
        db.create_table(u'flipflop_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['flipflop.Card'])),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'flipflop', ['Task'])

        # Adding model 'CardComment'
        db.create_table(u'flipflop_cardcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['flipflop.Card'])),
            ('posted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'flipflop', ['CardComment'])


    def backwards(self, orm):
        # Deleting model 'Label'
        db.delete_table(u'flipflop_label')

        # Deleting model 'Board'
        db.delete_table(u'flipflop_board')

        # Removing M2M table for field labels on 'Board'
        db.delete_table(db.shorten_name(u'flipflop_board_labels'))

        # Deleting model 'List'
        db.delete_table(u'flipflop_list')

        # Deleting model 'Card'
        db.delete_table(u'flipflop_card')

        # Removing M2M table for field assigned_to on 'Card'
        db.delete_table(db.shorten_name(u'flipflop_card_assigned_to'))

        # Removing M2M table for field labels on 'Card'
        db.delete_table(db.shorten_name(u'flipflop_card_labels'))

        # Deleting model 'Task'
        db.delete_table(u'flipflop_task')

        # Deleting model 'CardComment'
        db.delete_table(u'flipflop_cardcomment')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flipflop.board': {
            'Meta': {'object_name': 'Board'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'boards'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['flipflop.Label']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flipflop.card': {
            'Meta': {'ordering': "('submitted_date', 'title')", 'object_name': 'Card'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigned_to': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['flipflop.Label']", 'null': 'True', 'blank': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards'", 'to': u"orm['flipflop.List']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'submitted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submitted_cards'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flipflop.cardcomment': {
            'Meta': {'object_name': 'CardComment'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['flipflop.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'flipflop.label': {
            'Meta': {'object_name': 'Label'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flipflop.list': {
            'Meta': {'object_name': 'List'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lists'", 'to': u"orm['flipflop.Board']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flipflop.task': {
            'Meta': {'object_name': 'Task'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': u"orm['flipflop.Card']"}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['flipflop']
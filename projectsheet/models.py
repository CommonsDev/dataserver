from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from projects.models import Project
from autoslug.fields import AutoSlugField
from bucket.models import Bucket, BucketFile
from jsonfield import JSONField

try:
    # python >= 2.7
    from collections import OrderedDict
except:
    # need to install ordereddict package
    from ordereddict import OrderedDict

class ProjectSheetTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)
    shortdesc = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class ProjectSheetQuestion(models.Model):
    template = models.ForeignKey(ProjectSheetTemplate)
    order = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s - %s" % (self.order, self.text)

    class Meta:
        ordering = ('order',)

class ProjectSheet(models.Model):
    project = models.OneToOneField(Project)
    template = models.ForeignKey(ProjectSheetTemplate)
    bucket = models.ForeignKey(Bucket, null=True, blank=True)
    cover = models.ForeignKey(BucketFile, null=True, blank=True)
    videos = JSONField(default=None, blank=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (_('Project sheet for '), self.project)

def createProjectSheetBucket(sender, instance, **kwargs):
    bucket_name = instance.project.slug
    bucket_owner = User.objects.get(pk=-1) # FIXME : to whom should bucket projects belong ? default to Anonymous user by now
    projectsheet_bucket, created = Bucket.objects.get_or_create(created_by=bucket_owner,
                                                name=bucket_name)
    instance.bucket = projectsheet_bucket

class ProjectSheetSuggestedItem(models.Model):
    projectsheet = models.ForeignKey(ProjectSheet)
    question = models.ForeignKey(ProjectSheetQuestion)
    answer = models.TextField(blank=True)

    class Meta:
        ordering = ("question__order",)
#
# def createProjectSheetSuggestedItem(sender, instance, created, **kwargs):
#     for question in instance.template.projectsheetquestion_set.all():
#         ProjectSheetSuggestedItem.objects.create(projectsheet=instance,
#                                                  question=question)
#
# # post_save.connect(createProjectSheetSuggestedItem, ProjectSheet)
pre_save.connect(createProjectSheetBucket, ProjectSheet)

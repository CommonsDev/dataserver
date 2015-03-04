from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager
from scout.models import PostalAddress
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

class ProjectProgressRange(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)

class ProjectProgress(models.Model):
    progress_range = models.ForeignKey(ProjectProgressRange)
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    icon = models.ImageField(upload_to='progress_icons')

    class Meta:
        ordering  = ['order',]

class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True)
    baseline = models.CharField(max_length=250, null=True, blank=True)
    tags = TaggableManager(blank=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(PostalAddress, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    progress = models.ForeignKey(ProjectProgress, null=True, blank=True)

    def __unicode__(self):
        return self.title

class ProjectTeam(models.Model):
    project = models.ForeignKey(Project)
    members = models.ManyToManyField(Profile)

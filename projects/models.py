from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager
from scout.models import Place

class ProjectProgressRange(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)

    def __unicode__(self):
        return u"%s" % self.name

class ProjectProgress(models.Model):
    progress_range = models.ForeignKey(ProjectProgressRange)
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='progress_icons')

    class Meta:
        ordering  = ['order',]

    def __unicode__(self):
        return u"%s - %s - %s" % (self.progress_range, self.order, self.label)

class Project(models.Model):
    """
    A project is any idea you can document
    """
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True)
    baseline = models.CharField(max_length=250, null=True, blank=True)
    tags = TaggableManager(blank=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Place, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    progress = models.ForeignKey(ProjectProgress, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

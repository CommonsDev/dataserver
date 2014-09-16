from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager

class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True)
    baseline = models.CharField(max_length=250, null=True, blank=True)
    tags = TaggableManager(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    begin_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.title

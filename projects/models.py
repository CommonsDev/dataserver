""" Projects and related models. """

from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager
from scout.models import Place
from accounts.models import Profile
# from django.db.models.signals import post_save
# from django.dispatch.dispatcher import receiver


class ProjectProgressRange(models.Model):

    """ A project progress range. """

    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)

    def __unicode__(self):
        """ pep257, you know I love you. """

        return u"%s" % self.name


class ProjectProgress(models.Model):

    """ A project progress. """

    progress_range = models.ForeignKey(ProjectProgressRange)
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    icon = models.ImageField(upload_to='progress_icons')

    class Meta:
        ordering  = ['order', ]

    def __unicode__(self):
        """ pep257, you know I love you. """

        return u"%s - %s - %s" % (self.progress_range, self.order, self.label)


class Project(models.Model):

    """ A project is any idea you can document. """

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
        """ pep257, you know I love you. """
        return self.title


# XXX/TODO: obsolete
class ProjectTeam(models.Model):

    """ A project team.

    .. todo:: this model is probably obsolete.
        Someones knowing the truth checks it?
    """

    project = models.ForeignKey(Project)
    members = models.ManyToManyField(Profile)

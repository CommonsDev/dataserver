from django.db import models
from projects.models import Project

class ToolCategory(models.Model):
    """
    Categories for tools used in projects
    """
    label = models.CharField(max_length=200)
    baseline = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()

    def __unicode__(self):
        return unicode(self.label)

class ProjectTool(models.Model):
    """
    Any external tool that a project can use
    """
    project = models.ForeignKey(Project, related_name='tools')
    category = models.ForeignKey(ToolCategory, related_name='project_tools')
    description = models.TextField(blank=True, verbose_name=('tool description'))
    uri = models.URLField(null=True, blank=True, verbose_name=('link to the tool'))

    def __unicode__(self):
        return unicode(self.description)

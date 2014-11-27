from django.db import models
from projects.models import Project

class ToolCategory(models.Model):
    label = models.CharField(max_length=200)
    baseline = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.label)	
    
class ProjectTool(models.Model):
    project = models.OneToOneField(Project, related_name='project_tools')
    category = models.OneToOneField(ToolCategory, related_name='project_categories')
    description = models.TextField(blank=True, verbose_name=('tool description'))
    website = models.URLField(null=True, blank=True, verbose_name=('link to the tool'))

    def __unicode__(self):
        return self.description
from django.db import models
from projects.models import Project

class ToolCategory(models.Model):
    toolcategory = models.CharField(max_length=200)
    description = models.CharField(verbose_name=("description"), max_length=500, null=True, blank=True)
    example = models.TextField()
    website = models.URLField(null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.toolcategory)	
    
class ProjectTools(models.Model):
    project = models.OneToOneField(Project, related_name='project_category')
    category = models.OneToOneField(ToolCategory)
    projecttool = models.TextField(blank=True, verbose_name=('tool description'))
    website = models.URLField(null=True, blank=True, verbose_name=('link to the tool'))

    def __unicode__(self):
        return self.projecttool
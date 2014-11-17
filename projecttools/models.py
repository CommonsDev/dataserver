from django.db import models
from projects.models import Project

class ProjectTools(models.Model):
    project = models.OneToOneField(Project)
    contribution_meeting = models.TextField(blank=True)
    contribution_onlinemeeting = models.TextField(blank=True)
    def __unicode__(self):
        return self.contribution_meeting
    

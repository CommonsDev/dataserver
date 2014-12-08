from django.db import models
from projects.models import Project
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from autoslug.fields import AutoSlugField
    

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
    
    def __unicode__(self):
        return u"%s %s" % (_('Project sheet for '), self.project)
    
class ProjectSheetSuggestedItem(models.Model):
    projectsheet = models.ForeignKey(ProjectSheet)
    question = models.ForeignKey(ProjectSheetQuestion)
    answer = models.TextField(blank=True)
    
    class Meta:
        ordering = ("question__order",)
    
def createProjectSheetSuggestedItem(sender, instance, created, **kwargs):
    for question in instance.template.projectsheetquestion_set.all():
        ProjectSheetSuggestedItem.objects.create(projectsheet=instance,
                                                 question=question)

post_save.connect(createProjectSheetSuggestedItem, ProjectSheet)
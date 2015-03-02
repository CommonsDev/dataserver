from django.db import models

# Create your models here.

from projects.models import Project

class PrestationModule(models.Model):
	title = models.CharField(verbose_name=("Module title"), max_length=500, null=True, blank=True)
	description = models.TextField(verbose_name=("Description de l'objectif"), null=True, blank=True)
	provider = models.TextField(verbose_name=("Prestataire et mission"), null=True, blank=True)
	providerretribution = models.TextField(verbose_name=("Retribution du prestataire"),null=True, blank=True)
	providersupport = models.TextField(verbose_name=("Soutien du prestataire"), null=True, blank=True)
	commonsselected = models.ManyToManyField(Project,null=True, blank=True,verbose_name=("Choix du ou des communs"), related_name='prestation_module')
	commonsretribution = models.TextField(null=True, blank=True, verbose_name=("Retribution du commun"))

	class Meta:
		app_label='commons'

	def __unicode__(self):  # Python 3: def __str__(self):
		return unicode(self.title)

class Prestation(models.Model):
	title = models.CharField(verbose_name=("Prestation title"), max_length=500, null=True, blank=True)
	description = models.TextField()
	link = models.URLField(verbose_name=("Link to the prestation"), null=True, blank=True)
	organization = models.CharField(verbose_name=("commanditaire"), max_length=500, null=True, blank=True)
	module = models.ManyToManyField(PrestationModule, related_name='modules',  through="SelectedModules")

	def __unicode__(self):  # Python 3: def __str__(self):
		return unicode(self.title)

	class Meta:
		app_label='commons'


class SelectedModules(models.Model):
	prestation = models.ForeignKey(Prestation)
	modules = models.ForeignKey(PrestationModule)
	
	class Meta:
		app_label='commons'

	def __unicode__(self):  # Python 3: def __str__(self):
		return u"%s - %s" % (self.prestation, self.modules)

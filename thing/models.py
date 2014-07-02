from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.

class Place(models.Model):
	 name = models.CharField(max_length=255)
	 description = models.TextField()
	 address = models.TextField(default="")
	 
	 def __unicode__(self):
	 	return self.name

class Thing(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	price = models.CharField(max_length=255)
	available_at = models.ForeignKey(Place, related_name='things')

	def __unicode__(self):
		return self.name

class PeopleThing(models.Model):
	name = models.CharField(max_length=255)
	thing = models.ForeignKey(Thing, related_name='thing')
	assigned_to = models.ManyToManyField(User, verbose_name=('assigned to'), blank=True)

	def __unicode__(self):
		return self.name
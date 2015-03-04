# *-* encoding:utf-8 *-*

from django.db import models

# Create your models here.

from projects.models import Project


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=200)
    baseline = models.CharField(verbose_name=("one line description"), max_length=500, null=True, blank=True)
    description = models.TextField()
    interest = models.TextField()
    example = models.TextField()
    wikipage = models.URLField(null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.ingredient)

class EvaluationIngredient(models.Model):
	ADOPTION_CHOICES = (
		('NO', u"Ne souhaite pas"),
		('NOTAPP', u"Pas applicable"),
		('WISH', u"Souhait mais pas démarré"),
		('STARTED',u"Démarré"),
		('WIP',u"En progression"),
		('DONE',u"Réalisé"),
		)
	ingredient = models.ForeignKey(Ingredient)
	project = models.ForeignKey(Project, related_name='unisson_ingredients')
	adoption = models.CharField(max_length=10, choices=ADOPTION_CHOICES)
	comment = models.TextField()

	@property
	def score(self):
		return {'NO': -1000,
		 'NOTAPP': 0,
		 'WISH': 1,
		 'STARTED': 2,
		 'WIP': 3,
		 'DONE': 4}[self.adoption]

	def __unicode__(self):  # Python 3: def __str__(self):
           return  u"%s - %s" % (self.ingredient, self.project)
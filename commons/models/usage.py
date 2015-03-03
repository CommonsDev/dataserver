from django.db import models
from projects.models import Project

class Usage(models.Model):
    label = models.CharField(max_length=200)
    project = models.ManyToManyField(Project, through="Pertinence")

    class Meta:
        app_label='commons'

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.label


class Pertinence(models.Model):
    usage = models.ForeignKey(Usage)
    project = models.ForeignKey(Project)

    @property
    def unisson_score(self):
        score = 0
        for ingredient in self.project.unisson_ingredients.all():
            score += ingredient.score
        return score

    comment = models.TextField(blank=True, null=True)

    class Meta:
        app_label='commons'

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s - %s - %s" % (self.project, self.usage, self.comment)

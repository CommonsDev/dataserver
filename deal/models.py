from django.db import models

from django.contrib.auth.models import User

class Deal(models.Model):
    text = models.TextField()
    dealer = models.ForeignKey(User, related_name='deals')
    members = models.ManyToManyField(User, blank=True, related_name='deal_participated')
    when = models.DateTimeField()
    ressource_uri = models.URLField()

    def __unicode__(self):
        return "%s - %s " % (self.text, self.dealer)

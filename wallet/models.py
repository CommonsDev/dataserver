from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Wallet(models.Model):
    owner = models.ForeignKey(User, verbose_name=('assigned to'), blank=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
    	return  u"%s - %s" % (self.owner, self.balance)
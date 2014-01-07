from django.db import models
from cms.models import CMSPlugin

from scout.models import Map

class CartoPlugin(CMSPlugin):
    carto = models.ForeignKey(Map)

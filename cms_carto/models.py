from django.db import models
from cms.models import CMSPlugin

from scout.models import Map


class CartoPlugin(CMSPlugin):
    """
    Toy class to ket users choose the gup map of their choice
    """
    carto = models.ForeignKey(Map, null=True)

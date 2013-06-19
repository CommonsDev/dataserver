from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from accounts.models import GUPProfile

class TileLayer(models.Model):
    """
    A Tile layer for a given map.
    """
    name = models.CharField(max_length=200, verbose_name=_("name"))
    url_template = models.CharField(max_length=200, help_text=_("URL template using OSM tile format"))
    min_zoom = models.IntegerField(default=0)
    max_zoom = models.IntegerField(default=18)
    attribution = models.CharField(max_length=300)

    @classmethod
    def get_default(cls):
        """
        Returns the default tile layer (used for a map when no layer is set).
        """
        return cls.objects.order_by('pk')[0]  # FIXME, make it administrable
    
    def __unicode__(self):
        return self.name or "Unnamed layer"


class Map(models.Model):
    """
    A map.
    """
    slug = models.SlugField(db_index=True)
    name = models.CharField(max_length=200, verbose_name=_("name"))        
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))

    # Geo attributes
    center = models.PointField(geography=True, verbose_name=_("center"))
    zoom = models.IntegerField(default=7, verbose_name=_("zoom"))
    locate = models.BooleanField(default=False, verbose_name=_("locate"), help_text=_("Locate user on load?"))
    modified_at = models.DateTimeField(auto_now=True)
    tilelayers = models.ManyToManyField(TileLayer, related_name='maps')

    objects = models.GeoManager()

    def get_absolute_url(self):
        return reverse("map", kwargs={'slug': self.slug, 'username': self.owner.username})

    def __unicode__(self):
        return self.name or "Unnamed map"
        
import os
def marker_upload(instance, filename):
    return os.path.join(instance.id)
        
class Marker(models.Model):
    """
    Point of interest.
    """
    position = models.PointField(geography=True)
    tile_layer = models.ForeignKey(TileLayer, related_name='markers')

    created_by = models.ForeignKey(GUPProfile)
    created_on = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    picture = models.ImageField(upload_to=marker_upload,
                                null=True, blank=True)
    
    objects = models.GeoManager()

import os

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField

from accounts.models import GUPProfile
from bucket.models import Bucket

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
    slug = AutoSlugField(db_index=True, populate_from='name', unique=True)
    name = models.CharField(max_length=200, verbose_name=_("name"))        
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))

    # Geo attributes
    center = models.PointField(geography=True, verbose_name=_("center"))
    zoom = models.IntegerField(default=7, verbose_name=_("zoom"))
    locate = models.BooleanField(default=False, verbose_name=_("locate"), help_text=_("Locate user on load?"))
    modified_at = models.DateTimeField(auto_now=True)
    tilelayer = models.ForeignKey(TileLayer, related_name='maps')

    # File container (bucket)
    bucket = models.ForeignKey(Bucket, related_name='map')

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tilelayer = TileLayer.objects.all()[0]
            if not self.bucket:
                self.bucket = Bucket.objects.create()
            

        result = super(Map, self).save(*args, **kwargs)
            
        # Add a data layer once saved
        if len(self.datalayers.all()) == 0:
            DataLayer.objects.create(map=self)
            
        return result 

    def get_absolute_url(self):
        return reverse("map", kwargs={'slug': self.slug, 'username': self.owner.username})

    def __unicode__(self):
        return self.name or "Unnamed map"
        

class DataLayer(models.Model):
    """
    A layer containing features (markers, polylines and polygons)
    """
    map = models.ForeignKey(Map, related_name='datalayers')

    def __unicode__(self):
        return u"Datalayer for %s" % self.map
    
    
class MarkerCategory(models.Model):
    """
    A category for a marker
    """
    name = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=255)
    icon_color = models.CharField(max_length=30)
    marker_color = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name
            
class Marker(models.Model):
    """
    Point of interest.
    """
    position = models.PointField(geography=True)
    datalayer = models.ForeignKey(DataLayer, related_name='markers')

    address = models.TextField(default="")

    created_by = models.ForeignKey(GUPProfile)
    created_on = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(MarkerCategory, related_name='markers')

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def marker_upload(instance, filename):
        return os.path.join(instance.id)
    
    picture_url = models.URLField(blank=True)
    
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s" % (self.title or 'marker')

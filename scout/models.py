from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


class TileLayer(models.Model):
    """
    A Tile layer for a given map.
    """
    name = models.CharField(max_length=200, verbose_name=_("name"))
    url_template = models.CharField(max_length=200, help_text=_("URL template using OSM tile format"))
    min_zoom = models.IntegerField(default=0)
    max_zoom = models.IntegerField(default=18)
    attribution = models.CharField(max_length=300)

    @property
    def json(self):
        return dict((field.name, getattr(self, field.name)) for field in self._meta.fields)

    @classmethod
    def get_default(cls):
        """
        Returns the default tile layer (used for a map when no layer is set).
        """
        return cls.objects.order_by('pk')[0]  # FIXME, make it administrable


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
    tilelayers = models.ManyToManyField(TileLayer, through="MapToTileLayer")

    objects = models.GeoManager()

    def get_absolute_url(self):
        return reverse("map", kwargs={'slug': self.slug, 'username': self.owner.username})

class MapToTileLayer(models.Model):
    tilelayer = models.ForeignKey(TileLayer)
    map = models.ForeignKey(Map)
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['rank', 'tilelayer__name']


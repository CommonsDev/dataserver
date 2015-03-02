import os

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField
from guardian.shortcuts import assign_perm

from bucket.models import Bucket

## Transitional schema for a postal address
class PostalAddress(models.Model):
    """
    The mailing address
    http://schema.org/PostalAddress

    For the country codes, see http://en.wikipedia.org/wiki/ISO_3166-1
    """
    country = models.CharField(max_length=2)
    address_locality = models.CharField(max_length=255, blank=True)
    address_region = models.CharField(max_length=50, blank=True)
    post_office_box_number = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=30, blank=True)
    street_address = models.TextField(blank=True)

    def __unicode__(self):
        return "%s, %s - %s (%s)" % (self.post_office_box_number,
                                     self.street_address,
                                     self.address_locality,
                                     self.country)

class Place(models.Model):
    """
    A place, from
    http://schema.org/Place
    """
    address = models.ForeignKey(PostalAddress, related_name='place')
    geo = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s" % self.address

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
        return self.name or u"Unnamed layer"


class Map(models.Model):
    """
    A map.
    """
    PRIVACY_CHOICES = (
        ('GROUP_RW', _("RW for the group")),
        ('GROUP_RW_OTHERS_RO', _("RO for anyone and RW for the Group"))
    )

    class Meta:
        permissions = (
            ('view_map', _("View Map")),
        )

    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES)

    slug = AutoSlugField(db_index=True, populate_from='name', unique=True)
    name = models.CharField(max_length=200, verbose_name=_("name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))

    # Geo attributes
    center = models.PointField(geography=True, verbose_name=_("center"))
    zoom = models.IntegerField(default=7, verbose_name=_("zoom"))
    locate = models.BooleanField(default=False, verbose_name=_("locate"), help_text=_("Locate user on load?"))
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='maps_created')
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
        return self.name or u"Unnamed map"


class DataLayer(models.Model):
    """
    A layer containing features (markers, polylines and polygons)
    """
    map = models.ForeignKey(Map, related_name='datalayers')
    geojson = models.TextField(null=True, blank=True)

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

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(MarkerCategory, related_name='markers')

    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    video_src = models.TextField(null=True, blank=True)

    def marker_upload(instance, filename):
        return os.path.join(instance.id)

    # is URLField really required here ?? that make it not usable for relative urls
    picture_url = models.CharField(max_length=255, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s" % (self.title or 'marker')


@receiver(post_save, sender=Map)
def allow_user_to_edit_maps(sender, instance, created, *args, **kwargs):
    assign_perm("view_map", user_or_group=instance.created_by, obj=instance)
    assign_perm("change_map", user_or_group=instance.created_by, obj=instance)
    assign_perm("delete_map", user_or_group=instance.created_by, obj=instance)

    assign_perm("view_bucket", user_or_group=instance.created_by, obj=instance.bucket)
    assign_perm("change_bucket", user_or_group=instance.created_by, obj=instance.bucket)
    assign_perm("delete_bucket", user_or_group=instance.created_by, obj=instance.bucket)


@receiver(post_save, sender=User)
def allow_user_to_create_map_via_api(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("scout.add_map", instance)

import os
import re
import ckeditor.fields
import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Page
from cms.utils import get_cms_setting

#from cms_news import settings
from .utils import calculate_image_path


#class PublishedNewsManager(models.Manager):
    #"""
        #Filters out all unpublished and items with a publication date in the future
    #"""
    #def get_query_set(self):
        #return super(PublishedNewsManager, self).get_query_set() \
                    #.filter(is_published=True) \
                    #.filter(pub_date__lte=datetime.datetime.now())
    
class NewsPlugin(CMSPlugin):
    name = models.CharField(max_length=30)

#class News(CMSPlugin):
class NewsEntry(models.Model):
    """
    A piece of News
    """
    news = models.ForeignKey(NewsPlugin, related_name="news")
    title = models.CharField(_('Title'), max_length=255, blank=True)
    content = models.TextField(_('Content'), blank=True)
    # content = ckeditor.fields.RichTextField(_('Content'), blank=True)
    news_picture = models.ImageField(_("News preview image(smaller - 100x100px)"), upload_to=calculate_image_path, max_length=255, null=True, blank=True)

    is_published = models.BooleanField(_('Published'), default=False)
    pub_date = models.DateTimeField(_('Publication date'), default=datetime.datetime.now)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    #published = PublishedNewsManager()
    #objects = models.Manager()
    
    url = models.CharField(_("link"), max_length=255, blank=True, null=True,
        help_text=_("If present, clicking on image will take user to link."))
            
    def get_news_picture_url(self):
        try:
            return self.news_picture.url
        except ValueError:
            return None
    
    class Meta:
        verbose_name = _('News Entry')
        verbose_name_plural = _('News')
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title


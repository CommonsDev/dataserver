import os, re, datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin, Page
from cms.utils import get_cms_setting
from djangocms_text_ckeditor.fields import HTMLField

from .utils import calculate_image_path

class NewsPlugin(CMSPlugin):
    name = models.CharField(max_length=30, blank=True)
    
    def copy_relations(self, oldinstance):
        print "== copying old instances ==="
        print "# old instance : %s" % (oldinstance)
        print "# new instance : %s" % (self)
        
        for news_entry in oldinstance.news_entry.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            news_entry.pk = None
            news_entry.news_container = self
            news_entry.save()

class NewsEntry(models.Model):
    """
    A piece of News
    """
    news_container = models.ForeignKey(NewsPlugin, related_name="news_entry")
    title = models.CharField(_('Title'), max_length=255, blank=True)
    content = HTMLField(_('Content'), blank=True)
    news_picture = models.ImageField(_("News Image"), upload_to=calculate_image_path, max_length=255, null=True, blank=True)

    is_published = models.BooleanField(_('Published'), default=False)
    pub_date = models.DateTimeField(_('Publication date'), default=datetime.datetime.now)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

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


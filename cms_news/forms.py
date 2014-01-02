from __future__ import absolute_import
from django.forms.models import ModelForm
from django.conf import settings

from cms.plugin_pool import plugin_pool
#from cms.plugins.text.settings import USE_TINYMCE

#from cmsplugin_news.widgets.wymeditor_widget import WYMEditor
from cms_news.models import NewsEntry


class NewsForm(ModelForm):
    class Meta:
        model = NewsEntry

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
       

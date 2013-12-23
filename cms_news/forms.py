from __future__ import absolute_import
from django.forms.models import ModelForm
from django.conf import settings

from cms.plugin_pool import plugin_pool
#from cms.plugins.text.settings import USE_TINYMCE

#from cmsplugin_news.widgets.wymeditor_widget import WYMEditor
from cms_news.models import News


class NewsForm(ModelForm):
    class Meta:
        model = News

#    def _get_widget(self):
#        plugins = plugin_pool.get_text_enabled_plugins(placeholder=None,
#                page=None)
#        if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
#            from cmsplugin_news.widgets.tinymce_widget import TinyMCEEditor
#            return TinyMCEEditor(installed_plugins=plugins)
#        else:
#            return WYMEditor(installed_plugins=plugins)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
       
       # widget = self._get_widget()
       # self.fields['excerpt'].widget = widget
       # self.fields['content'].widget = widget

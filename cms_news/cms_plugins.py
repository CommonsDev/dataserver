from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cms_news.models import NewsPlugin, NewsEntry


class NewsEntryInline(admin.StackedInline):
    model = NewsEntry

class CMSNewsPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = NewsPlugin
    name = _('News container')
    render_template = "cms_news/news_list.html"
    inlines = [NewsEntryInline]

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        latest = NewsEntry.objects.all().order_by('-pub_date')[:10]
        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
        })
        return context    

plugin_pool.register_plugin(CMSNewsPlugin)

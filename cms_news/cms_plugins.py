from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cms_news.models import LatestNewsPlugin, News, ArchiveNewsPlugin


class CMSNewsPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = News
    name = _('News')
    render_template = "cms_news/news_list.html"

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        latest = News.objects.all().order_by('pub_date')[:5]
        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
        })
        return context

    save_as = False
    save_on_top = True
    
plugin_pool.register_plugin(CMSNewsPlugin)

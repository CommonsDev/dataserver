from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms_carto.models import CartoPlugin as CartoPluginModel
from django.utils.translation import ugettext as _

class CartoPlugin(CMSPluginBase):
    model = CartoPluginModel # Model where data about this plugin is saved
    name = _("Cartographie") # Name of the plugin
    render_template = "cms_carto/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(CartoPlugin) # register the plugin

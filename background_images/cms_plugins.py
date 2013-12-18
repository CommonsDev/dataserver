from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from background_images.models import BackgroundImagesPlugin as BackgroundImagesPluginModel
from django.utils.translation import ugettext as _

class BackgroundImagesPlugin(CMSPluginBase):
    model = BackgroundImagesPluginModel # Model where data about this plugin is saved
    name = _("Background Images Plugin") # Name of the plugin
    render_template = "background_images/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(BackgroundImagesPlugin) # register the plugin

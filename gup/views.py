from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView

from cms.models import Page
from cms.api import create_page, add_plugin

from gup import settings

class CMSRedirectView(RedirectView):
  """
    a view aimed at redirecting to base CMS views after some checks
    - 1st time : create a home page with all plugins 
    - Then: redirect to cms user home page
  """
  def get_redirect_url(self, **kwargs):
      return self.page.get_absolute_url()
  
  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    
    # check if logged in user has already created a page 
    try:
      self.page = Page.objects.get(created_by=request.user, published=True, publisher_is_draft=True, is_home=False, template=settings.PROJECT_PAGE_TEMPLATE)
    
    except:      
      # else, create page and hook plugins to placeholders :      
      page_name = 'home-%s' % (request.user)
      self.page = create_page(page_name, settings.PROJECT_PAGE_TEMPLATE, 'fr', created_by=request.user, published=True)
      # logo 
      logo_ph = self.page.placeholders.get(slot='logo')
      add_plugin(logo_ph, 'PicturePlugin', 'fr')
      # project_description
      descr_ph = self.page.placeholders.get(slot='project_description')
      add_plugin(descr_ph, 'TextPlugin', 'fr', body='Cliquez pour ajouter la description du projet')
      # project_pictures
      pic_ph = self.page.placeholders.get(slot='project_pictures')
      add_plugin(pic_ph, 'BackgroundImagesPlugin', 'fr')
      # news_block
      news_ph = self.page.placeholders.get(slot='news_block')
      add_plugin(news_ph, 'CMSNewsPlugin', 'fr')
      # carto
      carto_ph = self.page.placeholders.get(slot='carto')
      add_plugin(carto_ph, 'CartoPlugin', 'fr')

    return super(CMSRedirectView, self).dispatch(request, *args, **kwargs)
  
  
  
  

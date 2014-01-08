from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView

class CMSRedirectView(RedirectView):
  """
    a view aimed at redirecting to base CMS views after some checks
    - 1st time : create a home page with all plugins 
    - Then: redirect to cms homepage 
  """
   
  def dispatch(self, request, *args, **kwargs):
    # if: logged in user has already created a page
    
    # then: RETURN redirect to that page
    # else: create a new home page
    # hook plugins to placeholders : 
      # logo : image
      # project : text + add default text (to make it clickable)
      # image background
      # news
      # carto
    return super(CMSRedirectView, self).dispatch(request, *args, **kwargs)
  
  def get_redirect_url(self):
    #return reverse('cms_home')
    return '/'
  
  
  

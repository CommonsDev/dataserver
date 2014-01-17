from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext
from django.db import models

from cms_news.models import NewsEntry


class NewsEntryAdmin(admin.ModelAdmin):
    """
    Admin for news entries
    """
    date_hierarchy = 'pub_date'
    list_display = ('title', 'news_picture', 'pub_date', 'news_container')
    search_fields = ['title', 'content']
    
    save_as = True
    save_on_top = True
    
    def queryset(self, request):
        """
            Override to use the objects and not just the default visibles only.
        """
        return NewsEntry.objects.all()

admin.site.register(NewsEntry, NewsEntryAdmin)

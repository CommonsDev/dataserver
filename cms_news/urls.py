from django.conf.urls.defaults import *

from cms_news import views


urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$',
        views.ArchiveIndexView.as_view(), name='news_archive_index'),

    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(), name='news_archive_year'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(), name='news_archive_month'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(), name='news_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.DetailView.as_view(), name='news_detail'),

)

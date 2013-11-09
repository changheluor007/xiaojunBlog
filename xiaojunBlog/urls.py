#coding=utf8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps import  views as sitemap_views
from django.views.decorators.cache import  cache_page
from feeds import LatestEntriesFeed
from sitemap import  PostSitemap
from blog.views import IndexView,CategoryListView,TagsListView,PostDetailView,PagedetailView
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xiaojunBlog.views.home', name='home'),
    # url(r'^xiaojunBlog/', include('xiaojunBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls),name='admin'),

    url(r'^$',IndexView.as_view(),name='home'),

    url(r'^feed|rss/$',LatestEntriesFeed()),

    url(r'^sitemap\.xml$',cache_page(sitemap_views.sitemap,60*60*12),{'sitemaps':{'post':PostSitemap}}),

    url(r'^category/(?P<alias>\w+)/',CategoryListView.as_view()),

    url(r'^tag/(?P<tag>[\w|\.|\-]+)/$',TagsListView.as_view()),

    url(r'^(?P<slug>[\w|\-|\d|\W]+?).html$',PostDetailView.as_view()),

    url(r'^(?P<slug>\w+)/$',PagedetailView.as_view()),

    url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc', {}, 'xmlrpc'),

)
urlpatterns += staticfiles_urlpatterns()




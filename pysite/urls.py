from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pysite.views.home', name='home'),
    # url(r'^pysite/', include('pysite.foo.urls')),
    (r'^mysite/$', 'pysite.main.index'), 
    (r'^mysite/helloworld/$', 'pysite.main.helloworld'), 
    (r'^mysite/helloworld/results/$', 'pysite.main.results'), 
    (r'^mysite/paraselection/$', 'pysite.main.paraselection'),
    (r'^mysite/customize/$', 'pysite.main.customize'),
    (r'^mysite/startpage/$', 'pysite.main.startpage'),
    (r'^mysite/result/$', 'pysite.main.results'),
    (r'^mysite/result/(\d{11,13})/$', 'pysite.main.final'),
    (r'^message/$', 'pysite.main.message'),
#    (r'^mysite/download(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:\\', 'show_indexes':True}),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_PATH}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

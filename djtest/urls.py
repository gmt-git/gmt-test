from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djtest/', include('djtest.foo.urls')),
    (r'^$', 'djtest.hello.views.home_page'),
    (r'^cxpr_test/$', 'djtest.hello.views.cxpr_test'),
    (r'^edit_contacts/$', 'djtest.hello.views.edit_contacts'),
    (r'^auth_req/edit_contacts/$', 'djtest.hello.views.auth_req_edit_contacts'),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout, {'next_page': '/'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

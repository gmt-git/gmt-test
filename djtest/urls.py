from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout

from djtest.hello.models import HttpReqs

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

httpreqs_info = {
    'queryset': HttpReqs.objects.order_by('-date')[:10]
}

urlpatterns = patterns('',
    # Example:
    # (r'^djtest/', include('djtest.foo.urls')),
    (r'^$', 'djtest.hello.views.home_page'),
    (r'^cxpr_test/$', 'djtest.hello.views.cxpr_test'),
    (r'^edit_contacts/$', 'djtest.hello.views.edit_contacts'),
    (r'^auth_req/edit_contacts/$', 'djtest.hello.views.auth_req_edit_contacts'),
    (r'^edit_contacts_form/$', 'djtest.hello.views.edit_contacts_form'),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout, {'next_page': '/'}),
    (r'^httpreqs_log/$', 'django.views.generic.list_detail.object_list', httpreqs_info),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^debug/tags/(?P<tag_name>[a-z_]*)/(?P<err_code>\d)/$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'debug/tag_rendering_error.html'}),
)

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to, direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('3760.cv.views',
    url(r'^index/$', 'index', name='cv-index'),
    url(r'^editcv/$', 'editcv', name='cv-editcv'),

    url(r'^biographical/$', 'biographical', name='cv-biographical'),
    url(r'^off_campus/$', 'freeformat', {'section': 'off_campus'}, name='cv-off-campus'),
    url(r'^research/grants/$', 'research_grants', name='cv-research-grants'),
    url(r'^teaching/courses/$', 'teaching_courses', name='cv-teaching-courses'),
    url(r'^teaching/graduate/$', 'teaching_graduate', name='cv-teaching-graduate'),
    url(r'^service/contributions/$', 'service', name='cv-service-contributions'),
    url(r'^export/$', 'export_download', {'download': False}, name='cv-export'),
    url(r'^export_download/$', 'export_download', {'download': True},
        name='cv-export-download'),
    url(r'^teaching/(support|scholarship|other|course_development|recognition|counselling)?/?$', 'freeformat', {'section': 'teaching'}, name='cv-teaching'),
    url(r'^research/(professional_consulting|patents|other|recognition)?/?$', 'freeformat', {'section': 'research'}, name='cv-research'),
    url(r'^executive/$', 'freeformat', {'section': 'executive'}, name='cv-executive'),
    url(r'^executive/doe$', 'distribution_of_effort', name='cv-distribution-of-effort'),
    url(r'^autocomplete/$', 'autocomplete', name='cv-autocomplete'),
)

urlpatterns += patterns('',
    (r'^$', redirect_to, {'url': '/index/'}),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
        'login.html'}, name="cv-login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':
        '/'}, name="cv-logout")
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

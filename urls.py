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
    url(r'^executive/$', 'executive', name='cv-executive'),
    url(r'^biographical/$', 'biographical', name='cv-biographical'),
    url(r'^off_campus_recognition/$', 'off_campus_recognition',
        name='cv-off-campus-recognition'),
    url(r'^research/grants/$', 'research_grants', name='cv-research-grants'),
    url(r'^research/consulting/$', 'research_consulting', name='cv-research-consulting'),
    url(r'^research/patents/$', 'research_patents', name='cv-research-patents'),
    url(r'^research/other/$', 'research_other', name='cv-research-other'),
    url(r'^research/recognition/$', 'research_recognition', name='cv-research-recognition'),
    url(r'^research_activity/$', 'research_activity', name='cv-research-activity'),
    url(r'^report_on_teaching/$', 'report_on_teaching', name='cv-report-on-teaching'),
    url(r'^teaching/courses/$', 'courses', name='cv-teaching-courses'),
    url(r'^teaching/counselling/$', 'counselling', name='cv-teaching-counselling'),
    url(r'^teaching/graduate/$', 'graduate', name='cv-teaching-graduate'),
    url(r'^service/contributions/$', 'service', name='cv-service-contributions'),
    url(r'^export/$', 'export_download', {'download': False}, name='cv-export'),
    url(r'^export_download/$', 'export_download', {'download': True},
        name='cv-export-download'),
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

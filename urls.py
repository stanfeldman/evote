from django.conf.urls.defaults import *
from django.conf import *
from views import *
from django.views.generic import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'', include("about.urls")),
    (r'^vote/', include("vote.urls")),
    (r'^auth/', include("auth.urls")),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
   )



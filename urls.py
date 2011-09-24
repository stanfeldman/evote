from django.conf.urls.defaults import *
from django.conf import *
from views import *
from django.views.generic import *

urlpatterns = patterns('',
	(r'', include("about.urls")),
    (r'^vote/', include("vote.urls")),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
   )



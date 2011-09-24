from django.conf.urls.defaults import *
from views import *
from django.views.generic import *

urlpatterns = patterns('',
    (r"choice/(\d+)/$", choice),
    (r"find/$", find),
    (r"submit/$", submit),
)


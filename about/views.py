# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponseRedirect

def index(request):
	return render_to_response("about/templates/index.html", locals(), context_instance=RequestContext(request))


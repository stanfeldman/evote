# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponseRedirect
from vote.models import *

def index(request):
	poll_list = Poll.objects.all()
	return render_to_response("about/templates/index.html", locals(), context_instance=RequestContext(request))


# -*- coding: utf-8 -*-
from django.shortcuts import *
import datetime
from django.contrib.auth.decorators import login_required
from django.http import *

#@login_required
def start(request):
	return render_to_response("vote/templates/start.html", locals(), context_instance=RequestContext(request))


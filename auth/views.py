# -*- coding: utf-8 -*-
from django.shortcuts import *
from django.http import HttpResponseRedirect
import django.contrib.auth

def login(request):
	state = "Please log in below..."
	username = password = ''
	next=request.GET.get("next");
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = django.contrib.auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				django.contrib.auth.login(request, user)
				state = "You're successfully logged in!"
				return HttpResponseRedirect(next)
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Your username and/or password were incorrect."
	return render_to_response("auth/templates/login.html", locals(), context_instance=RequestContext(request))


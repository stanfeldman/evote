# -*- coding: utf-8 -*-
from django.shortcuts import *
import datetime
from django.contrib.auth.decorators import login_required
from django.http import *
from vote.models import *
import datetime
import random
import uuid

@login_required
def choice(request, pk):
	poll = get_object_or_404(Poll, id=pk)

	choice_list = poll.choice_set.all()
	permutation = range(choice_list.count())
	random.shuffle(permutation)
	shuffled_choice_list = [choice_list[i] for i in permutation]

	return render_to_response("vote/templates/choice.html", locals(), context_instance=RequestContext(request))
	
@login_required
def submit(request):
	if request.POST:
		choice = get_object_or_404(Choice, id=request.POST.get('choice'))
		user_choice = UserChoice(user=request.user, choice=choice)
		user_choice.save()
		return render_to_response("vote/templates/submit.html", locals(), context_instance=RequestContext(request))
	
def find(request):
	return render_to_response("vote/templates/find.html", locals(), context_instance=RequestContext(request))


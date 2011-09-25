# -*- coding: utf-8 -*-
import sys
from django.shortcuts import *
import datetime
from django.contrib.auth.decorators import login_required
from django.http import *
from vote.models import *
import datetime
import random
import uuid
from django.core.urlresolvers import reverse
from lib import evotegen


@login_required
def choice(request, pk):
	poll = get_object_or_404(Poll, id=pk)
	# if user have already voted show can't vote page
	
	# generate random choice list
	choice_list = poll.choice_set.all()
	permutation = range(choice_list.count())
	random.shuffle(permutation)
	shuffled_choice_list = [choice_list[i] for i in permutation]
	shuffled_choice_ids_list = [choice.id for choice in shuffled_choice_list]
	
	ballot = Ballot(poll = poll)

	e = evotegen.eVoteGEN()
	enc = e.round_encrypt(str(shuffled_choice_ids_list))
	ballot.uuid = enc['uuid']
	ballot.encoded_permutation = enc['evp']
	
	ballot.save()
	return render_to_response("vote/templates/choice.html", locals(), context_instance=RequestContext(request))
	
@login_required
def submit(request):
	if request.POST:
		ballot = get_object_or_404(Ballot, id=request.POST.get("ballot"))
		ballot.choice_index = request.POST.get("choice");

		e = evotegen.eVoteGEN()
		ballot.date = time.time()
		ballot.sign = e.sign_vote(ballot.encoded_permutation,
					  ballot.choice_index,
					  ballot.date)
		
		ballot.save()
		return render_to_response("vote/templates/vote_result.html", locals(), context_instance=RequestContext(request))
		
def vote_result(request, pk):
	user_choice = get_object_or_404(UserChoice, id=pk)
	user_choice_id = "http://" + request.get_host() + "/vote/vote_result/" + str(user_choice.id)
	return render_to_response("vote/templates/vote_result.html", locals(), context_instance=RequestContext(request))
	
def find(request):
	return render_to_response("vote/templates/find.html", locals(), context_instance=RequestContext(request))


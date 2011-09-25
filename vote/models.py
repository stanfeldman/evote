# -*- coding: utf-8 -*-
from django.db.models import *
from django.contrib.auth.models import User

class Poll(Model):
    question = CharField(max_length=200)
    start_date = DateField()
    end_date = DateField()
    def __unicode__(self):
		return self.question
		
class UserPoll(Model):
	user = ForeignKey(User)
	poll = ForeignKey(Poll)
	date = DateTimeField(auto_now=True)

class Choice(Model):
    poll = ForeignKey(Poll)
    choice = CharField(max_length=200)
    def __unicode__(self):
		return self.choice

class Ballot(Model):
    uuid = CharField(max_length=200)
    poll = ForeignKey(Poll)
    encoded_permutation = CharField(max_length=2048)
    date = DateTimeField(auto_now=True)        
    choice_index = IntegerField(null=True)
    sign = CharField(max_length=1024, null=True)
    
    def __unicode__(self):
        return self.id
	
from django.contrib import admin
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Ballot)

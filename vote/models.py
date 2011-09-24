# -*- coding: utf-8 -*-
from django.db.models import *
from django.contrib.auth.models import User

class Poll(Model):
    question = CharField(max_length=200)
    start_date = DateField()
    end_date = DateField()
    def __unicode__(self):
		return self.question

class Choice(Model):
    poll = ForeignKey(Poll)
    choice = CharField(max_length=200)
    def __unicode__(self):
		return self.choice
	
class UserChoice(Model):
	user = ForeignKey(User)
	choice = ForeignKey(Choice)
	date = DateTimeField()
	
from django.contrib import admin
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(UserChoice)

# -*- coding: utf-8 -*-
from django.db.models import *

class Poll(Model):
    question = CharField(max_length=200)
    pub_date = DateTimeField('date published')

class Choice(Model):
    poll = ForeignKey(Poll)
    choice = CharField(max_length=200)
    votes = IntegerField()

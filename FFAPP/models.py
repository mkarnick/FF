
# Create your models here.
from django.db import models

class Subdomain(models.Model):
	subname = models.CharField(primary_key=True, max_length=128,default='')
	leagueId = models.IntegerField(default=0)
	email = models.EmailField(default='')

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class User(models.Model):
    idx = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=256, default='')
    password = models.CharField(max_length=256, default='')
    firstName = models.CharField(max_length=256, default='')
    lastName  = models.CharField(max_length=256, default='')
    email = models.EmailField(null=True)
    votes = models.IntegerField(default=0)


class ChatText(models.Model):
	parentLeague = models.CharField(default='',max_length=50)
	timestamp = models.CharField(default='',max_length=150)
	actualtimestamp = models.DateTimeField(default='2000-01-01 00:00')
	author = models.CharField(default='',max_length=140)
	commentText = models.CharField(default='',max_length=140)

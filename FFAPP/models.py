
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

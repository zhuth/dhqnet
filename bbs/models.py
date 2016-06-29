#coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True)
    content = models.TextField()
    created = models.DateTimeField(
            default=timezone.now)
    link = models.ForeignKey('self', null=True)

    def publish(self):
        self.author = self.author if self.author and self.author != '' else u'匿名'
        self.created = timezone.now()
        self.save()
        
class Log(models.Model):
    ua = models.CharField(max_length=500)
    fp = models.CharField(max_length=255)
    url = models.CharField(max_length=100)
    args = models.CharField(max_length=1000)
    post = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    
    def log(self):
        self.created = timezone.now()
        self.save()
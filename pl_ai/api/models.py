# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Note(models.Model):
    note = models.CharField(max_length=10);
    start_time = models.FloatField();
    velocity = models.IntegerField();

def __str__(self):
    return "{}".format(self.note, self.start_time, self.velocity)

# Create your models here.

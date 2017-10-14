# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Note(models.Model):
    note = models.IntegerField(default=0);
    start_time = models.IntegerField(default=0);
    velocity = models.IntegerField(default=0);

def __str__(self):
    return "{}".format(self.note, self.start_time, self.velocity)

# Create your models here.

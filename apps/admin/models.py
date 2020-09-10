# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Employee(User):
    class Meta:
        ordering = ("username",)
        proxy = True

    objects = EmployeeManager()
    
    def full_name(self):
        return self.first_name + " - " + self.last_name

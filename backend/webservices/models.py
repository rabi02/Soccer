# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from datetime import datetime
class Assets(models.Model):

    status_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('archived', 'archived')
    )
    enum_choices = (
        ('y', 'y'),
        ('n', 'n')
    )
    imageurl                =   models.TextField(blank=True, null=True)
    image_name              =   models.TextField(blank=True, null=True)
    isdeleted               =   models.CharField(max_length=2,choices=enum_choices, default='n')
    status                  =   models.CharField(max_length=20,choices=status_choices, default='y')
    created_date            =   models.DateTimeField(default=datetime.now, blank=True)
    modified                =   models.DateTimeField(blank=True, null=True)
    isblocked               =   models.CharField(max_length=2,choices=enum_choices,default='n', null=True)
    date                    =   models.FloatField(null=True, blank=True, default=None)
    

    class Meta:
        db_table = 'asset'  

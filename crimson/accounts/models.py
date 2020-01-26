from django.db import models
from django.contrib.auth.models import *# AbstractUser, User
from django.conf import *

class CustomUser(AbstractUser):
    # add additional fields in here
	def __str__(self):
		return self.email

class releaseapk(models.Model):
	# user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blan)
	email_field=models.CharField(max_length=100, blank=True)
	key=models.CharField(max_length=2048, unique=True, blank=True)
	domain_name=models.CharField(max_length=2048, unique=True, blank=True)
	paid=models.BooleanField(default=False)
	
	# def __unicode__(self):
	# 	return self.user

# class debugapk(models.Model):
# 	domain_name=models.CharField(max_length=2048)

# class transaction(models.Model):
# 	paid=models.BooleanField(default=False)

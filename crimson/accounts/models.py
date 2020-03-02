from django.db import models
from django.contrib.auth.models import *# AbstractUser, User
from django.conf import *

class CustomUser(AbstractUser):
    # add additional fields in here
	def __str__(self):
		return self.email

class releaseapk(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	# keystore=models.CharField(max_length=100, blank=True, unique=True)
	# key=models.CharField(max_length=2048, unique=True, blank=True)
	domain_name=models.CharField(max_length=2048, unique=True, blank=True)
	# keystore_link=models.CharField(max_length=120, blank=True, unique=True, default="/dashboard/")
	app_name=models.CharField(max_length=120, default="app")
	paid=models.BooleanField(default=False)
	
class keystore_table(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	keystore=models.CharField(max_length=100, unique=True)
	keystore_link=models.CharField(max_length=120,  unique=True, default="/dashboard/")
	key=models.CharField(max_length=2048, unique=True, )
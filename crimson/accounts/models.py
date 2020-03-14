from django.db import models
from django.contrib.auth.models import *# AbstractUser, User
from django.conf import *

class CustomUser(AbstractUser):
    # add additional fields in here
	def __str__(self):
		return self.email

class releaseapk(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	domain_name=models.CharField(max_length=2048, blank=True)
	app_name=models.CharField(max_length=120, default="app")
	invoice=models.AutoField(primary_key=True)
	date=models.DateField(blank=True)
	paid=models.BooleanField(default=False)
	
class keystore_table(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	keystore=models.CharField(max_length=100)
	keystore_link=models.CharField(max_length=120, default="/dashboard/")
	# key=models.CharField(max_length=2048, unique=True )

class key_table(models.Model):
	keystore=models.ForeignKey(keystore_table, on_delete=models.CASCADE)
	key=models.CharField(max_length=2048)
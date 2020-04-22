from django.db import models
from django.contrib.auth.models import *# AbstractUser, User
from django.conf import *

class CustomUser(AbstractUser):
    
	def __str__(self):
		return self.email

class releaseapk(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	domain_name=models.CharField(max_length=2048)
	app_name=models.CharField(max_length=120, default="app")
	invoice=models.AutoField(primary_key=True)
	date=models.DateField(blank=True, auto_now_add=True)
	paid=models.BooleanField(default=False)
	
class keystore_table(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	# app_name=models.ForeignKey(max_length=120, blank=True)
	keystore=models.CharField(max_length=100)
	keystore_pass=models.CharField(max_length=100)
	keystore_link=models.CharField(max_length=120, default="/dashboard/")
	
	# storepass=models.CharField(max_length=2048, unique=True )
class app_and_keystore(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	keystore=models.CharField(max_length=120)
	app_name=models.CharField(max_length=120)

class key_table(models.Model):
	keystore=models.ForeignKey(keystore_table, on_delete=models.CASCADE)
	key=models.CharField(max_length=2048)
	key_pass=models.CharField(max_length=2048)
	key_user_name=models.CharField(max_length=2048)
	key_organization_unit=models.CharField(max_length=2048)
	key_organization=models.CharField(max_length=2048)
	key_city=models.CharField(max_length=2048)
	key_state=models.CharField(max_length=2048)
	key_country=models.CharField(max_length=2048)



#this is temporary table uses for api.
class temp(models.Model):
	keystore=models.CharField(max_length=120)
	keystore_pass=models.CharField(max_length=120)
	key=models.CharField(max_length=120)
	key_pass=models.CharField(max_length=120)

	class Meta:
		get_latest_by='keystore'

class appname_and_image(models.Model):
	app_name=models.CharField(max_length=120)
	app_icon=models.ImageField(upload_to='icon/', blank=True)

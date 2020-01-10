from django.db import models


class releaseapk(models.Model):
	
	key=models.CharField(max_length=2048, unique=True)
	domain_name=models.CharField(max_length=2048)

class debugapk(models.Model):
	domain_name=models.CharField(max_length=2048)
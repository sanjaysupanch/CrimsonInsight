from django.db import models


class apk(models.Model):
	
	key=models.CharField(max_length=2048, unique=True)
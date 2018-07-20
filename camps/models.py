from django.db import models
from django.db.models import Model

class Camp(Model):
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	startdate = models.DateField()
	enddate = models.DateField()

	def __str__(self):
		return self.name

class Fee(Model):
	camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	price = models.DecimalField(decimal_places=4, max_digits=10)
	startdate = models.DateField()
	enddate = models.DateField()
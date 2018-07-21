from django.db.models import Model, fields, ForeignKey, CASCADE


class Diocese(Model):
	name = fields.CharField(max_length=100)

	def __str__(self):
		return self.name


class District(Model):
	name = fields.CharField(max_length=100)
	diocese = ForeignKey(Diocese, on_delete=CASCADE)

	def __str__(self):
		return self.name


class Clan(Model):
	name = fields.CharField(max_length=100)
	district = ForeignKey(District, on_delete=CASCADE)

	def __str__(self):
		return self.name

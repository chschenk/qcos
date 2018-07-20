from django.db.models import Model, fields, ForeignKey, CASCADE


class Diocese(Model):
	name = fields.CharField(max_length=100)

class District(Model):
	name = fields.CharField(max_length=100)
	diocese = ForeignKey(Diocese, on_delete=CASCADE)

class Clan(Model):
	name = fields.CharField(max_length=100)
	district = ForeignKey(District, on_delete=CASCADE)

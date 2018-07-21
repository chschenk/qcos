from django.db.models import Model, fields, ForeignKey, PROTECT
from base.models import Clan
from camps.models import Fee

#TODO: Think about PROTECT/CASCADE for each model


class Registration(Model):
	clan = ForeignKey(Clan, on_delete=PROTECT)
	telephone = fields.CharField(max_length=100)
	contact_name = fields.CharField(max_length=100)
	email = fields.EmailField(max_length=100)


class TicketInfo(Model):
	registration = ForeignKey(Registration, on_delete=PROTECT)
	fee = ForeignKey(Fee, on_delete=PROTECT)
	quantity = fields.PositiveIntegerField()


class Ticket(Model):
	registration = ForeignKey(Registration, on_delete=PROTECT)
	fee = ForeignKey(Fee, on_delete=PROTECT)
	guid = fields.UUIDField()
	printed = fields.BooleanField()
	registrated = fields.DateTimeField(null=True)

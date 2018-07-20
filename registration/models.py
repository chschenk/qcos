from django.db.models import Model, fields, ForeignKey
from base.models import Clan
from camps.models import Fee


class Registration(Model):
	clan = ForeignKey(Clan)
	telephone = fields.CharField(max_length=100)
	contact_name = fields.CharField(max_length=100)
	email = fields.EmailField(max_length=100)


class TicketInfo(Model):
	registration = ForeignKey(Registration)
	fee = ForeignKey(Fee)
	quantity = fields.PositiveIntegerField()


class Ticket(Model):
	registration = ForeignKey(Registration)
	fee = ForeignKey(Fee)
	guid = fields.UUIDField()
	printed = fields.BooleanField()
	registrated = fields.DateTimeField(null=True)

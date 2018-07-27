from django.db.models import Model, fields, ForeignKey, PROTECT, CASCADE
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from base.models import Clan
from camps.models import Fee, Camp
#TODO: Think about PROTECT/CASCADE for each model


def validate_true(value):
	if not value:
		raise ValidationError("Has to be checked")


class Registration(Model):
	camp = ForeignKey(Camp, on_delete=CASCADE)
	clan = ForeignKey(Clan, on_delete=PROTECT)
	telephone = fields.CharField(max_length=100)
	contact_name = fields.CharField(max_length=100)
	email = fields.EmailField(max_length=100)
	comment = fields.TextField(max_length=1000, null=True, blank=True)
	paid = fields.DecimalField(decimal_places=2, max_digits=6, default=0)
	rules_accepted = fields.BooleanField(default=False, validators=[validate_true])
	present_participants = fields.PositiveIntegerField(null=True)

	def get_price(self):
		price = 0
		for info in self.ticketinfo_set.all():
			price += info.quantity * info.fee.price
		return price

	def get_quantity(self):
		quantity = 0
		for info in self.ticketinfo_set.all():
			quantity += info.quantity
		return quantity

	def get_quantities(self):
		quantities = list()
		for fee in self.camp.fee_set.all().order_by('pk'):
			value = 0
			for info in self.ticketinfo_set.all():
				if info.fee == fee:
					value = info.quantity
			quantities.append(value)
		return quantities

	def get_ticket_count(self):
		tickets = list()
		for info in self.ticketinfo_set.all():
			tickets.extend(info.ticket_set.all())
		return len(tickets)

	def get_registrated_participant_count(self):
		count = 0
		for info in self.ticketinfo_set.all():
			for ticket in info.ticket_set.all():
				if ticket.registrated:
					count += 1
		return count

	def __str__(self):
		return "Registration from {}".format(self.clan.name)


class TicketInfo(Model):
	registration = ForeignKey(Registration, on_delete=PROTECT)
	fee = ForeignKey(Fee, on_delete=PROTECT)
	quantity = fields.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.quantity)


class Ticket(Model):
	ticket_info = ForeignKey(TicketInfo, on_delete=PROTECT)
	guid = fields.UUIDField()
	printed = fields.BooleanField(default=False)
	registrated = fields.DateTimeField(null=True)
